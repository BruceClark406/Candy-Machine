from tkinter import *

class CandySelection:
    def __init__(self):
        self.CANDY = {"M&Ms": .2, "Chocolate Almonds": .1875}
        self.candySelectedRatio = 1
        self.candySelected = "No Candy Selected"

    def setCandy(self, key):
        self.candySelectedRatio = self.CANDY[key]
        self.candySelected = key

    def getCandySelectedRatio(self):
        return self.candySelectedRatio

    def getCandySelected(self):
        return self.candySelected

    def selectCandy(self):
        master = Tk()

        master.title("Candy Selection")
        master.geometry("300x150")

        #list of buttons
        buttons = []
        for key in self.CANDY:
            button = (Button(master, text=str(key), width = 15, command=lambda a=key: self.setCandy(a)))
            button.pack()
            buttons.append(button)

        confirm = Button(master, text="Submit", width=25, command=master.destroy)
        confirm.pack(side=BOTTOM)
        master.mainloop()



        

    
