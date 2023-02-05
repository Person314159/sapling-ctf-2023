import re

from Crypto.Cipher import AES

key = "1666b7e028d54f193895dbc3bddba88a"
cipher = AES.new(bytes.fromhex(key), AES.MODE_ECB)

with open("messages.txt") as f:
    for i in f.readlines():
        msg = bytes.fromhex(i[3:-1])
        match = re.search(r"maple\{[a-zA-Z0-9_!\-\?]+\}", cipher.decrypt(msg).decode())

        if match:
            print(match[0])
            break
