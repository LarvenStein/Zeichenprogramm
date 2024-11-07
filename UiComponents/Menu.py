import tkinter as tk
import webbrowser
import json
import os
import tarfile
from tkinter.filedialog import asksaveasfile
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import askyesno

from Objects.Shape import Shape
from Objects.Polygon import Polygon

class Menu:

    def __init__(self, app):
        menubar = tk.Menu(app)
        self.app = app

        self.add_menu(menubar, "Datei", [
            ["Neu", self.unimplemented_option],
            ["Speichern", self.save],
            ["Laden", self.open],
            ["Exit", exit]
        ])
        self.add_menu(menubar, "Bearbeiten", [
            ["Ausschneiden", self.unimplemented_option],
            ["Kopieren", self.unimplemented_option],
            ["Einfügen", self.unimplemented_option],
            ["Zurücksetzen", self.reset]
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

    def reset(self):
        if(askyesno("Canvas wirklich leeren?", "Möchten Sie wirklich den Canvas leeren? Dies kann nicht rückgängig gemacht werden")):
            self.app.drawing_area.shapes = []
            self.app.drawing_area.draw_shapes()

    def open(self):
        f = askopenfilename(defaultextension=".ezf", filetypes=[("Editable zeichenprogramm file", "*.ezf")])
        with tarfile.open(f, "r") as tar:
            tar.extractall()

        json_filename = "shapes.json"
        with open(json_filename, 'r') as json_file:
            json_data = json_file.read()

        shapes_list = json.loads(json_data)
        self.app.drawing_area.shapes = []
        for shape_data in shapes_list:
            if shape_data["shape_type"] == "polygon":
                shape = Polygon(shape_data["points"], shape_data["color"], shape_data["fill"])
            else:
                shape = Shape(
                    shape_data["shape_type"],
                    shape_data["x"],
                    shape_data["y"],
                    shape_data["width"],
                    shape_data["height"],
                    shape_data["color"]
                )
                shape.fill = shape_data["fill"]
            self.app.drawing_area.shapes.append(shape)
        self.app.drawing_area.draw_shapes()
        os.remove(json_filename)

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
