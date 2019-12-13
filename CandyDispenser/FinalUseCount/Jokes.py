from joke.jokes import *

import random


def bruce():
    for i in range(1):
        choices = [geek, icanhazdad, chucknorris, icndb]
        r1 = random.randint(0, len(choices)-1)
        #select = choice([geek, icanhazdad, chucknorris, icndb])
        #print(select.__str__)
        joke=choices[r1]()
        print(r1)
        print(joke)
bruce()


