import tkinter as tk
from UiComponents.Menu import Menu
from UiComponents.ShapeLibrary import ShapeLibrary
from UiComponents.DrawingArea import DrawingArea
from tkinter import ttk


class InitApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("900x900")
        self.title("Zeichenprogramm")
        Menu(self)

        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.drawing_area = DrawingArea(app=self, master=main_frame, bg="white")

        ShapeLibrary(app=self, main_frame=main_frame, drawing_area=self.drawing_area)

        self.mainloop()


if __name__ == "__main__":
    InitApp()
