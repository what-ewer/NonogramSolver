from tkinter import *
from tkinter import ttk
import os
import NonogramSolverGUI as NSGUI
import NonogramMakerImage as NMI

def solve():
    nonogram = hintsListbox.get(hintsListbox.curselection())
    NSGUI.MainWindow(nonogram)

def makeFromHints():
    w = int(widthSize.get())
    h = int(heightSize.get())
    print("Tworzenie obrazku logicznego o wymiarach ", w, " x ", h)

def makeFromImage():
    w = int(widthSize.get())
    h = int(heightSize.get())
    NMI.MainWindow(w,h)
    print("Tworzenie obrazku logicznego o wymiarach ", w, " x ", h)

if __name__ == "__main__":
    root = Tk()

    c = ttk.Frame(root, padding=(5, 5, 12, 0))
    c.grid(column=0, row=0, sticky=(N,W,E,S))
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0,weight=1)

    root.geometry("525x275")
    root.resizable(0, 0)

    root.title("NonogramSolverMenu")

    listLabel = Label(root,text = "Wybierz obrazek logiczny z listy")
    listLabel.grid(column=0, row=0, rowspan = 1, columnspan = 2, pady=5, padx = 5)

    hintsListbox = Listbox(root)
    path = "hints/"
    os.chdir(path)
    items = os.listdir()
    i = 1
    for item in items:
        hintsListbox.insert(i, item)
        i += 1

    hintsListbox.grid(column=0, row=1, rowspan = 3, columnspan = 2, pady=5, padx = 5)

    solveButton = Button(root, text="Rozwiąż obrazek logiczny", command = solve)
    solveButton.grid(column=0, row=4, rowspan = 2, columnspan = 2, pady=5, padx = 5)

    makeNonogramLabel = Label(root,text = "Utwórz swój obrazek logiczny")
    makeNonogramLabel.grid(column=2, row=0, rowspan = 1, columnspan = 2, pady=5, padx = 5)

    sizeLabel = Label(root,text = "Podaj wymiary obrazka")
    sizeLabel.grid(column=2, row=1, rowspan = 1, columnspan = 2, pady=5, padx = 5)

    wLabel = Label(root,text = "WYSOKOŚĆ")
    wLabel.grid(column=2, row=2, rowspan = 1, columnspan = 1, pady=5, padx = 5)

    hLabel = Label(root,text = "SZEROKOŚĆ")
    hLabel.grid(column=3, row=2, rowspan = 1, columnspan = 1, pady=5, padx = 5)

    widthSize = Entry(root)
    widthSize.grid(column=2, row=3, rowspan = 1, columnspan = 1, pady=5, padx = 5)

    heightSize = Entry(root)
    heightSize.grid(column=3, row=3, rowspan = 1, columnspan = 1, pady=5, padx = 5)

    createHints = Button(root, text="Utwórz z użyciem wskazówek", command = makeFromHints)
    createHints.grid(column=2, row=4, rowspan = 2, columnspan = 1, pady=5, padx = 5)

    createImage = Button(root, text="Utwórz wykonując obrazek", command = makeFromImage)
    createImage.grid(column=3, row=4, rowspan = 2, columnspan = 1, pady=5, padx = 5)


    root.mainloop()