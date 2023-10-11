# coding: utf-8
import datetime
import os
import subprocess
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import time


def doTask(page):
    time.sleep(9 - page)
    print(f"crawl task{page} finished")
    return page

# pool = ThreadPoolExecutor(max_workers=2, thread_name_prefix='test_thread')
# # submit是非阻塞方法，提交一个函数到线程池中，返回一个 future 对象
# future1 = pool.submit(target_func, param)

# if __name__ == '__main__':
#     with ThreadPoolExecutor(max_workers=5) as t:
#         obj_list = []
#         for page in range(1, 8):
#             obj = t.submit(doTask, page)
#             obj_list.append(obj)
#
#         for future in as_completed(obj_list):
#             data = future.result()
#             print(f"main: {data}")

def run_task_callback(i):
    # https://blog.csdn.net/weixin_39916966/article/details/127387937
    # os.system() 默认是阻塞的，subprocess.Popen默认不阻塞
    # proc = subprocess.Popen(cmd_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # proc.wait()
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    print(f'{current_time} task{i} begin\n')
    # 这里使用sleep模拟wait的阻塞运行
    time.sleep(5)
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    print(f'{current_time} task{i} done')

# https://zhuanlan.zhihu.com/p/490353142
task = threading.Thread(target=run_task_callback, args=(1, ))
task.start()
# 从打印可以看出在子线程中调用system和Popen方法不会阻塞主线程，但是会阻塞当前进程
current_time = datetime.datetime.now().strftime("%H:%M:%S")
print(f'{current_time} wait for task finish')
