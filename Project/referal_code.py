import string
import random

def id_generator(id=0,size=6, chars=string.digits):
    code=''.join(random.choice(chars) for x in range(size+id))
    return int(code)

# print(id_generator())