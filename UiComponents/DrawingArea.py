import tkinter as tk
from Objects.Shape import Shape
from Objects.Polygon import Polygon
from UiComponents.ShapeDrawer import ShapeDrawer

class DrawingArea(tk.Canvas):
    def __init__(self, app, master, **kwargs):
        super().__init__(master, **kwargs)
        self.shapes = []

        self.drawer = ShapeDrawer(canvas=self, drawing_area=self)

        self.bind("<ButtonPress-1>", self.drawer.on_press)
        self.bind("<B1-Motion>", self.drawer.on_drag)
        self.bind("<ButtonRelease-1>", self.drawer.on_release)
        self.bind("<ButtonPress-3>", self.drawer.finish_polygon)
        self.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.master = app

    def set_shape_type(self, shape_type):
        self.drawer.set_shape_type(shape_type)

    def set_color(self, color):
        self.drawer.set_color(color)

    def add_shape(self, shape_type, x, y, width, height, color):
        shape = Shape(shape_type, x, y, width, height, color)
        self.shapes.append(shape)
        self.draw_shapes()


    def draw_shape(self, shape):
        if shape.shape_type == "rectangle":
            return self.create_rectangle(shape.x, shape.y, shape.x + shape.width, shape.y + shape.height,
                                  outline=shape.color)
        elif shape.shape_type == "oval":
            return self.create_oval(shape.x, shape.y, shape.x + shape.width, shape.y + shape.height,
                             outline=shape.color)
        elif shape.shape_type == "line":
            return self.create_line(shape.x, shape.y, shape.width, shape.height, fill=shape.color)
        elif shape.shape_type == "polygon":
            return self.create_polygon(shape.points, outline=shape.color, fill=shape.fill)

        elif shape.shape_type == "diamond":
            return self.create_polygon(shape.x + shape.width / 2, shape.y,
                                shape.x + shape.width, shape.y + shape.height / 2,
                                shape.x + shape.width / 2, shape.y + shape.height,
                                shape.x, shape.y + shape.height / 2,
                                outline=shape.color, fill="")

    def draw_shapes(self):
        self.delete("all")
        print(self.shapes)
        for shape in self.shapes:
            self.draw_shape(shape)
