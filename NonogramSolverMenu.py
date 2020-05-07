from tkinter import *
from tkinter import ttk
import os
import NonogramSolverGUI as NSGUI
import NonogramMakerImage as NMI
import NonogramMakerHints as NMH

def refreshHintbox():
    items = os.listdir()
    for item in items:
        if item not in hintsListbox.get(0, "end"):
            hintsListbox.insert(hintsListbox.size(), item)

def solve():
    nonogram = hintsListbox.get(hintsListbox.curselection())
    NSGUI.MainWindow(nonogram)

def makeFromHints():
    w = int(widthSize.get())
    h = int(heightSize.get())
    name = nonogramName.get()

    NMH.NonogramMakerHints(h, w, name)
    print("Tworzenie obrazku logicznego o wymiarach ", w, " x ", h)

def makeFromImage():
    w = int(widthSize.get())
    h = int(heightSize.get())
    name = nonogramName.get()

    NMI.MainWindow(w, h, name)
    print("Tworzenie obrazku logicznego o wymiarach ", w, " x ", h)

if __name__ == "__main__":
    root = Tk()

    c = ttk.Frame(root, padding=(5, 5, 12, 0))
    c.grid(column=0, row=0, sticky=(N, W, E, S))
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    root.resizable(0, 0)

    root.title("NonogramSolverMenu")

    listLabel = Label(root, text="Wybierz obrazek logiczny z listy")
    listLabel.grid(column=0, row=0, rowspan=1, columnspan=3, pady=5, padx=5)

    hintsListbox = Listbox(root)
    path = "hints/"
    os.chdir(path)
    items = os.listdir()
    i = 1
    for item in items:
        hintsListbox.insert(i, item)
        i += 1

    hintsListbox.grid(column=0, row=1, rowspan=3, columnspan=3, pady=5, padx=5)

    solveButton = Button(root, text="Rozwiąż obrazek logiczny", command=solve)
    solveButton.grid(column=0, row=4, rowspan=2, columnspan=3, pady=5, padx=5)

    refreshHintboxButton = Button(root, text="Refresh", command=refreshHintbox)
    refreshHintboxButton.grid(column=3, row=0, rowspan=1, columnspan=1, pady=5, padx=5)

    makeNonogramLabel = Label(root, text="Utwórz swój obrazek logiczny")
    makeNonogramLabel.grid(column=3, row=0, rowspan=1, columnspan=3, pady=5, padx=5)

    sizeLabel = Label(root, text="Podaj wymiary obrazka")
    sizeLabel.grid(column=3, row=1, rowspan=1, columnspan=2, pady=5, padx=5)

    nameLabel = Label(root, text="Podaj nazwę obrazka")
    nameLabel.grid(column=5, row=1, rowspan=1, columnspan=2, pady=5, padx=5)

    wLabel = Label(root, text="WYSOKOŚĆ")
    wLabel.grid(column=3, row=2, rowspan=1, columnspan=1, pady=5, padx=5)

    hLabel = Label(root, text="SZEROKOŚĆ")
    hLabel.grid(column=4, row=2, rowspan=1, columnspan=1, pady=5, padx=5)

    nLabel = Label(root, text="NAZWA OBRAZKA")
    nLabel.grid(column=5, row=2, rowspan=1, columnspan=1, pady=5, padx=5)

    heightSize = Entry(root)
    heightSize.grid(column=3, row=3, rowspan=1, columnspan=1, pady=5, padx=5)

    widthSize = Entry(root)
    widthSize.grid(column=4, row=3, rowspan=1, columnspan=1, pady=5, padx=5)

    nonogramName = Entry(root)
    nonogramName.grid(column=5, row=3, rowspan=1, columnspan=2, pady=5, padx=5)

    createHints = Button(root, text="Utwórz z użyciem wskazówek", command=makeFromHints)
    createHints.grid(column=3, row=4, rowspan=2, columnspan=1, pady=5, padx=5)

    createImage = Button(root, text="Utwórz wykonując obrazek", command=makeFromImage)
    createImage.grid(column=4, row=4, rowspan=2, columnspan=1, pady=5, padx=5)


    root.mainloop()