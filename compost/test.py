from pwn import *

context.log_level = 50

m = {}


def diff(s1, s2):
    for i, (a1, a2) in enumerate(zip(s1, s2)):
        if a1 != a2:
            return i

    return -1


normal_output = "0103003003030103003003030"
lst = ["0"] * 25

for i in range(25):
    lst[i] = "1"
    io = process(["./compost"])
    io.recvline()
    io.sendline("".join(lst).encode())
    output = io.recvline().decode()[2:-1]
    m[i] = diff(normal_output, output)
    lst[i] = "0"
    io.close()

lst = ["."] * 25
expected = "hglhhlbomrrw_nebedrcllpue"

for i in range(25):
    for j in range(33, 127):
        lst[i] = chr(j)
        io = process(["./compost"])
        io.recvline()
        io.sendline("".join(lst).encode())
        output = io.recvline().decode()[2:-1]
        print("".join(lst), end="\033[1G")
        io.close()

        if len(output) != 25:
            continue

        if output[m[i]] == expected[m[i]]:
            break

print("".join(lst))
