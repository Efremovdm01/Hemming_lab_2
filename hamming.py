from typing import List
from math import log2, ceil


def __hamming_common(src: List[List[int]], s_num: int, encode=True) -> int:
    s_range = range(s_num)
    errors = 0

    for i in src:
        sindrome = 0
        for s in s_range:
            sind = 0
            for p in range(2 ** s, len(i) + 1, 2 ** (s + 1)):
                for j in range(2 ** s):
                    if (p + j) > len(i):
                        break
                    sind ^= i[p + j - 1]

            if encode:
                i[2 ** s - 1] = sind
            else:
                sindrome += (2 ** s * sind)

        if (not encode) and sindrome:
            try:
                i[sindrome - 1] = int(not i[sindrome - 1])
            except IndexError:
                errors += 1

    return errors


def hamming_encode(msg: str, mode: int = 8) -> str:
    """
    Encoding the message with Hamming code.
    :param msg: Message string to encode
    :param mode: number of significant bits
    :return:
    """

    result = ""
    msg_b = msg.encode("utf8")
    s_num = ceil(log2(log2(mode + 1) + mode + 1))  # number of control bits
    bit_seq = []
    for byte in msg_b:  # get bytes to binary values; every bits store to sublist
        bit_seq += list(map(int, f"{byte:08b}"))

    res_len = ceil((len(msg_b) * 8) / mode)  # length of result (bytes)
    bit_seq += [0] * (res_len * mode - len(bit_seq))  # filling zeros

    to_hamming = []

    for i in range(res_len):  # insert control bits into specified positions
        code = bit_seq[i * mode:i * mode + mode]
        for j in range(s_num):
            code.insert(2 ** j - 1, 0)
        to_hamming.append(code)

    errors = __hamming_common(to_hamming, s_num, True)  # process

    for i in to_hamming:
        result += "".join(map(str, i))

    return result


def hamming_decode(msg: str, mode: int = 8):
    """
    Decoding the message with Hamming code.
    :param msg: Message string to decode
    :param mode: number of significant bits
    :return:
    """

    result = ""

    s_num = ceil(log2(log2(mode + 1) + mode + 1))  # number of control bits
    res_len = len(msg) // (mode + s_num)  # length of result (bytes)
    code_len = mode + s_num  # length of one code sequence

    to_hamming = []

    for i in range(res_len):  # convert binary-like string to int-list
        code = list(map(int, msg[i * code_len:i * code_len + code_len]))
        to_hamming.append(code)

    errors = __hamming_common(to_hamming, s_num, False)  # process

    for i in to_hamming:  # delete control bits
        for j in range(s_num):
            i.pop(2 ** j - 1 - j)
        result += "".join(map(str, i))

    msg_l = []

    for i in range(len(result) // 8):  # convert from binary-sring value to integer
        val = "".join(result[i * 8:i * 8 + 8])
        msg_l.append(int(val, 2))

    try:
        result = bytes(msg_l).decode("utf8")
    except UnicodeDecodeError:
        pass

    return result, errors