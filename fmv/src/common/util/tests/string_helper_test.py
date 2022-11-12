from common.util.string_helper import *


if __name__ == '__main__':

    print(hash256("this is a test"))

    l1 = hash256("this is d test", 8)
    l2 = hash256(l1, 8)
    l3 = hash256(l2, 8)

    print(l1, l2, l3)