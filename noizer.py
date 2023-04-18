from math import log2, ceil
from random import randrange

def noizer(msg: str, mode: int) -> str:
    """
    Generates an error in each element of a Hamming encoded message
    """
    seq = list(map(int, msg))
    s_num = ceil(log2(log2(mode + 1) + mode + 1))  # количество служебных битов
    code_len = mode + s_num  # длина кодового слова
    cnt = len(msg) // code_len
    result = ""

    for i in range(cnt):
        to_noize = seq[i * code_len:i * code_len + code_len]
        noize = randrange(code_len)
        to_noize[noize] = int(not to_noize[noize])
        result += "".join(map(str, to_noize))

    return result


def noizer2(msg: str, mode: int) -> str:
    """
    Generates up to 2 errors in each fourth element of a Hamming encoded message
    """
    seq = list(map(int, msg))
    s_num = ceil(log2(log2(mode + 1) + mode + 1))  # количество служебных битов
    code_len = mode + s_num  # длина кодового слова
    cnt = len(msg) // code_len
    result = ""

    for i in range(0, cnt, 4):
        to_noize = seq[i * code_len:i * code_len + code_len]
        noize1 = randrange(code_len)
        noize2 = randrange(code_len)
        to_noize[noize1] = int(not to_noize[noize1])
        to_noize[noize2] = int(not to_noize[noize2])
        result += "".join(map(str, to_noize))

    return result