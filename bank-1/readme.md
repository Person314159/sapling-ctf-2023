## `bank-1`
### Problem Description
- Author: Arctic
    - Based on the lead you gave us we've tracked down a secret exchange that we believe our suspects have been using.
    - There appears to be some special access that we need to purchase, but we can't use our funds without raising suspicion.
    - Can you find a way to redirect their funds into our account so we can gain access?
    - Guide: https://ctf.maplebacon.org/crypto_bank_1

### Solution
AES ECB mode has a very big weakness: **the same block of plaintext will always be encrypted using a given key to the same block of ciphertext**. The transaction ID format is `{sender_id}|{recipient_id}|{sender_pin}|{amount}`. Also, `request_money` includes the `ADMIN_PIN` as `sender_pin`, and we have control over the `recipient_id`...

Considering that the same plaintext is encoded to the same ciphertext, we can craft our `send_money/request_money` to decrypt the `ADMIN_PIN`, one digit at a time. For an overview of how this works, see [here](https://crypto.stackexchange.com/a/46928).

We first `request_money` for various different `recipient_id`s, so we can have the first plaintext blocks look like the following:

```
0|recipient_id|A
0|recipient_i|AD
0|recipient_|ADM
0|recipient|ADMI
0|recipien|ADMIN
0|recipie|ADMINP
```

Once we have the corresponding ciphertext for each of these, we can `send_money` to have full control over the `sender_pin`:

```
0|recipient_id|0 # does this encrypt to the same ciphertext as 0|recipient_id|A above?
0|recipient_id|1 # does this encrypt to the same ciphertext as 0|recipient_id|A above?
0|recipient_id|2 # does this encrypt to the same ciphertext as 0|recipient_id|A above?
...
```

This way, we can figure out the first digit of the `ADMIN_PIN`, and decipher the next digit using `0|recipient_i|AD`, etc etc.

We're given 100 attempts at `send_money/request_money` attempts, but we only need 6 + 60 = 66 in the worst case.

### Script
```python
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
```

### Flag: `maple{4LL_Y0UR_m0NEy_4Re_8eL0Ng_70_u2}`

<video width="1024" height="560" controls>
  <source src="./bank-1.mp4" type="video/mp4">
</video>