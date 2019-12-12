from tkinter import *

class CandySelection:
    def __init__(self):
        self.CANDY = {"M&Ms": .2, "Chocolate Almonds": .1875, "Skittles": .45}
        self.candySelectedRatio = 1
        self.candySelected = "No Candy Selected"

    def selectCandy(self, key):
        self.candySelectedRatio = self.CANDY[key]
        self.candySelected = key

    def getCandySelectedRatio(self):
        return self.candySelectedRatio

    def getCandySelected(self):
        return self.candySelected

def createBottons():
    master = Tk()
    candyInst = CandySelection()

    master.title("Candy Selection")
    master.geometry("300x150")

    #list of bottons
    buttons = []
    for key in candyInst.CANDY:
        #button = (Button(master, text=str(key), command=lambda a=k: doThis(a)))
        button = (Button(master, text=str(key), width = 15, command=lambda a=key: candyInst.selectCandy(a)))
        button.pack()
        buttons.append(button)

    confirm = Button(master, text="Submit", width=25, command=master.destroy)
    confirm.pack(side=BOTTOM)
    master.mainloop()
    return candyInst
    

if __name__ == "__main__":
    candyInst = createBottons()
    print(candyInst.getCandySelectedRatio())
    print(candyInst.getCandySelected())