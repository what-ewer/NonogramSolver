
from tkinter import *
from tkinter import ttk

class NonogramMakerHints:

    def __init__(self, rows, cols, filename):
        self.rows = rows
        self.cols = cols
        self.solution = [[], []]
        self.filename = filename
        self.i = 0

        root = Tk()

        c = ttk.Frame(root, padding=(5, 5, 12, 0))
        c.grid(column=0, row=0, sticky=(N, W, E, S))
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)

        root.resizable(0, 0)
        self.root = root

        main_label = Label(root, text="Podaj po przecinku liczby dla wiersza 0")
        main_label.grid(column=0, row=0, rowspan=1, columnspan=3, pady=5, padx=5)
        self.main_label = main_label

        values = Entry(root)
        values.grid(column=5, row=3, rowspan=1, columnspan=2, pady=5, padx=5)
        self.values = values

        confirm_button = Button(root, text="OK", command=self.parseInput)
        confirm_button.grid(column=0, row=4, rowspan=2, columnspan=3, pady=5, padx=5)
        self.confirm_button = confirm_button

        root.mainloop()

    def parseInput(self):
        self.i += 1
        v = self.values.get()
        print(v)

        if self.i >= self.rows:
            txt = "Podaj po przecinku liczby dla kolumny "
            txt += str(self.i - 3)
            self.main_label = Label(self.root, text=txt)
            self.main_label.grid(column=0, row=0, rowspan=1, columnspan=3, pady=5, padx=5)
        else:
            txt = "Podaj po przecinku liczby dla wiersza "
            txt += str(self.i)
            self.main_label = Label(self.root, text=txt)
            self.main_label.grid(column=0, row=0, rowspan=1, columnspan=3, pady=5, padx=5)

        if not v:
            v = [0]
        else:
            v = v.split(", ")
            v = list(map(int, v))

        if self.i > self.rows:
            self.solution[1].append(v)
        else:
            self.solution[0].append(v)

        if self.i >= self.rows + self.cols:
            self.save()

    def save(self):
        f = open(self.filename, mode="w+", encoding="utf-8")
        f.write(str(self.solution))
        f.close()
        self.root.destroy()
