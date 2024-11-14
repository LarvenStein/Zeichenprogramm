import tkinter as tk
import webbrowser
import json
import os
import tarfile
from tkinter.filedialog import asksaveasfile, asksaveasfilename
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import askyesno
from Objects.Shape import Shape
from Objects.Polygon import Polygon



class Menu:

    def __init__(self, app):
        menubar = tk.Menu(app)
        self.app = app
        self.app.bind("<Control-c>", self.copy)
        self.app.bind("<Control-x>", self.cut)
        self.app.bind("<Control-v>", self.paste)
        self.app.bind("<Control-s>", self.save)
        self.app.bind("<Control-n>", self.reset)
        self.app.bind("<Control-o>", self.open)
        self.app.bind("<Control-e>", self.export)
        self.app.bind("<Delete>", self.delete)

        self.add_menu(menubar, "Datei", [
            ["Neu", self.reset, "Strg+N"],
            ["Speichern", self.save, "Srg+S"],
            ["Exportieren", self.export, "Strg+E"],
            ["Laden", self.open, "Strg+O"],
            ["Exit", exit, None]
        ])
        self.add_menu(menubar, "Bearbeiten", [
            ["Entfernen", self.delete, "Entf"],
            ["Ausschneiden", self.cut, "Srg+X"],
            ["Kopieren", self.copy, "Strg+C"],
            ["Einfügen", self.paste, "Strg+V"],
            ["Zurücksetzen", self.reset, "Strg+N"]
        ])
        self.add_menu(menubar, "Hilfe", [
            ["Author", lambda: webbrowser.open("https://eike.in"), None],
            ["GitHub", lambda: webbrowser.open("https://github.com/LarvenStein/Zeichenprogramm"), None],
        ])

        app.config(menu=menubar)

        self.pasted_shapes = []
        self.saved_path = None

    @staticmethod
    def add_menu(menubar, label: str, commands):
        menu = tk.Menu(menubar, tearoff=0)
        for command in commands:
            menu.add_command(label=command[0], command=command[1], accelerator=command[2])

        menubar.add_cascade(label=label, menu=menu)

    def cut(self, event=None):
        self.copy()
        self.delete()

    def delete(self, event=None):
        self.app.drawing_area.shapes = [obj for obj in self.app.drawing_area.shapes if
                                        obj not in self.app.drawing_area.selected_shapes]
        self.app.drawing_area.draw_shapes()

    def copy(self, event=None):
        self.app.clipboard_clear()
        self.app.clipboard_append(self.objects_to_json(self.app.drawing_area.selected_shapes))
        self.app.update()

    def paste(self, event=None):
        json_data = self.app.clipboard_get()
        self.pasted_shapes.append(json_data)
        offset = self.pasted_shapes.count(json_data) * 10

        pasted_shapes = self.json_to_objects(json_data, offset=offset)
        self.app.drawing_area.shapes += pasted_shapes
        self.app.drawing_area.draw_shapes()

    def reset(self, event=None):
        if (askyesno("Canvas wirklich leeren?",
                     "Möchten Sie wirklich den Canvas leeren? Dies kann nicht rückgängig gemacht werden")):
            self.app.drawing_area.shapes = []
            self.app.drawing_area.draw_shapes()

    def open(self, event=None):
        f = askopenfilename(defaultextension=".ezf", filetypes=[("Editable zeichenprogramm file", "*.ezf")])
        with tarfile.open(f, "r") as tar:
            tar.extractall()

        json_filename = "shapes.json"
        with open(json_filename, 'r') as json_file:
            json_data = json_file.read()

        self.app.drawing_area.shapes = self.json_to_objects(json_data)

        self.app.drawing_area.draw_shapes()
        os.remove(json_filename)

    def save(self, event=None):
        file_name = self.saved_path
        if self.saved_path is None:
            file_name = asksaveasfile(initialfile='Untitled.ezf',
                                      defaultextension=".ezf",
                                      filetypes=[("Editable zeichenprogramm file", "*.ezf")]).name

        json_data = self.objects_to_json(self.app.drawing_area.shapes)

        json_filename = "shapes.json"
        with open(json_filename, 'w') as json_file:
            json_file.write(json_data)

        with tarfile.open(file_name, "w") as tar:
            tar.add(json_filename, arcname=os.path.basename(json_filename))

        os.remove(json_filename)  # Clean up the temporary JSON file

        self.saved_path = file_name

    def export(self, event=None):
        filename = asksaveasfilename(defaultextension=".png",
                                     filetypes=[("JPEG files", "*.jpg *.jpeg"),
                                                ("Bitmap files", "*.bmp"),
                                                ("WebP files", "*.webp"),
                                                ("GIF files", "*.gif"),
                                                ("PNG files", "*.png")])

        if filename:
            self.app.drawing_area.export_canvas_as_image(filename)

    @staticmethod
    def unimplemented_option():
        print("unimplemented")

    @staticmethod
    def objects_to_json(objects):
        shapes_dict = []
        for shape in objects:
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

        return json.dumps(shapes_dict)

    @staticmethod
    def json_to_objects(json_data, offset=0):
        shapes = []
        shapes_list = json.loads(json_data)
        for shape_data in shapes_list:
            if shape_data["shape_type"] == "polygon":
                points = []
                for point in shape_data["points"]:
                    point += offset
                    points.append(point)

                shape = Polygon(points, shape_data["color"], shape_data["fill"])
            else:
                shape = Shape(
                    shape_data["shape_type"],
                    shape_data["x"] + offset,
                    shape_data["y"] + offset,
                    shape_data["width"],
                    shape_data["height"],
                    shape_data["color"]
                )
            shape.fill = shape_data["fill"]
            shapes.append(shape)

        return shapes
