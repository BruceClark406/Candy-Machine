from joke.jokes import *

import random

def get_joke():
        #choices = [geek, icanhazdad, chucknorris, icndb]
        choices = [icanhazdad, icanhazdad]
        r1 = random.randint(0, len(choices)-1)
        joke=choices[r1]()
        if "â" in joke:
            joke = joke.replace("â", "'")
        return joke

if __name__ == "__main__":
    print(get_joke())


