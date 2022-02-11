import random


def gen_bload_group() -> list:
    bload_a = 'A'*45
    bload_b = 'B'*16
    bload_0 = '0'*33
    bload_ab = 'AB,'*6
    bload_ab_list = bload_ab.split(',')
    bload_ab_list.pop()
    bload_group_list = list(bload_a) + list(bload_b) + list(bload_0) + bload_ab_list
    random.shuffle(bload_group_list)
    return bload_group_list


def get_random_bload_group():
    return random.choice(gen_bload_group())
