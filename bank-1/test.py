#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host bank-2.ctf.maplebacon.org --port 1337
from pwn import *

context.log_level = 50

# Set up pwntools for the correct architecture
context.update(arch="i386")
exe = "python3"

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or "bank-1.ctf.maplebacon.org"
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
gdbscript = '''
continue
'''.format(**locals())

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

import re

io = start(["challenge.py"])
io.recvuntil(b">")


def request_money(amt):
    io.sendline(b"2")
    io.recvuntil(b":")
    io.sendline(str(amt).encode())
    io.recvuntil(b"Your receipt: ")
    ctxt = io.recvline()
    io.recvuntil(b">")
    return ctxt


def send_money(sender_id, recipient_id, sender_pin, amount):
    io.sendline(b"1")
    io.recvuntil(b":")
    io.sendline(str(sender_id).encode())
    io.recvuntil(b":")
    io.sendline(str(recipient_id).encode())
    io.recvuntil(b":")
    io.sendline(str(sender_pin).encode())
    io.recvuntil(b":")
    io.sendline(str(amount).encode())
    io.recvuntil(b"Your receipt: ")
    ctxt = io.recvline()
    io.recvuntil(b">")
    return ctxt


ids = [111111111111, 11111111111, 1111111111, 111111111, 11111111, 1111111]
ADMIN_ID = 0
ctxts = [request_money(i) for i in ids]

for i in range(6):
    for j in range(10):
        print(ADMIN_ID * 10 + j, end="\033[1G")
        ctxt = send_money(0, ids[i], ADMIN_ID * 10 + j, 0)

        if ctxts[i][:32] == ctxt[:32]:
            ADMIN_ID = ADMIN_ID * 10 + j
            break

print(ADMIN_ID)
send_money(0, 1, ADMIN_ID, 100000000)
io.sendline(b"3")
print(re.search(r"maple\{[a-zA-Z0-9_!\-\?]+\}", io.recvline().decode())[0])
