import tkinter as tk
from Objects.Shape import Shape


class DrawingArea(tk.Canvas):
    def __init__(self, app, master, **kwargs):
        super().__init__(master, **kwargs)
        self.shapes = []
        self.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.master = app

    def add_shape(self, shape_type, x, y):
        shape = Shape(shape_type, x, y, 100, 50)
        self.shapes.append(shape)
        self.draw_shapes()

    def draw_shapes(self):
        self.delete("all")
        for shape in self.shapes:
            if shape.shape_type == "rectangle":
                self.create_rectangle(shape.x, shape.y, shape.x + shape.width, shape.y + shape.height,
                                      outline="black")
            elif shape.shape_type == "oval":
                self.create_oval(shape.x, shape.y, shape.x + shape.width, shape.y + shape.height,
                                 outline="black")
            elif shape.shape_type == "oval_with_underline":
                self.create_oval(shape.x, shape.y, shape.x + shape.width, shape.y + shape.height,
                                 outline="black")
                self.create_line(shape.x + 10, shape.y + shape.height - 10,
                                 shape.x + shape.width - 10, shape.y + shape.height - 10)
            elif shape.shape_type == "diamond":
                self.create_polygon(shape.x + shape.width / 2, shape.y,
                                    shape.x + shape.width, shape.y + shape.height / 2,
                                    shape.x + shape.width / 2, shape.y + shape.height,
                                    shape.x, shape.y + shape.height / 2,
                                    outline="black", fill="")