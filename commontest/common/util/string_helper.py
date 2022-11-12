import string
import random
import hashlib

start = 0


def get_random_value() -> str:
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(8))
    return result_str


def remove_underscore(input: str) -> int:
    return int(input.replace("_", ""))


def get_next_value() -> str:
    global start
    start += 1
    v = str(start)
    return 'Value_' + v


def get_next_int() -> str:
    global start
    start += 1
    return str(start)


def hash256(data: str, return_size: int = -1):

    unicoded = data.encode('utf-8')
    m = hashlib.sha256(unicoded)
    h = m.hexdigest()
    if return_size == -1:
        return h
    else:
        return h[0:return_size]

#>>> hashlib.sha256(str(random.getrandbits(256)).encode('utf-8')).hexdigest()