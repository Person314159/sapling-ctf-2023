from pwn import *

context.log_level = 50


def trace(msg):
    io = process(["./art"])
    io.sendline(msg)
    lst = []

    for i in range(6):
        lst.append(io.recvline()[:-1])

    lst[0] = lst[0][2:]
    io.close()
    return lst


flag = b"maple{" + b"." * 29 + b"}"
lst = list(flag)
expected = [i.encode() for i in open("art.txt").read().splitlines()]


def diff(output, expected, i):
    for row in range(6):
        for idx in range(4 * i + 1, 4 * (i + 1) + 1):
            if output[row][-idx] != expected[row][-idx]:
                return row, idx, i

    return 0


for i in range(6, 35):
    for j in range(33, 127):
        lst[i] = j
        output = trace(bytes(lst))
        print(bytes(lst).decode(), end="\033[1G")

        if not diff(output, expected, i):
            break

print(bytes(lst).decode())
