from pwn import *

context.log_level = 50


def unrotate(c, n):
    return (c - 32 - n) % 95 + 32


check_str = b"iqexvngduyvzfywdbshdizrhvnssvdjtre~szudzng|msjdtqffwzujcnpdkmlivf"

io = process(["./seedling"])
io.recvline()
io.sendline(b"0" * 65)
io.recvuntil(b"> ")

levels = [int(i) for i in io.recvline().decode()[:-1]]
print("maple{" + bytes(unrotate(check_str[i], levels[i]) for i in range(len(check_str))).decode() + "}")
io.close()
