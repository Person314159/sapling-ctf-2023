#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host cpsc233-assignment1.ctf.maplebacon.org --port 1337
from pwn import *

context.log_level = 50

# Set up pwntools for the correct architecture
exe = ELF("cpsc233_a1")
context.binary = exe
path = "./cpsc233_a1"

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or "cpsc233-assignment1.ctf.maplebacon.org"
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
your_asm_code_here = """
 add    edi,esi
 lea    eax,[rdi+rdx*1]
 ret
"""
shellcode = asm(your_asm_code_here)
io.sendlineafter(b"here: ", shellcode.hex().encode())
io.recvuntil(b"here is your flag: ")
print(io.recvline().decode(), end="")
io.close()
