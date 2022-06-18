from random import choice
from string import ascii_letters as ASCII_LETTERS
from string import digits as DIGITS


def clamp(num, min_val, max_val):  # credit to paxdiablo on StackOverflow
    if num <= min_val:
        return min_val
    if num >= max_val:
        return max_val
    return num


def unbiasedRandomChoice(data: list):
    choice1 = choice(data)
    choice2 = choice(data)
    while choice1 == choice2:
        choice1 = choice(data)
        choice2 = choice(data)
    return choice1


def randOp(a, b):
    if unbiasedRandomChoice([True, False]):
        return a + b
    else:
        return a - b


def avg(data: list): return sum(data)/len(data)


def generateRandomAlphanumericString(length: int) -> str:
    letters = [i for i in ASCII_LETTERS]
    numbers = [str(i) for i in DIGITS]
    combined = letters + numbers
    string = []
    for _ in range(length):
        string.append(unbiasedRandomChoice(combined))
    return "".join(string)