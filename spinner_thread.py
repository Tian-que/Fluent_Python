# spinner_thread.py

# credits: Adapted from Michele Simionato's
# multiprocessing example in the python-list:
# https://mail.python.org/pipermail/python-list/2009-February/538048.html

# BEGIN SPINNER_THREAD
import threading
import itertools
import time
import sys

class Signal:   # 定义一个简单的可变对象；其中有个 go 属性，用于从外部控制线程
    go = True

def spin(msg, singnal):  # 这个函数会在单独的线程中运行。signal 参数是 Signal 类的实例
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):  # 这其实是个无限循环，char 一直在几个字符间来回变
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status))  # 使用退格符把光标移回来以显示动画
        time.sleep(1)
        if not singnal.go:  # 如果 go 的属性不是 True，就退出循环
            break
    write(' ' * len(status) + '\x08' * len(status))  # 使用空格清除状态信息，把光标移回开头


def slow_function():  # 假设这是耗时的计算
    # 假装等待 I/0 一段时间
    time.sleep(3)  # 调用 sleep 会阻塞主线程，不过一定要这么做，以便释放 GIL，创建从属线程
    return 42


def supervisor():  # 这个函数设置从属线程，显示线程对象，运行耗时的计算，最后杀死线程
    signal = Signal()
    spinner = threading.Thread(target=spin,
                               args=('thinking!', signal))
    print('spinner object:', spinner)  # 显示从属线程对象
    spinner.start()  # 启动从属线程
    result = slow_function()  # 运行 slow_function 函数，阻塞主线程；同时，从属线程以动画的形式旋转指针。
    signal.go = False  # 改变 signal 的状态；这会终止 spin 函数中的 for 循环
    spinner.join()  # 等待 spinner 线程结束
    return result


def main():
    result = supervisor()  # 运行 supervisor 函数
    print('Answer:', result)


if __name__ == '__main__':
    main()
# END SPINNER_THREAD
