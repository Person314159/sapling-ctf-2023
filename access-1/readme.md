## `access-1`
### Problem Description
- Author: Arctic
    - Good job finding the secret bank exchange that APT-74 has been using, our next step will be to gain access and infiltrate their operations.
    - We sent an operative to attempt to gain access and they were told they needed decrypt their message to gain access. Luckily for you they also managed to snag a copy of the source code used to generate the key and message.
    - Do you think you can figure out what the key is?

### Solution
First thing to note is that even though `DATA` is 8 bytes/32 bits, the effective bitsize is actually 7, because of the `secret % 7`. So we can just brute force all 7^8 possible `DATA` until we get the right one.

```python
def make_key_hack(data):
    result = list(DATA_2)
    for secret in data:
        result = shuffle_using(result, secret)
    key = "".join(result[:8])
    return bytes.fromhex(key)

encrypted_flag = bytes.fromhex("b8a363a95d83b3d13886dc97899844463d356fe030f67fa3681537a3d88e8966")

for combo in product(range(1, 8), repeat=8):
    decrypt_key = make_key_hack(bytes(combo))
    decrypted_flag = decrypt(decrypt_key, encrypted_flag)
    print(strip_padding(decrypted_flag), end="\033[2K\033[1G")

    if decrypted_flag.startswith(b"maple"):
        print(strip_padding(decrypted_flag).decode())
        break
```

### Flag: `maple{N0T_3N0U9H_81T5!}`