from joke.jokes import *

import random

def get_joke():
        choices = [geek, icanhazdad, chucknorris, icndb]
        r1 = random.randint(0, len(choices)-1)
        joke=choices[r1]()
        return joke

if __name__ == "__main__":
    print(get_joke())


