import tkinter as tk
import webbrowser
import json
import os
import tarfile
from tkinter.filedialog import asksaveasfile
from tkinter.filedialog import askopenfilename


class Menu:

    def __init__(self, app):
        menubar = tk.Menu(app)
        self.app = app

        self.add_menu(menubar, "Datei", [
            ["Neu", self.unimplemented_option],
            ["Speichern", self.save],
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
            ["Author", lambda:webbrowser.open("https://eike.in")],
            ["GitHub", lambda:webbrowser.open("https://github.com/LarvenStein/Zeichenprogramm")],
        ])

        app.config(menu=menubar)

    @staticmethod
    def add_menu(menubar, label: str, commands):
        menu = tk.Menu(menubar, tearoff=0)
        for command in commands:
            menu.add_command(label=command[0], command=command[1])

        menubar.add_cascade(label=label, menu=menu)

    def save(self):
        f = asksaveasfile(initialfile='Untitled.ezf',
                          defaultextension=".ezf", filetypes=[("Editable zeichenprogramm file", "*.ezf")])
        shapes_dict = []
        for shape in self.app.drawing_area.shapes:
            if shape.shape_type == "polygon":
                shape_data = {
                    "shape_type": shape.shape_type,
                    "points": shape.points,
                    "color": shape.color,
                    "fill": shape.fill
                }
            else:
                shape_data = {
                    "shape_type": shape.shape_type,
                    "x": shape.x,
                    "y": shape.y,
                    "width": shape.width,
                    "height": shape.height,
                    "color": shape.color,
                    "fill": shape.fill
                }
            shapes_dict.append(shape_data)

        json_data = json.dumps(shapes_dict)

        json_filename = "shapes.json"
        with open(json_filename, 'w') as json_file:
            json_file.write(json_data)

        with tarfile.open(f.name, "w") as tar:
            tar.add(json_filename, arcname=os.path.basename(json_filename))

        os.remove(json_filename)  # Clean up the temporary JSON file

    @staticmethod
    def unimplemented_option():
        print("unimplemented")
