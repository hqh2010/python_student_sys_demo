# 删除实验时，需要更新实验所属的其它方案
# 删除某个方案时，需要更新其它方案（方案间实验是重合的）
# 删除方案中间的某个实验时，该实验后面的id也需要刷新
# swb添加工具时，会创建一个虚拟结点，添加工具后再添加参数创建实验
# 创建工程 --> 添加工具 --> 添加参数
import copy
import datetime
import os
import subprocess
import threading
from threading import RLock

single_lock = RLock()


def Singleton(cls):
    instance = {}

    def _singleton_wrapper(*args, **kargs):
        with single_lock:
            if cls not in instance:
                instance[cls] = cls(*args, **kargs)
        return instance[cls]

    return _singleton_wrapper


# fix to do prj_node_max_id定义挪到Project中去
prj_node_max_id = 1


class ExperimentNode:
    def __init__(self, id, param_key, param_value, parent_node, children_list):
        # 结点类型（暂时未使用）
        self.type = 1
        # node id
        self.id = id
        # 结点对应的参数名称
        self.param_key = param_key
        self.param_value = param_value
        # 结点运行状态（暂时未使用）
        self.status = "none"
        self.is_default = False
        # 结点所属实验ID（暂时未使用）
        self.experiment_id = None
        # 字段（暂时未使用）
        self.parent = parent_node
        # 字段（暂时未使用）
        self.children = children_list
        # 字段（暂时未使用）
        self.scenario = None


class ExperimentTree:
    def __init__(self):
        # 字段（暂时未使用）
        self.id = 1
        # self.scenarios = list[str]
        # self.node_list = list[ExperimentNode]
        self.scenarios = []
        self.node_list = []


class ToolNode:
    def __init__(self, name, path):
        # 当前点工具名字，不可重复
        self.name = name
        # 当前点工具的位置
        self.pos = 0
        # self.type = ''
        # self.label = ''
        # self.comment = ''
        self.icon = ''
        self.path = path
        # params:dict[str,list]
        self.params_dict = {}
        self.params_list = []

    def edit_cmd(self):
        # fix to do file_name要根据点工具类型变化
        file_name = f'./{self.name}_des.cmd'
        if not os.path.exists(file_name):
            file = open(file_name, 'w', encoding='utf-8')
            file.close()
        cmd_str = f'xdg-open {file_name}'
        # subprocess.Popen(cmd_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        os.system(cmd_str)

    def add_param(self, scenario, param_name, value_list, param_pos, prj):
        # 以append方式添加参数
        if len(self.params_list) <= param_pos:
            self.__append_param(scenario, param_name, value_list, param_pos, prj)
        else:
            self.__insert_param(scenario, param_name, value_list, param_pos, prj)

    def __append_param(self, scenario, param_name, value_list, param_pos, prj):
        # 以append方式添加参数
        if len(self.params_list) <= param_pos:
            self.params_list.insert(param_pos, param_name)
            self.params_dict[param_name] = value_list
            global prj_node_max_id
            old_experiments = copy.deepcopy(prj.experiments)
            cur_experiments = prj.experiments
            # 当前scenario添加参数，默认参数为default
            # 找插入点
            # 当前点工具的前一个参数结点 golden给工具结点第一次添加参数时无位置选项
            # 计算参数结点insert pos self.pos为当前工具结点的位置
            insert_pos = 0
            for index in range(0, self.pos):
                insert_pos += len(prj.tool_list[index].params_list)
            # 计算当前点工具的偏移
            insert_pos += param_pos
            for i in range(0, len(old_experiments)):
                for j in range(0, len(value_list)):
                    tmp = ExperimentNode(prj_node_max_id, param_name, value_list[j], None, None)
                    prj_node_max_id += 1
                    if j == 0:
                        # ExperimentTree的第一个结点为根结点
                        # 对于第一条实验直接将参数结点插入
                        cur_experiments[i * len(value_list) + j].node_list.insert(insert_pos, tmp)
                    else:
                        tmp_tree = ExperimentTree()
                        for tmp_node in old_experiments[i].node_list:
                            tmp_tree.node_list.append(tmp_node)
                        tmp_tree.node_list.insert(insert_pos, tmp)
                        cur_experiments.insert(i * len(value_list) + j, tmp_tree)

    def __insert_param(self, scenario, param_name, value_list, param_pos, prj):
        # 以insert方式添加参数
        if len(self.params_list) > param_pos:
            self.params_dict[param_name] = value_list
            params_list_backup = copy.deepcopy(self.params_list)
            params_list_backup.insert(param_pos, param_name)
            # 插入操作转化为顺序追加参数
            del self.params_list[param_pos:]
            # 计算参数结点 insert pos self.pos为当前工具结点的位置
            insert_pos = 0
            for index in range(0, self.pos):
                insert_pos += len(prj.tool_list[index].params_list)
            # 计算当前点工具的偏移
            insert_pos += param_pos
            cur_experiments = prj.experiments

            # 删掉参数后，同时删除重复的实验
            last_param = params_list_backup[-1]
            step = len(self.params_dict[last_param])
            new_experiments = [cur_experiments[index] for index in range(0, len(cur_experiments)) if index % step == 0]
            prj.experiments = new_experiments
            # 更新当前所有实验
            for exp in new_experiments:
                del exp.node_list[insert_pos:]

            for i in range(param_pos, len(params_list_backup)):
                tmp_name = params_list_backup[i]
                self.__append_param(scenario, tmp_name, self.params_dict[tmp_name], i, prj)

    def del_param(self, scenario, param_name, prj):
        if param_name not in self.params_list:
            print(f'del_param input param \'{param_name}\' error')
            return
        param_pos = 0
        for i in range(0, len(self.params_list)):
            if param_name == self.params_list[i]:
                param_pos = i
                break
        # 计算待删除参数结点的位置
        del_pos = 0
        for index in range(0, self.pos):
            del_pos += len(prj.tool_list[index].params_list)
        # 计算当前点工具的偏移
        del_pos += param_pos
        if len(self.params_dict[param_name]) == 1:
            cur_experiments = prj.experiments
            for exp in cur_experiments:
                del exp.node_list[del_pos]
        else:
            step = len(self.params_dict[param_name])
            cur_experiments = prj.experiments
            new_experiments = [cur_experiments[index] for index in range(0, len(cur_experiments)) if index % step == 0]
            prj.experiments = new_experiments
            for exp in prj.experiments:
                del exp.node_list[del_pos]

        self.params_list.remove(param_name)
        del self.params_dict[param_name]


class Project:
    def __init__(self, name):
        self.label = name
        self.description = 'this is a project'
        self.full_path = None
        self.status = {}
        # self.tool_list = list[ToolNode]
        self.tool_list = []
        # self.scenarios = dict[str:list[ExperimentTree]]
        # self.experiments = list[ExperimentTree]
        self.experiments = []

    def add_tool(self, tool_node: ToolNode, pos):
        global prj_node_max_id
        tool_node.pos = pos
        # 是否为首个工具结点
        if len(self.tool_list) == 0:
            # 空结点的key暂定为#
            tool_node.params_list.append('#')
            tool_node.params_dict['#'] = ['--']
            self.tool_list.append(tool_node)
            node = ExperimentNode(prj_node_max_id, '#', '--', None, None)
            prj_node_max_id += 1
            tmp_tree = ExperimentTree()
            tmp_tree.node_list.append(node)
            # fix to do 当前默认方案名为default
            scenario_tmp = "default"
            if scenario_tmp not in tmp_tree.scenarios:
                tmp_tree.scenarios.append(scenario_tmp)
            self.experiments.append(tmp_tree)
        elif pos >= 0 and pos <= len(self.tool_list):
            tool_node.params_list.append('#')
            tool_node.params_dict['#'] = ['--']
            self.tool_list.insert(pos, tool_node)
            # 计算插入位置
            insert_pos = 0
            for index in range(0, pos):
                insert_pos += len(self.tool_list[index].params_list)
            for emp in self.experiments:
                node = ExperimentNode(prj_node_max_id, '#', '--', None, None)
                # 插入若干虚拟结点，参考Golden有几条实验就插入几条--虚拟结点
                emp.node_list.insert(insert_pos, node)
                prj_node_max_id += 1
            # 更新项目中其它点工具的位置
            for i in range(pos + 1, len(self.tool_list)):
                self.tool_list[i].pos = i
        else:
            print(f'add_tool input param {pos} error')

    def del_tool(self, scenario, name):
        tool_index = 0
        for i in range(0, len(self.tool_list)):
            if self.tool_list[i].name == name:
                tool_index = i
                break
        # 计算删除结点的位置
        base_index = 0
        for i in range(0, tool_index):
            base_index += len(self.tool_list[i].params_list)
        # 倒序删除
        for i in range(len(self.tool_list[tool_index].params_list) - 1, -1, -1):
            param_key = self.tool_list[tool_index].params_list[i]
            step = len(self.tool_list[tool_index].params_dict[param_key])
            if step > 1:
                cur_experiments = self.experiments
                new_experiments = [cur_experiments[index] for index in range(0, len(cur_experiments)) if
                                   index % step == 0]
                self.experiments = new_experiments
            for exp in self.experiments:
                del exp.node_list[base_index + i]
        del self.tool_list[tool_index]
        # 更新项目中其它点工具的位置
        for i in range(0, len(self.tool_list)):
            self.tool_list[i].pos = i

        if len(self.tool_list) == 0:
            self.experiments.clear()

    def add_experiment(self, scenario, **kwargs):
        key_num = 0
        for tool_node in self.tool_list:
            # 虚拟结点不用填
            key_num += len(tool_node.params_list) - 1
        if len(kwargs) != key_num:
            print('add_experiment input param num error')
            return
        flag = False
        for key in kwargs:
            for tool_node in self.tool_list:
                if key in tool_node.params_list:
                    flag = True
                    break
            if not flag:
                print(f'input param error, \'{key}\' is not a valid param')
                return
            flag = False
        compare_tree = copy.deepcopy(self.experiments[0])
        for tmp_node in compare_tree.node_list:
            if tmp_node.param_key != '#':
                tmp_node.param_value = kwargs[tmp_node.param_key]
        global prj_node_max_id
        # 查找新增实验的插入位置
        max_row = 0
        max_col = 0
        dst_pos = [max_row, max_col]
        for i in range(0, len(self.experiments)):
            # j从1开始过滤掉第一个虚拟结点
            for j in range(1, len(self.experiments[i].node_list)):
                compare_node = compare_tree.node_list[j]
                dest_node = self.experiments[i].node_list[j]
                # 查找最后一个相同的结点
                if compare_node.param_value == dest_node.param_value:
                    max_row = i
                    max_col = j
                else:
                    break
                if max_col >= dst_pos[1]:
                    dst_pos[0] = max_row
                    dst_pos[1] = max_col
        # 全新的实验
        if dst_pos[1] == 0:
            tmp_tree = ExperimentTree()
            tmp_tree.node_list.append(self.experiments[0].node_list[0])
            for j in range(1, len(compare_tree.node_list)):
                node = ExperimentNode(prj_node_max_id, compare_tree.node_list[j].param_key,
                                      compare_tree.node_list[j].param_value, None, None)
                tmp_tree.node_list.append(node)
                prj_node_max_id += 1
                # 更新工具结点参数的取值范围
                for tool_node in self.tool_list:
                    if compare_tree.node_list[j].param_key in tool_node.params_list:
                        if compare_tree.node_list[j].param_value not in tool_node.params_dict[
                            compare_tree.node_list[j].param_key]:
                            tool_node.params_dict[compare_tree.node_list[j].param_key].append(
                                compare_tree.node_list[j].param_value)
            self.experiments.append(tmp_tree)
        else:
            if dst_pos[1] == len(compare_tree.node_list) - 1:
                print('add a duplicated experiment')
                return
            tmp_tree = ExperimentTree()
            for j in range(0, dst_pos[1] + 1):
                tmp_tree.node_list.append(self.experiments[dst_pos[0]].node_list[j])
            for j in range(dst_pos[1] + 1, len(compare_tree.node_list)):
                node = ExperimentNode(prj_node_max_id, compare_tree.node_list[j].param_key,
                                      compare_tree.node_list[j].param_value, None, None)
                tmp_tree.node_list.append(node)
                prj_node_max_id += 1
                # 更新工具结点参数的取值范围
                for tool_node in self.tool_list:
                    if compare_tree.node_list[j].param_key in tool_node.params_list:
                        if compare_tree.node_list[j].param_value not in tool_node.params_dict[
                            compare_tree.node_list[j].param_key]:
                            tool_node.params_dict[compare_tree.node_list[j].param_key].append(
                                compare_tree.node_list[j].param_value)
            self.experiments.insert(dst_pos[0] + 1, tmp_tree)

    def del_experiment(self, scenario, id):
        if id > len(self.experiments):
            print('del_experiment input param error')
        flag = False
        # 更新工具结点的参数取值范围
        for i in range(1, self.experiments[id - 1].node_list):
            for j in range(1, len(self.experiments)):
                if j != id and self.experiments[j].node_list[i].param_value == self.experiments[id - 1].node_list[
                    i].param_value:
                    flag = True
                    break
            if not flag:
                for tool_node in self.tool_list:
                    key = self.experiments[id - 1].node_list[i].param_key
                    if key in tool_node.params_list:
                        tool_node.params_dict[key].remove(self.experiments[id - 1].node_list[i].param_value)
            flag = False
        del self.experiments[id - 1]
        # 更新其它方案的实验fix to do

    def dump_tree(self, tree_path):
        if len(self.experiments) == 0:
            print('no experiment data to dump')
            return
        with open(os.path.abspath('./gtree.txt'), 'w', encoding='utf-8') as wfile:
            wfile.write('# --- simulation flow\n')
            for tool_node in self.tool_list:
                for param_key in tool_node.params_list:
                    line_info = f'{tool_node.name} {param_key} {tool_node.params_dict[param_key]}'
                    print(line_info)
                    wfile.write(line_info + '\n')
            # just for debug
            print('==========' * len(self.experiments[0].node_list))
            for tmp_tree in self.experiments:
                tree_info = ""
                for tmp_node in tmp_tree.node_list:
                    tree_info += f'[n{tmp_node.id}]:{tmp_node.param_value}' + " "
                print(tree_info)
            print(f'experiments num:{len(self.experiments)}, experiment node num:{len(self.experiments[0].node_list)}')
            # just for debug
            # 打印与Golden一致的记录
            print('==========' * len(self.experiments[0].node_list))
            wfile.write('# --- simulation tree\n')
            record_list = []
            for tmp_tree in self.experiments:
                node_info = ""
                for i in range(0, len(tmp_tree.node_list)):
                    if i == 0:
                        node_info = f'{i} {tmp_tree.node_list[i].id} 0 -- {{default}} 0'
                    else:
                        node_info = f'{i} {tmp_tree.node_list[i].id} {tmp_tree.node_list[i - 1].id} {tmp_tree.node_list[i].param_value} {{default}} 0'
                    if tmp_tree.node_list[i].id not in record_list:
                        print(node_info)
                        wfile.write(node_info + '\n')
                        record_list.append(tmp_tree.node_list[i].id)

    def load_tree(self, tree_path):
        if os.path.exists('./gtree.txt'):
            with open('./gtree.txt', 'r', encoding='utf-8') as rfile:
                while True:
                    line_info = rfile.readline().strip()
                    if line_info.find('simulation flow') != -1:
                        break
                tool_index = 0
                while True:
                    line_info = rfile.readline().strip()
                    # 处理工具结点 line_info不能为空
                    if line_info and line_info.find('simulation tree') == -1:
                        # 点工具结点
                        if line_info.find('#') != -1:
                            tool_info = line_info.split(" ", 2)
                            # fix to do ToolNode path
                            tool_node = ToolNode(tool_info[0], '/home/device/xxxxxx')
                            tool_node.params_list.append(tool_info[1])
                            tool_node.params_dict[tool_info[1]] = eval(tool_info[2])
                            tool_node.pos = tool_index
                            self.tool_list.append(tool_node)
                            tool_index += 1
                        else:
                            tool_info = line_info.split(" ", 2)
                            for tmp_node in self.tool_list:
                                if tool_info[0] == tmp_node.name:
                                    tmp_node.params_list.append(tool_info[1])
                                    tmp_node.params_dict[tool_info[1]] = eval(tool_info[2])
                    else:
                        break

                # 处理实验结点
                # 计算列宽
                table_col = 0
                node_key_list = []
                for tmp_node in self.tool_list:
                    table_col += len(tmp_node.params_list)
                    node_key_list += tmp_node.params_list
                tree_info = rfile.readlines()
                first_tree_info = tree_info[0:table_col]
                global prj_node_max_id
                first_tree = ExperimentTree()
                for node_info in first_tree_info:
                    node_list = node_info.split()
                    node_id = int(node_list[1])
                    node_value = node_list[3]
                    node_key = node_key_list[int(node_list[0])]
                    if node_id > prj_node_max_id:
                        prj_node_max_id = node_id
                    node = ExperimentNode(node_id, node_key, node_value, None, None)
                    first_tree.node_list.append(node)
                self.experiments.append(first_tree)
                # 恢复剩下的实验
                step = 0
                start_pos = table_col
                while True:
                    start_pos += step
                    if start_pos > len(tree_info) - 1:
                        prj_node_max_id += 1
                        break
                    tmp_node_info = tree_info[start_pos].split()
                    step = table_col - int(tmp_node_info[0])
                    tmp_tree = ExperimentTree()
                    for i in range(0, table_col - step):
                        # fix to do 多个tree共用一个结点 与前面的处理方式有差异，是否会有问题
                        tmp_tree.node_list.append(self.experiments[len(self.experiments) - 1].node_list[i])
                    for i in range(start_pos, start_pos + step):
                        node_info = tree_info[i]
                        node_list = node_info.split()
                        node_id = int(node_list[1])
                        if node_id > prj_node_max_id:
                            prj_node_max_id = node_id
                        node_value = node_list[3]
                        node_key = node_key_list[int(node_list[0])]
                        node = ExperimentNode(node_id, node_key, node_value, None, None)
                        tmp_tree.node_list.append(node)
                    self.experiments.append(tmp_tree)
        else:
            print("err no project data found!")


@Singleton
class Controller:
    def edit_cmd(self, tool_node: ToolNode):
        # fix to do file_name要根据点工具类型变化
        file_name = f'./{tool_node.name}_des.cmd'
        if not os.path.exists(file_name):
            file = open(file_name, 'w', encoding='utf-8')
            file.close()
        cmd_str = f'xdg-open {file_name}'
        # subprocess.Popen(cmd_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        os.system(cmd_str)

    def add_param(self, prj, tool_node, scenario, param_name, value_list, param_pos):
        # 以append方式添加参数
        if len(tool_node.params_list) <= param_pos:
            self.__append_param(prj, tool_node, scenario, param_name, value_list, param_pos)
        else:
            self.__insert_param(prj, tool_node, scenario, param_name, value_list, param_pos)

    def __append_param(self, prj, tool_node, scenario, param_name, value_list, param_pos):
        # 以append方式添加参数
        if len(tool_node.params_list) <= param_pos:
            tool_node.params_list.insert(param_pos, param_name)
            tool_node.params_dict[param_name] = value_list
            global prj_node_max_id
            old_experiments = copy.deepcopy(prj.experiments)
            cur_experiments = prj.experiments
            # 当前scenario添加参数，默认参数为default
            # 找插入点
            # 当前点工具的前一个参数结点 golden给工具结点第一次添加参数时无位置选项
            # 计算参数结点insert pos tool_node.pos为当前工具结点的位置
            insert_pos = 0
            for index in range(0, tool_node.pos):
                insert_pos += len(prj.tool_list[index].params_list)
            # 计算当前点工具的偏移
            insert_pos += param_pos
            for i in range(0, len(old_experiments)):
                for j in range(0, len(value_list)):
                    tmp = ExperimentNode(prj_node_max_id, param_name, value_list[j], None, None)
                    prj_node_max_id += 1
                    if j == 0:
                        # ExperimentTree的第一个结点为根结点
                        # 对于第一条实验直接将参数结点插入
                        cur_experiments[i * len(value_list) + j].node_list.insert(insert_pos, tmp)
                    else:
                        tmp_tree = ExperimentTree()
                        for tmp_node in old_experiments[i].node_list:
                            tmp_tree.node_list.append(tmp_node)
                        tmp_tree.node_list.insert(insert_pos, tmp)
                        cur_experiments.insert(i * len(value_list) + j, tmp_tree)

    def __insert_param(self, prj, tool_node, scenario, param_name, value_list, param_pos):
        # 以insert方式添加参数
        if len(tool_node.params_list) > param_pos:
            tool_node.params_dict[param_name] = value_list
            params_list_backup = copy.deepcopy(tool_node.params_list)
            params_list_backup.insert(param_pos, param_name)
            # 插入操作转化为顺序追加参数
            del tool_node.params_list[param_pos:]
            # 计算参数结点 insert pos tool_node.pos为当前工具结点的位置
            insert_pos = 0
            for index in range(0, tool_node.pos):
                insert_pos += len(prj.tool_list[index].params_list)
            # 计算当前点工具的偏移
            insert_pos += param_pos
            cur_experiments = prj.experiments

            # 删掉参数后，同时删除重复的实验
            last_param = params_list_backup[-1]
            step = len(tool_node.params_dict[last_param])
            new_experiments = [cur_experiments[index] for index in range(0, len(cur_experiments)) if
                               index % step == 0]
            prj.experiments = new_experiments
            # 更新当前所有实验
            for exp in new_experiments:
                del exp.node_list[insert_pos:]

            for i in range(param_pos, len(params_list_backup)):
                tmp_name = params_list_backup[i]
                self.__append_param(prj, tool_node, scenario, tmp_name, tool_node.params_dict[tmp_name], i)

    def del_param(self, prj, tool_node, scenario, param_name):
        if param_name not in tool_node.params_list:
            print(f'del_param input param \'{param_name}\' error')
            return
        param_pos = 0
        for i in range(0, len(tool_node.params_list)):
            if param_name == tool_node.params_list[i]:
                param_pos = i
                break
        # 计算待删除参数结点的位置
        del_pos = 0
        for index in range(0, tool_node.pos):
            del_pos += len(prj.tool_list[index].params_list)
        # 计算当前点工具的偏移
        del_pos += param_pos
        if len(tool_node.params_dict[param_name]) == 1:
            cur_experiments = prj.experiments
            for exp in cur_experiments:
                del exp.node_list[del_pos]
        else:
            step = len(tool_node.params_dict[param_name])
            cur_experiments = prj.experiments
            new_experiments = [cur_experiments[index] for index in range(0, len(cur_experiments)) if index % step == 0]
            prj.experiments = new_experiments
            for exp in prj.experiments:
                del exp.node_list[del_pos]

        tool_node.params_list.remove(param_name)
        del tool_node.params_dict[param_name]

    def add_tool(self, prj, tool_node: ToolNode, pos):
        global prj_node_max_id
        tool_node.pos = pos
        # 是否为首个工具结点
        if len(prj.tool_list) == 0:
            # 空结点的key暂定为#
            tool_node.params_list.append('#')
            tool_node.params_dict['#'] = ['--']
            prj.tool_list.append(tool_node)
            node = ExperimentNode(prj_node_max_id, '#', '--', None, None)
            prj_node_max_id += 1
            tmp_tree = ExperimentTree()
            tmp_tree.node_list.append(node)
            # fix to do 当前默认方案名为default
            scenario_tmp = "default"
            if scenario_tmp not in tmp_tree.scenarios:
                tmp_tree.scenarios.append(scenario_tmp)
            prj.experiments.append(tmp_tree)
        elif pos >= 0 and pos <= len(prj.tool_list):
            tool_node.params_list.append('#')
            tool_node.params_dict['#'] = ['--']
            prj.tool_list.insert(pos, tool_node)
            # 计算插入位置
            insert_pos = 0
            for index in range(0, pos):
                insert_pos += len(prj.tool_list[index].params_list)
            for emp in prj.experiments:
                node = ExperimentNode(prj_node_max_id, '#', '--', None, None)
                # 插入若干虚拟结点，参考Golden有几条实验就插入几条--虚拟结点
                emp.node_list.insert(insert_pos, node)
                prj_node_max_id += 1
            # 更新项目中其它点工具的位置
            for i in range(pos + 1, len(prj.tool_list)):
                prj.tool_list[i].pos = i
        else:
            print(f'add_tool input param {pos} error')

    def del_tool(self, prj, scenario, name):
        tool_index = 0
        for i in range(0, len(prj.tool_list)):
            if prj.tool_list[i].name == name:
                tool_index = i
                break
        # 计算删除结点的位置
        base_index = 0
        for i in range(0, tool_index):
            base_index += len(prj.tool_list[i].params_list)
        # 倒序删除
        for i in range(len(prj.tool_list[tool_index].params_list) - 1, -1, -1):
            param_key = prj.tool_list[tool_index].params_list[i]
            step = len(prj.tool_list[tool_index].params_dict[param_key])
            if step > 1:
                cur_experiments = prj.experiments
                new_experiments = [cur_experiments[index] for index in range(0, len(cur_experiments)) if
                                   index % step == 0]
                prj.experiments = new_experiments
            for exp in prj.experiments:
                del exp.node_list[base_index + i]
        del prj.tool_list[tool_index]
        # 更新项目中其它点工具的位置
        for i in range(0, len(prj.tool_list)):
            prj.tool_list[i].pos = i

        if len(prj.tool_list) == 0:
            prj.experiments.clear()

    def add_experiment(self, prj, scenario, **kwargs):
        key_num = 0
        for tool_node in prj.tool_list:
            # 虚拟结点不用填
            key_num += len(tool_node.params_list) - 1
        if len(kwargs) != key_num:
            print('add_experiment input param num error')
            return
        flag = False
        for key in kwargs:
            for tool_node in prj.tool_list:
                if key in tool_node.params_list:
                    flag = True
                    break
            if not flag:
                print(f'input param error, \'{key}\' is not a valid param')
                return
            flag = False
        compare_tree = copy.deepcopy(prj.experiments[0])
        for tmp_node in compare_tree.node_list:
            if tmp_node.param_key != '#':
                tmp_node.param_value = kwargs[tmp_node.param_key]
        global prj_node_max_id
        # 查找新增实验的插入位置
        max_row = 0
        max_col = 0
        dst_pos = [max_row, max_col]
        for i in range(0, len(prj.experiments)):
            # j从1开始过滤掉第一个虚拟结点
            for j in range(1, len(prj.experiments[i].node_list)):
                compare_node = compare_tree.node_list[j]
                dest_node = prj.experiments[i].node_list[j]
                # 查找最后一个相同的结点
                if compare_node.param_value == dest_node.param_value:
                    max_row = i
                    max_col = j
                else:
                    break
                if max_col >= dst_pos[1]:
                    dst_pos[0] = max_row
                    dst_pos[1] = max_col
        # 全新的实验
        if dst_pos[1] == 0:
            tmp_tree = ExperimentTree()
            tmp_tree.node_list.append(prj.experiments[0].node_list[0])
            for j in range(1, len(compare_tree.node_list)):
                node = ExperimentNode(prj_node_max_id, compare_tree.node_list[j].param_key,
                                      compare_tree.node_list[j].param_value, None, None)
                tmp_tree.node_list.append(node)
                prj_node_max_id += 1
                # 更新工具结点参数的取值范围
                for tool_node in prj.tool_list:
                    if compare_tree.node_list[j].param_key in tool_node.params_list:
                        if compare_tree.node_list[j].param_value not in tool_node.params_dict[
                            compare_tree.node_list[j].param_key]:
                            tool_node.params_dict[compare_tree.node_list[j].param_key].append(
                                compare_tree.node_list[j].param_value)
            prj.experiments.append(tmp_tree)
        else:
            if dst_pos[1] == len(compare_tree.node_list) - 1:
                print('add a duplicated experiment')
                return
            tmp_tree = ExperimentTree()
            for j in range(0, dst_pos[1] + 1):
                tmp_tree.node_list.append(prj.experiments[dst_pos[0]].node_list[j])
            for j in range(dst_pos[1] + 1, len(compare_tree.node_list)):
                node = ExperimentNode(prj_node_max_id, compare_tree.node_list[j].param_key,
                                      compare_tree.node_list[j].param_value, None, None)
                tmp_tree.node_list.append(node)
                prj_node_max_id += 1
                # 更新工具结点参数的取值范围
                for tool_node in prj.tool_list:
                    if compare_tree.node_list[j].param_key in tool_node.params_list:
                        if compare_tree.node_list[j].param_value not in tool_node.params_dict[
                            compare_tree.node_list[j].param_key]:
                            tool_node.params_dict[compare_tree.node_list[j].param_key].append(
                                compare_tree.node_list[j].param_value)
            prj.experiments.insert(dst_pos[0] + 1, tmp_tree)

    def del_experiment(self, prj, scenario, id):
        if id > len(prj.experiments):
            print('del_experiment input param error')
        flag = False
        # 更新工具结点的参数取值范围
        for i in range(1, prj.experiments[id - 1].node_list):
            for j in range(1, len(prj.experiments)):
                if j != id and prj.experiments[j].node_list[i].param_value == prj.experiments[id - 1].node_list[
                    i].param_value:
                    flag = True
                    break
            if not flag:
                for tool_node in prj.tool_list:
                    key = prj.experiments[id - 1].node_list[i].param_key
                    if key in tool_node.params_list:
                        tool_node.params_dict[key].remove(prj.experiments[id - 1].node_list[i].param_value)
            flag = False
        del prj.experiments[id - 1]

    def dump_tree(self, prj, tree_path):
        if len(prj.experiments) == 0:
            print('no experiment data to dump')
            return
        with open(os.path.abspath('./gtree.txt'), 'w', encoding='utf-8') as wfile:
            wfile.write('# --- simulation flow\n')
            for tool_node in prj.tool_list:
                for param_key in tool_node.params_list:
                    line_info = f'{tool_node.name} {param_key} {tool_node.params_dict[param_key]}'
                    print(line_info)
                    wfile.write(line_info + '\n')
            # just for debug
            print('==========' * len(prj.experiments[0].node_list))
            for tmp_tree in prj.experiments:
                tree_info = ""
                for tmp_node in tmp_tree.node_list:
                    tree_info += f'[n{tmp_node.id}]:{tmp_node.param_value}' + " "
                print(tree_info)
            print(f'experiments num:{len(prj.experiments)}, experiment node num:{len(prj.experiments[0].node_list)}')
            # just for debug
            # 打印与Golden一致的记录
            print('==========' * len(prj.experiments[0].node_list))
            wfile.write('# --- simulation tree\n')
            record_list = []
            for tmp_tree in prj.experiments:
                node_info = ""
                for i in range(0, len(tmp_tree.node_list)):
                    if i == 0:
                        node_info = f'{i} {tmp_tree.node_list[i].id} 0 -- {{default}} 0'
                    else:
                        node_info = f'{i} {tmp_tree.node_list[i].id} {tmp_tree.node_list[i - 1].id} {tmp_tree.node_list[i].param_value} {{default}} 0'
                    if tmp_tree.node_list[i].id not in record_list:
                        print(node_info)
                        wfile.write(node_info + '\n')
                        record_list.append(tmp_tree.node_list[i].id)

    def load_tree(self, prj, tree_path):
        if os.path.exists('./gtree.txt'):
            with open('./gtree.txt', 'r', encoding='utf-8') as rfile:
                while True:
                    line_info = rfile.readline().strip()
                    if line_info.find('simulation flow') != -1:
                        break
                tool_index = 0
                while True:
                    line_info = rfile.readline().strip()
                    # 处理工具结点 line_info不能为空
                    if line_info and line_info.find('simulation tree') == -1:
                        # 点工具结点
                        if line_info.find('#') != -1:
                            tool_info = line_info.split(" ", 2)
                            # fix to do ToolNode path
                            tool_node = ToolNode(tool_info[0], '/home/device/xxxxxx')
                            tool_node.params_list.append(tool_info[1])
                            tool_node.params_dict[tool_info[1]] = eval(tool_info[2])
                            tool_node.pos = tool_index
                            prj.tool_list.append(tool_node)
                            tool_index += 1
                        else:
                            tool_info = line_info.split(" ", 2)
                            for tmp_node in prj.tool_list:
                                if tool_info[0] == tmp_node.name:
                                    tmp_node.params_list.append(tool_info[1])
                                    tmp_node.params_dict[tool_info[1]] = eval(tool_info[2])
                    else:
                        break

                # 处理实验结点
                # 计算列宽
                table_col = 0
                node_key_list = []
                for tmp_node in prj.tool_list:
                    table_col += len(tmp_node.params_list)
                    node_key_list += tmp_node.params_list
                tree_info = rfile.readlines()
                first_tree_info = tree_info[0:table_col]
                global prj_node_max_id
                first_tree = ExperimentTree()
                for node_info in first_tree_info:
                    node_list = node_info.split()
                    node_id = int(node_list[1])
                    node_value = node_list[3]
                    node_key = node_key_list[int(node_list[0])]
                    if node_id > prj_node_max_id:
                        prj_node_max_id = node_id
                    node = ExperimentNode(node_id, node_key, node_value, None, None)
                    first_tree.node_list.append(node)
                prj.experiments.append(first_tree)
                # 恢复剩下的实验
                step = 0
                start_pos = table_col
                while True:
                    start_pos += step
                    if start_pos > len(tree_info) - 1:
                        prj_node_max_id += 1
                        break
                    tmp_node_info = tree_info[start_pos].split()
                    step = table_col - int(tmp_node_info[0])
                    tmp_tree = ExperimentTree()
                    for i in range(0, table_col - step):
                        # fix to do 多个tree共用一个结点 与前面的处理方式有差异，是否会有问题
                        tmp_tree.node_list.append(prj.experiments[len(prj.experiments) - 1].node_list[i])
                    for i in range(start_pos, start_pos + step):
                        node_info = tree_info[i]
                        node_list = node_info.split()
                        node_id = int(node_list[1])
                        if node_id > prj_node_max_id:
                            prj_node_max_id = node_id
                        node_value = node_list[3]
                        node_key = node_key_list[int(node_list[0])]
                        node = ExperimentNode(node_id, node_key, node_value, None, None)
                        tmp_tree.node_list.append(node)
                    prj.experiments.append(tmp_tree)
        else:
            print("err no project data found!")

    def __run_node_callback(self, prj, scenario, experiment_id, node_id):
        # golden会将点工具的cmd文件拷贝一份,然后以结点名来命名文件作参数替换后再运行
        # 对于Hierarchical类型的项目会新建results/nodes/node_id目录保存结点数据
        # fix to do是否是可运行结点的处理
        dest_index = -1
        for i in range(0, len(prj.experiments[experiment_id].node_list)):
            if prj.experiments[experiment_id].node_list[i].id == node_id:
                dest_index = i
                break
        # 查找结点所属点工具
        col_num = 0
        dest_tool = None
        for tool_node in prj.tool_list:
            col_num += len(tool_node.params_list)
            if col_num >= dest_index:
                dest_tool = tool_node
                break

        node_dir = f'./results/nodes/{node_id}'
        if not os.path.exists(node_dir):
            os.makedirs(node_dir)
        # fix to do 点工具对应的模板文件名参考 edit_cmd 方法
        tool_cmd_name = f'./{dest_tool.name}_des.cmd'
        dest_node = prj.experiments[experiment_id].node_list[dest_index]
        node_cmd_name = f'./{node_dir}/n{node_id}_des.cmd'
        with open(f'./{tool_cmd_name}', 'r', encoding='utf-8') as rfile:
            cmd_info = rfile.read()
            node_cmd_info = cmd_info.replace(f'@{dest_node.param_key}@', dest_node.param_value)
            with open(f'./{node_cmd_name}', 'w', encoding='utf-8') as wfile:
                wfile.write(node_cmd_info)
        # 默认点工具的输入文件是python脚本，脚本文件调用点工具时需要同步调用，否则结点状态刷新会异常
        cmd_str = f'python {node_cmd_name}'
        proc = subprocess.Popen(cmd_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        proc.wait()
        # fix to do更新结点运行状态
        dest_node.status = 'done'
        cur_time = datetime.datetime.now().time().strftime("%H:%M:%S")
        print(f'{cur_time} node:n{node_id} run done')

    def run_node(self, prj, scenario, experiment_id, node_id):
        cur_time = datetime.datetime.now().time().strftime("%H:%M:%S")
        print(f'{cur_time} node:n{node_id} run begin')
        if experiment_id > len(prj.experiments) - 1:
            return
        task = threading.Thread(target=self.__run_node_callback, args=(prj, scenario, experiment_id, node_id))
        task.start()

    def __run_experiment_callback(self, prj, scenario, experiment_id):
        run_node_list = []
        index = 0
        for tool_node in prj.tool_list:
            index += len(tool_node.params_list)
            if prj.experiments[experiment_id].node_list[index - 1].param_key != '#':
                run_node_list.append(prj.experiments[experiment_id].node_list[index - 1])
        for tmp_node in run_node_list:
            cur_time = datetime.datetime.now().time().strftime("%H:%M:%S")
            self.__run_node_callback(prj, scenario, experiment_id, tmp_node.id)

        cur_time = datetime.datetime.now().time().strftime("%H:%M:%S")
        print(f'{cur_time} experiment:{experiment_id} run done')

    def run_experiment(self, prj, scenario, experiment_id):
        cur_time = datetime.datetime.now().time().strftime("%H:%M:%S")
        print(f'{cur_time} experiment:{experiment_id} run begin')
        if experiment_id > len(prj.experiments) - 1:
            return
        # fix to do ThreadPoolExecutor
        task = threading.Thread(target=self.__run_experiment_callback, args=(prj, scenario, experiment_id))
        task.start()


# prj = Project('prj1')
# edevice_path = "/home/device/xxxxxx"
# edevice_tool = ToolNode('eDevice', edevice_path)
# # 添加实验有两种方式，一种是添加参数，一种是直接右键添加实验
# prj.add_tool(edevice_tool, 0)
# edevice_tool.add_param('default', 'Lg', ['0.25'], 1, prj)
# edevice_tool.add_param('default', 'NWell', ['1e+17', '2e+17'], 2, prj)
# edevice_tool.add_param('default', 'LDD_Dose', ['1e+14', '2e+14'], 3, prj)
#
# # 在参数LDD_Dose前插入一个参数GOxTime
# edevice_tool.add_param('default', 'GOxTime', ['10', '15'], 3, prj)
#
# evisual_path = "/home/visual/xxxxxx"
# evisual_tool = ToolNode('eVisual', evisual_path)
# prj.add_tool(evisual_tool, 1)
# evisual_tool.add_param('default', 'Vd', ['0.5'], 1, prj)
# # 在Vd前面插入一个Id参数
# evisual_tool.add_param('default', 'Id', ['0.6', '0.8'], 1, prj)

# # 给点工具添加命令
# evisual_tool.edit_cmd()

# # 删除evisual最后一个单结点参数0.5
# evisual_tool.del_param('default', 'Vd', prj)

# 删除evisual中间的一个单结点参数[0.6, 0.8]
# evisual_tool.del_param('default', 'Id', prj)

# 在中间插入一个点工具
# eprocess_path = "/home/process/xxxxxx"
# eprocess_tool = ToolNode('eProcess', eprocess_path)
# prj.add_tool(eprocess_tool, 1)
# eprocess_tool.add_param('default', 'P0', ['0.5', '0.8'], 1, prj)

# # 增加实验
# prj.add_experiment('default', Lg = '0.20', NWell='1e+17', GOxTime='10',LDD_Dose='1e+14', Vd='0.5')
# # 增加一条完全相同的实验
# prj.add_experiment('default', Lg='0.25', NWell='1e+17', GOxTime='10', LDD_Dose='1e+14', Id='0.8', Vd='0.5')
# # 增加一个部分相同的实验
# prj.add_experiment('default', Lg='0.25', NWell='1e+17', GOxTime='15', LDD_Dose='3e+14', Vd='0.5')

# # 删除点工具
# prj.del_tool('default', 'eVisual')
# prj.del_tool('default', 'eDevice')
# prj.dump_tree("")

# # 验证反序列化
# prj.load_tree("")
# prj.dump_tree("")

##使用controller测试
contrl = Controller()

prj = Project('prj1')
edevice_path = "/home/device/xxxxxx"
edevice_tool = ToolNode('eDevice', edevice_path)
# 添加实验有两种方式，一种是添加参数，一种是直接右键添加实验
contrl.add_tool(prj, edevice_tool, 0)
contrl.add_param(prj, edevice_tool, 'default', 'Lg', ['0.25'], 1)
contrl.add_param(prj, edevice_tool, 'default', 'NWell', ['1e+17', '2e+17'], 2)
contrl.add_param(prj, edevice_tool, 'default', 'LDD_Dose', ['1e+14', '2e+14'], 3)

# 在参数LDD_Dose前插入一个参数GOxTime
contrl.add_param(prj, edevice_tool, 'default', 'GOxTime', ['10', '15'], 3)

evisual_path = "/home/visual/xxxxxx"
evisual_tool = ToolNode('eVisual', evisual_path)
contrl.add_tool(prj, evisual_tool, 1)
contrl.add_param(prj, evisual_tool, 'default', 'Vd', ['0.5'], 1)
# # 在Vd前面插入一个Id参数
# contrl.add_param(prj, evisual_tool, 'default', 'Id', ['0.6', '0.8'], 1)

# # 给点工具添加命令
# contrl.edit_cmd(edevice_tool)

# # 删除evisual最后一个单结点参数0.5
# contrl.del_param(prj, evisual_tool, 'default', 'Vd')

# # 删除evisual中间的一个单结点参数[0.6, 0.8]
# contrl.del_param(prj, evisual_tool, 'default', 'Id')

# # 在中间插入一个点工具
# eprocess_path = "/home/process/xxxxxx"
# eprocess_tool = ToolNode('eProcess', eprocess_path)
# contrl.add_tool(prj, eprocess_tool, 1)
# contrl.add_param(prj, eprocess_tool, 'default', 'P0', ['0.5', '0.8'], 1)

# 增加实验
# contrl.add_experiment(prj, 'default', Lg='0.20', NWell='1e+17', GOxTime='10', LDD_Dose='1e+14', Vd='0.5')
# 增加一条完全相同的实验
# contrl.add_experiment(prj, 'default', Lg='0.25', NWell='1e+17', GOxTime='10', LDD_Dose='1e+14', Vd='0.5')
# 增加一个部分相同的实验
# contrl.add_experiment(prj, 'default', Lg='0.25', NWell='1e+17', GOxTime='15', LDD_Dose='3e+14', Vd='0.5')

# 删除点工具
# contrl.del_tool(prj, 'default', 'eVisual')
# contrl.del_tool(prj,'default', 'eDevice')

# 运行单个结点
# contrl.run_node(prj, 'default', 0, 13)
# print("wait node to run finish~~~")
# contrl.run_node(prj, 'default', 0, 29)
# 运行一条实验
contrl.run_experiment(prj, 'default', 0)
print("wait experiment to run finish~~~")

# contrl.dump_tree(prj, "")

