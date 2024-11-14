import tkinter as tk
from Objects.Shape import Shape
from UiComponents.ShapeDrawer import ShapeDrawer
from PIL import Image, ImageDraw, ImageOps
import os

class DrawingArea(tk.Canvas):
    def __init__(self, app, master, **kwargs):
        super().__init__(master, **kwargs)
        self.shapes = []
        self.selected_shapes = []
        self.drawer = ShapeDrawer(canvas=self, drawing_area=self)

        self.bind("<ButtonPress-1>", self.drawer.on_press)
        self.bind("<B1-Motion>", self.drawer.on_drag)
        self.bind("<ButtonRelease-1>", self.drawer.on_release)
        self.bind("<ButtonPress-3>", self.drawer.finish_polygon)
        self.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.master = app

    def export_canvas_as_image(self, filename):
        # Create an empty image with the same size as the canvas
        width = self.winfo_width()
        height = self.winfo_height()
        image = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(image)

        # Draw all shapes onto the image
        for shape in self.shapes:
            if shape.color == '':
                shape.color = 'black'  # Set a default color if none is specified

            if shape.shape_type == "rectangle":
                draw.rectangle([shape.x, shape.y, shape.x + shape.width, shape.y + shape.height], outline=shape.color, fill=shape.fill)
            elif shape.shape_type == "oval":
                draw.ellipse([shape.x, shape.y, shape.x + shape.width, shape.y + shape.height], outline=shape.color, fill=shape.fill)
            elif shape.shape_type == "line":
                draw.line([shape.x, shape.y, shape.width, shape.height], fill=shape.color)
            elif shape.shape_type == "polygon":
                draw.polygon(shape.points, outline=shape.color, fill=shape.fill)
            elif shape.shape_type == "diamond":
                draw.polygon([shape.x + shape.width / 2, shape.y, shape.x + shape.width, shape.y + shape.height / 2,
                              shape.x + shape.width / 2, shape.y + shape.height, shape.x, shape.y + shape.height / 2],
                             outline=shape.color, fill=shape.fill)

        # Save the image
        file_extension = filename.split('.')[-1].lower()
        valid_extensions = ["jpg", "jpeg", "bmp", "webp", "gif", "png"]

        if file_extension not in valid_extensions:
            raise ValueError(f"Unsupported file format: {file_extension}")

        image.save(filename)

    def select_colliding_shapes(self):
        rect = self.drawer.current_shape
        if not rect:
            print("Error: The current shape is None")
            return

        selected_shapes = []

        for shape in self.shapes:
            if self.is_colliding(rect, shape):
                shape.selected = True
                selected_shapes.append(shape)
            else:
                shape.selected = False

        self.draw_shapes()
        self.selected_shapes = selected_shapes

    def is_colliding(self, rect, shape):
        if not rect:
            return False

        if shape.shape_type == 'polygon':
            # Check if any point of the polygon is inside the rectangle
            for i in range(0, len(shape.points), 2):
                if rect.x <= shape.points[i] <= rect.x + rect.width and rect.y <= shape.points[
                    i + 1] <= rect.y + rect.height:
                    return True
            # Check if any edge of the rectangle intersects with any edge of the polygon
            rect_edges = [
                ((rect.x, rect.y), (rect.x + rect.width, rect.y)),
                ((rect.x + rect.width, rect.y), (rect.x + rect.width, rect.y + rect.height)),
                ((rect.x + rect.width, rect.y + rect.height), (rect.x, rect.y + rect.height)),
                ((rect.x, rect.y + rect.height), (rect.x, rect.y))
            ]
            for i in range(0, len(shape.points), 2):
                polygon_edge = (
                    (shape.points[i], shape.points[i + 1]),
                    (shape.points[(i + 2) % len(shape.points)], shape.points[(i + 3) % len(shape.points)])
                )
                for rect_edge in rect_edges:
                    if self.edges_intersect(rect_edge, polygon_edge):
                        return True
        else:
            # Check for collision with other shapes
            return not (rect.x > shape.x + shape.width or
                        rect.x + rect.width < shape.x or
                        rect.y > shape.y + shape.height or
                        rect.y + rect.height < shape.y)
        return False

    def edges_intersect(self, edge1, edge2):
        def ccw(A, B, C):
            return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

        A, B = edge1
        C, D = edge2
        return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)

    def set_shape_type(self, shape_type):
        self.master.config(cursor="tcross")

        if shape_type == "polygon":
            self.master.config(cursor="target")

        if shape_type == "move":
            self.master.config(cursor="fleur")

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
        color = shape.color
        if shape.selected:
            color = "red"


        if shape.shape_type == "rectangle":
            return self.create_rectangle(shape.x, shape.y, shape.x + shape.width, shape.y + shape.height,
                                  outline=color, fill=shape.fill)

        elif shape.shape_type == "oval":
            return self.create_oval(shape.x, shape.y, shape.x + shape.width, shape.y + shape.height,
                             outline=color, fill=shape.fill)

        elif shape.shape_type == "line":
            return self.create_line(shape.x, shape.y, shape.width, shape.height, fill=color)

        elif shape.shape_type == "polygon":
            return self.create_polygon(shape.points, outline=color, fill=shape.fill)

        elif shape.shape_type == "diamond":
            return self.create_polygon(shape.x + shape.width / 2, shape.y,
                                shape.x + shape.width, shape.y + shape.height / 2,
                                shape.x + shape.width / 2, shape.y + shape.height,
                                shape.x, shape.y + shape.height / 2,
                                outline=color, fill=shape.fill)

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
