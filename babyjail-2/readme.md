## `babyjail-2`
### Problem Description
- Author: desp
    - grats on becoming a free baby! too bad you are instantly caught again :(
    - at least only 2 lines of coded were added this time - surely it's not gonna be that bad right?
    - to deploy the local testing docker, run the following in the directory with both of the provided files:
    - sudo docker build . --tag babyjail2
    - sudo docker run --rm -it -t babyjail2

### Solution
The flag is stored in the code file, but we can't `cat` it to terminal anymore, since only root has read/write access. So unfortunately we have to somehow retrieve the flag from within the interactive Python console. But there's a pesky `del flag`, so we can't just `print(flag)`. However, the fact that this flag is `del`'d gives us an idea...why don't we use Python's garbage collector?

### Script
```python
import re

io = start(["babyjail-2.py"])
io.sendlineafter(b">>> ", b"import gc;print(gc.get_objects()); exit()")
print(re.search(r"maple\{[a-zA-Z0-9_!\-\?]+\}", io.recvall().decode())[0])
io.close()
```

### Flag: `maple{gc_0r_m3m_dump?}`