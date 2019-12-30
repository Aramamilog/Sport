import random
import string

def generate_name(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))