import re
from functools import reduce


PUZZLE_INPUT = "235741-706948"


def input_to_bounds(input_str):
    bounds = input_str.split('-')
    return int(bounds[0]), int(bounds[1])


# password must contain two identical and adjacent numbers
def rule1(pw):
    return re.search(r"([0-9])\1", pw) != None


# the digits in the password never decrease left-to-right
def rule2(pw):
    return pw == ''.join(sorted(pw))


def password_valid(pw):
    pw = str(pw)
    return rule1(pw) and rule2(pw)


if __name__ == '__main__':
    lower, upper = input_to_bounds(PUZZLE_INPUT)
    valid_passwords = reduce(lambda x, y: password_valid(y) + x, range(lower, upper+1), 0)
    print("{} # of valid passwords".format(valid_passwords))