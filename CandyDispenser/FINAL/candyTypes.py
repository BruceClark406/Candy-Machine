class CandySelection:
    def __init__(self):
        self.CANDY = {"M&Ms": .2, "Chocolate Almonds": .1875}
        self.candySelectedRatio = 1
        self.candySelected = "No Candy Selected"

    def selectCandy(self):
        print("What candy would you like: (", end="")

        for treat in self.CANDY:
            lastTreat = treat

        for treat in self.CANDY:
            if treat == lastTreat:
                print(treat, end="")
            else:
                print(treat, end=", ")
                
        print(")")

        candyType = input()

        try:
            self.candySelectedRatio = self.CANDY[candyType]
            self.candySelected = candyType
        except:
            print("This is not a valid input, please try again...\n")
            self.selectCandy()

    def getCandySelectedRatio(self):
        return self.candySelectedRatio

    def getCandySelected(self):
        return self.candySelected

        

    
