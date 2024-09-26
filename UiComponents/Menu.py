import tkinter as tk
import webbrowser


class Menu:

    def __init__(self, app):
        menubar = tk.Menu(app)

        self.add_menu(menubar, "Datei", [
            ["Neu", self.unimplemented_option],
            ["Speichern", self.unimplemented_option],
            ["Laden", self.unimplemented_option],
            ["Exit", exit]
        ])
        self.add_menu(menubar, "Bearbeiten", [
            ["Ausschneiden", self.unimplemented_option],
            ["Kopieren", self.unimplemented_option],
            ["Einfügen", self.unimplemented_option],
            ["Zurücksetzen", self.unimplemented_option]
        ])
        self.add_menu(menubar, "Hilfe", [
            ["Author", self.open_website],
            ["GitHub", self.open_github],
        ])

        app.config(menu=menubar)

    @staticmethod
    def add_menu(menubar, label: str, commands):
        menu = tk.Menu(menubar, tearoff=0)
        for command in commands:
            menu.add_command(label=command[0], command=command[1])

        menubar.add_cascade(label=label, menu=menu)

    @staticmethod
    def open_website():
        webbrowser.open("https://eike.in")

    @staticmethod
    def open_github():
        webbrowser.open("https://github.com/LarvenStein/Zeichenprogramm")

    @staticmethod
    def unimplemented_option():
        print("unimplemented")
