import os
# from flag import FLAG
from itertools import product

from Crypto.Cipher import AES

FLAG = b"hello"

DATA = os.urandom(8)
DATA_2 = "a355c8b253a6f0037c9cd331c8b4b5afb7198c944e56db549612942ceec05e8c"


# pads the message to a multiple of 16 bytes
def pad(msg):
    bytes_of_padding = (16 - len(msg)) % 16
    pad_bytes = bytes([bytes_of_padding])  # creates a single byte that has the numerical value of the number of bytes of padding you want
    # this padding scheme is called PKCS, don't worry about it, just know it pads the message to 16 bytes
    return msg + pad_bytes * bytes_of_padding


# strip the padding off
# don't worry about this function
def strip_padding(block):
    last = block[-1]
    if last < 16 and all([last == b for b in block[-1 * last:]]):
        # we have a padded msg, strip it off
        return block[:-1 * last]
    else:
        # no padding
        return block


def shuffle_using(xs, y):
    for i in range(0, len(xs), y):
        xs.append(xs.pop(i))
    return xs


def make_key():
    result = list(DATA_2)
    for secret in DATA:
        # FIXME: i got this to work by putting a mod here, will ask the security team to review after the weekend
        # but we gotta get this live so ill just push it to prod
        result = shuffle_using(result, secret % 7 + 1)
    key = "".join(result[:8])
    return bytes.fromhex(key)


def make_key_hack(data):
    result = list(DATA_2)
    for secret in data:
        result = shuffle_using(result, secret)
    key = "".join(result[:8])
    return bytes.fromhex(key)


def extend_key(key):
    return key * 8


def encrypt(key, message):
    key_one = key[:2]
    key_two = key[2:]

    key_one = extend_key(key_one)
    key_two = extend_key(key_two)

    c_one = AES.new(key_one, AES.MODE_ECB)
    c_two = AES.new(key_two, AES.MODE_ECB)

    return c_two.encrypt(c_one.encrypt(pad(message)))


def decrypt(key, message):
    key_one = key[:2]
    key_two = key[2:]

    key_one = extend_key(key_one)
    key_two = extend_key(key_two)

    c_one = AES.new(key_one, AES.MODE_ECB)
    c_two = AES.new(key_two, AES.MODE_ECB)

    return c_one.decrypt(c_two.decrypt(message))


encrypted_flag = bytes.fromhex("b8a363a95d83b3d13886dc97899844463d356fe030f67fa3681537a3d88e8966")

for combo in product(range(1, 8), repeat=8):
    decrypt_key = make_key_hack(bytes(combo))
    decrypted_flag = decrypt(decrypt_key, encrypted_flag)
    print(strip_padding(decrypted_flag), end="\033[2K\033[1G")

    if decrypted_flag.startswith(b"maple"):
        print(strip_padding(decrypted_flag).decode())
        break
