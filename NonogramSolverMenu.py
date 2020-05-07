from tkinter import *  
import os
import NonogramSolverGUI as NSGUI

def solve():
    nonogram = hintsListbox.get(hintsListbox.curselection())
    to_solve = "hints/" + nonogram
    nGUI = NSGUI.MainWindow(nonogram)



if __name__ == "__main__":
    top = Tk()
    top.geometry("200x250")
    top.title("NonogramSolverMenu")
    path = "hints/"

    lbl = Label(top,text = "Wybierz obrazek logiczny z listy")
    lbl.pack()

    hintsListbox = Listbox(top)
    os.chdir(path)
    items = os.listdir()
    i = 1
    for item in items:
        hintsListbox.insert(i, item)
        i += 1
    hintsListbox.pack()


    button = Button(top, text="Rozwiąż obrazek logiczny", command = solve)
    button.pack()

    top.mainloop()