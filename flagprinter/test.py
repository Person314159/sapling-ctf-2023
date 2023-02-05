from pwn import *

context.log_level = 50
context.update(arch='amd64')
elf = ELF("./flagprinter")

# correct solution
elf.write(0x4009ce, asm("push rbp"))
elf.write(0x400b1f, asm("mov rsi, rax"))
elf.write(0x40f450, asm("ret"))
elf.save("flagprinter2")

# my very cheese, segfaults but the flag is on the stack at point of segfault
# elf.write(0x4009ce, asm("nop"))
# elf.write(0x40f44f, asm("ret"))

io = process(["./flagprinter2"])
print(re.search(r"maple\{[a-zA-Z0-9_!\-\?]+\}", io.recvall().decode())[0])
io.close()
