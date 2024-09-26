import tkinter as tk
from UiComponents.Menu import Menu


class InitApp:
    def __init__(self):
        app = tk.Tk()
        app.geometry("300x200")
        app.title("Zeichenprogramm")
        Menu(app)
        app.mainloop()


if __name__ == "__main__":
    InitApp()
