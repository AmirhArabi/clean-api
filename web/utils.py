import random
import string

class Shortener:
    token_size = 5
    def __init__(self):
        self.token_size = self.token_size if self.token_size is not None else 5

    def generate_token(self):
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for i in range(self.token_size))
