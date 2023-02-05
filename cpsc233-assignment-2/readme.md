## `CPSC233 Assignment 2`
### Problem Description
- Author: aynakeya
    - CPSC233 Assignment 2 Instruction
    - In this assignment, you are going to apply your knowledge of syscalls.
    - Online Learning Resource:
        1. x64 assembly reference: http://6.s081.scripts.mit.edu/sp18/x86-64-architecture-guide.html
        2. Exploring assembly language: https://godbolt.org/
        3. x64 cheat sheet: https://cs.brown.edu/courses/cs033/docs/guides/x64_cheatsheet.pdf
        4. syscall table: https://chromium.googlesource.com/chromiumos/docs/+/HEAD/constants/syscalls.md

### Solution
Slightly more difficult, now we need to `read` the `fd` into a buffer, `write` it to `stdout`, then `close` the `fd`. 213/313 and the man pages pls help me

### Script:

```python
io = start()
your_asm_code_here = """
mov rax, 0      # read
sub rsp, 0x400  # allocate buffer on stack
mov rsi, rsp    # read arg
mov rdx, 1024   # read arg
syscall
mov rdx, rax    # read returns how many bytes is read, move this into arg for write
mov rax, 1      # write
mov r8, rdi     # save the fd so we can close it later
mov rdi, 1      # stdout
syscall
mov rdi, r8     # restore fd into rdi
mov rax, 3      # close
syscall
add rsp, 0x400  # restore stack
ret
"""
shellcode = asm(your_asm_code_here)
io.sendlineafter(b"here: ", shellcode.hex().encode())
io.recvline()
print(io.recvline().decode(), end="")
io.close()
```

### Flag: `maple{p21n71n9_1n_4445555mmmm}`