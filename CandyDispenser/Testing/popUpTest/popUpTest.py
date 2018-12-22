import tkinter as tk
from tkinter import ttk

def popUpNotification(calories):

    widthOfPopup = 600
    heightOfPopup = 200

    popup = tk.Tk()
    popup.wm_title("Calorie Kill Count")
    output = ("You are about to consume %s calaries!" % (calories))
    label = ttk.Label(popup, text=output, font = ("Verdana", 12))
    label.pack(side="top", fill="x", padx=20, pady=20)

    #after 3 second destroy the alert

    widthOfScreen = (popup.winfo_screenwidth() /2) - (widthOfPopup/2)
    heightOfScreen = (popup.winfo_screenheight() /2) - (heightOfPopup/2)

    popup.after(3000, lambda: popup.destroy())
    popup.geometry("%dx%d+%d+%d" % (widthOfPopup, heightOfPopup, widthOfScreen, heightOfScreen))
    popup.mainloop()


if __name__ == "__main__":
    popUpNotification(str(4))
