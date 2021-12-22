# BEGIN SPINNER_ASYNCIO
import asyncio
import itertools
import sys


# 打算交给 asyncio 处理的协程要使用 @asyncio.coroutine 装饰。这不是强制要求，但强烈建议这么做。原因在后面说明
async def spin(msg):  # 这里不需要 关闭线程的 signal 函数
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status))
        try:
            await asyncio.sleep(.1)  # 使用 yield from asyncio.sleep(.1) 代替 time.sleep(.1)，这样的休眠不会阻塞事件循环
        except asyncio.CancelledError:  # 如果 spin 苏醒后抛出 asyncio.CancelledError 异常，其原因是发出了取消请求，因此退出循环
            break
    write(' ' * len(status) + '\x08' * len(status))


async def slow_function():  # 现在，slow_function 函数是协程，在用休眠假装进行 I/0 操作时，使用 yield from asyncio.sleep(3) 继续执行事件循环
    # pretend waiting a long time for I/O
    await asyncio.sleep(3)  # yield from asyncio.sleep(3) 表达式把控制权交给主循环，在休眠结束后回复这个协程
    return 42

async def supervisor():  # 现在，supervisor 函数也是协程，因此可以使用 yield from 驱动 slow_function 函数。
    spinner = asyncio.create_task(spin('thinking!'))  # loop.create_task(...) 函数排定 spin 协程的运行时间，使用一个 Task 对象包装 spin 协程，并立即返回
    print('spinner object:', spinner)  # 显示 Task 对象
    # 驱动 slow_function 函数，结束后，获取返回值。同时，事件循环继续运行，因为 slow_function 函数最后使用 yield from 表达式把控制权交回了主循环
    result = await slow_function()  
    spinner.cancel()  # Task 对象可以取消，取消后会在协程当前暂停的 yield 处抛出 asyncio.CancelledError 异常，协程可用捕获这个异常，也可以延迟取消，甚至拒绝取消
    return result


def main():
    loop = asyncio.get_event_loop()  # 获取事件循环的引用
    result = loop.run_until_complete(supervisor())  # 驱动 supervisor 协程，让它运行完毕；这个协程的返回值是这次调用的返回值
    loop.close()
    print('Answer:', result)


if __name__ == '__main__':
    main()
# END SPINNER_ASYNCIO