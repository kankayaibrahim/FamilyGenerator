import random
from random import randint

def erkek_boy_araligi_kaydet():
    mean = 177
    stdev = 7
    values = []
    while len(values) < 100_000:
        sample = random.gauss(mean, stdev)
        if sample >= 140 and sample < 200:
            values.append(int(sample))

    textfile = open("erkek_boy_uzunlugu.txt", "w")
    for element in values:
        textfile.write(str(element) + "\n")
    textfile.close()


def kadin_boy_araligi_kaydet():
    mean = 164
    stdev = 7
    values = []
    while len(values) < 100_000:
        sample = random.gauss(mean, stdev)
        if sample >= 140 and sample < 200:
            values.append(int(sample))

    textfile = open("kadin_boy_uzunlugu.txt", "w")
    for element in values:
        textfile.write(str(element) + "\n")
    textfile.close()


def erkek_kilo_araligi_kaydet():
    mean = 77
    stdev = 7
    values = []
    while len(values) < 100_000:
        sample = random.gauss(mean, stdev)
        if sample >= 48 and sample < 150:
            values.append(sample)

    textfile = open("erkek_kilo.txt", "w")
    for element in values:
        textfile.write(str(int(element)) + "\n")
    textfile.close()


def kadin_kilo_araligi_kaydet():
    mean = 68
    stdev = 9
    values = []
    while len(values) < 100_000:
        sample = random.gauss(mean, stdev)
        if sample >= 36 and sample < 150:
            values.append(sample)

    textfile = open("kadin_kilo.txt", "w")
    for element in values:
        textfile.write(str(int(element)) + "\n")
    textfile.close()


def get_male_random_weight() -> int:
    return int(random.choice(list(open('erkek_kilo.txt'))))


def get_male_random_height() -> int:
    return int(random.choice(list(open('erkek_boy_uzunlugu.txt'))))


def get_female_random_weight() -> int:
    return int(random.choice(list(open('kadin_kilo.txt'))))


def get_female_random_height() -> int:
    return int(random.choice(list(open('kadin_boy_uzunlugu.txt'))))

def get_random_tckn():
    tcno = str(randint(100000000, 1000000000))
    list_tc = list(map(int, tcno))
    tc10 = (sum(list_tc[::2]) * 7 - sum(list_tc[1::2])) % 10
    new_tc = tcno + str(tc10) + str((sum(list_tc[:9]) + tc10) % 10)
    return new_tc


# erkek_boy_araligi_kaydet()
# kadin_boy_araligi_kaydet()
# erkek_kilo_araligi_kaydet()
# kadin_kilo_araligi_kaydet()
# x = get_random_tckn()
# print(x)