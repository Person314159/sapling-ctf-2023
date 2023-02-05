from pwn import *

context.log_level = 50

flag = "maple{" + " " * 18 + "}"
lst = list(flag)


def trace(s):
    io = process(["ltrace", "./dyn", s])
    io.recvlines(3)
    output = io.recvline()
    io.close()
    return output.decode().split()[-1]


for i in range(6, 23):
    for j in range(32, 127):
        lst[i] = chr(j)
        output = trace("".join(lst))
        print("".join(lst), end="\033[1G")
        old = lst[i + 1]
        lst[i + 1] = "."
        output2 = trace("".join(lst))

        if output2 != output:
            lst[i + 1] = old
            break

        lst[i + 1] = old

for j in range(32, 127):
    lst[23] = chr(j)
    output = trace("".join(lst))

    if output == "0":
        break

    print("".join(lst), end="\033[1G")

print("".join(lst))
