# eVisual接口文档

### set_2d_plot_params

- 函数描述

  设置待显示曲线的x轴和y轴坐标的参数名称。

- 函数格式

  ```
  def set_2d_plot_params(axis_x: str="", axis_y: str="")
  ```
  
- 输入参数

  | 参数   | 类型 | 是否必须 | 示例值          | 描述                                                         |
  | ------ | ---- | -------- | --------------- | ------------------------------------------------------------ |
  | axis_x | str  | false    | P,OuterVoltage  | 设置plt图x轴坐标的参数名称，参数名称必须为plt文件数据集中的参数，plt文件路径参考[run](#run)接口中的filepath |
  | axis_y | str  | false    | P,ToltalCurrent | 设置plt图y轴坐标的参数名称，参数名称必须为plt文件数据集中的参数，plt文件路径参考[run](#run)接口中的filepath |
  
- 示例

  ```
  set_2d_plot_params(axis_x="P,OuterVoltage", axis_y="P,ToltalCurrent")
  ```
  
- 说明

  所有的设置必须在调用run接口前调用，否则设置无效。


### show_params

- 函数描述

  查询所有设置待显示的plt图的参数信息。

- 函数格式

  ```
  def show_params()
  ```
  
- 输入参数

  无
  
- 示例

  ```
  show_params()
  ```

### <a id="run">run</a>

- 函数描述

  调用run接口，启动evisual点工具。

- 函数格式

  ```
  def run(
      filepath: str="",
  ) -> Tuple[code, message, result]:
      pass
  ```
  
- 输入参数

  | 参数     | 类型 | 是否必须 | 示例值   | 描述                                          |
  | -------- | ---- | -------- | -------- | --------------------------------------------- |
  | filepath | str  | false    | 'pn.plt' | 输入文件, 加载需要显示的plot文件路径，tdr格式 |
  
- 示例

  ```
  run(filepath="/home/xxx.plt")
  ```
  


- 输出参数

  返回一个具有三个元素的Tuple，类型为Tuple[code, message, result]。其中三个元素的详细信息如下表所示。

  | 序号 | 含义                     | 类型   | 示例值     | 默认值 |
  | ---- | ------------------------ | ------ | ---------- | ------ |
  | 1    | 响应的code码             | INT    | 10001      |        |
  | 2    | 响应的成功或失败消息内容 | STRING | 参数不正确 |        |
  | 3    | 成功响应返回的结果       | ANY    |            | NONE   |

- 成功响应示例

  ```
  (0,"success",None)
  ```

- 错误响应示例

  ```
  (10001,"参数不正确")
  ```

