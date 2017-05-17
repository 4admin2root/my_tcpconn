# coding=utf-8
import time
import random


def fib(n):
    index = 0
    a = 0
    b = 1
    while index < n:
        sleep_cnt = yield b
        print('let me think {0} secs'.format(sleep_cnt))
        time.sleep(sleep_cnt)
        a, b = b, a + b
        index += 1


def main():
    n = 5
    sfib = fib(n)
    fib_res = sfib.next()
    while True:
        print(fib_res)
        try:
            fib_res = sfib.send(random.uniform(0, 5))
        except StopIteration:
            break


if __name__ == '__main__':
    main()


