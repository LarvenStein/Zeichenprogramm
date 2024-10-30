import tkinter as tk
from Objects.Shape import Shape
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

    def flood_fill(self, event, color):
        for shape in self.shapes:
            if shape.shape_type == 'polygon':
                if self.is_point_in_polygon(event.x, event.y, shape.points):
                    shape.fill = color
                    self.draw_shapes()
                    break
            else:
                if (shape.x <= event.x <= shape.x + shape.width) and (shape.y <= event.y <= shape.y + shape.height):
                    shape.fill = color
                    self.draw_shapes()
                    break

    def set_color(self, color):
        self.drawer.set_color(color)

    def add_shape(self, shape_type, x, y, width, height, color):
        shape = Shape(shape_type, x, y, width, height, color)
        self.shapes.append(shape)
        self.draw_shapes()


    def draw_shape(self, shape):
        if shape.shape_type == "rectangle":
            return self.create_rectangle(shape.x, shape.y, shape.x + shape.width, shape.y + shape.height,
                                  outline=shape.color, fill=shape.fill)

        elif shape.shape_type == "oval":
            return self.create_oval(shape.x, shape.y, shape.x + shape.width, shape.y + shape.height,
                             outline=shape.color, fill=shape.fill)

        elif shape.shape_type == "line":
            return self.create_line(shape.x, shape.y, shape.width, shape.height, fill=shape.color)

        elif shape.shape_type == "polygon":
            return self.create_polygon(shape.points, outline=shape.color, fill=shape.fill)

        elif shape.shape_type == "diamond":
            return self.create_polygon(shape.x + shape.width / 2, shape.y,
                                shape.x + shape.width, shape.y + shape.height / 2,
                                shape.x + shape.width / 2, shape.y + shape.height,
                                shape.x, shape.y + shape.height / 2,
                                outline=shape.color, fill=shape.fill)

    def is_point_in_polygon(self, x, y, points):
        n = len(points) // 2  # Number of points
        inside = False
        p1x, p1y = points[0], points[1]
        for i in range(n + 1):
            p2x, p2y = points[(i % n) * 2], points[(i % n) * 2 + 1]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside

    def draw_shapes(self):
        self.delete("all")
        for shape in self.shapes:
            self.draw_shape(shape)
