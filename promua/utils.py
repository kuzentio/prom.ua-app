import string, random


def random_string(n):
    a = string.ascii_letters + string.digits
    return ''.join([random.choice(a) for i in range(n)])
