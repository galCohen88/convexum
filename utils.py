import random
import string


def random_str(len=7):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(len))
