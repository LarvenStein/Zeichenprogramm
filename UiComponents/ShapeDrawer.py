from Objects.Shape import Shape
from Objects.Polygon import Polygon


class ShapeDrawer:
    def __init__(self, canvas, drawing_area):
        self.canvas = canvas
        self.drawing_area = drawing_area
        self.start_x = None
        self.start_y = None
        self.current_shape = None
        self.shape_type = None
        self.polygon_points = []
        self.color = "black"

    def set_shape_type(self, shape_type):
        self.shape_type = shape_type

    def set_color(self, color):
        self.color = color[1]

    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y

        if self.shape_type == "flood_fill":
            self.drawing_area.flood_fill(event, self.color)
            return

        if self.shape_type == "polygon":
            self.polygon_points.append(event.x)
            self.polygon_points.append(event.y)
            return

        if self.shape_type is None:
            self.select_shape(event)

    def handle_hove(self, event):
        dx = event.x - self.start_x
        dy = event.y - self.start_y

        for shape in self.canvas.selected_shapes:
            if shape.shape_type == "polygon":
                new_points = []
                for i in range(0, len(shape.points), 2):
                    new_points.append(shape.points[i] + dx)
                    new_points.append(shape.points[i + 1] + dy)
                shape.points = new_points
            elif shape.shape_type == "line":
                # Move both start and end points of the line
                shape.x += dx
                shape.y += dy
                shape.width += dx
                shape.height += dy
            else:
                # For other shapes (rectangles, ovals, etc.)
                shape.x += dx
                shape.y += dy

        self.drawing_area.draw_shapes()
        self.start_x = event.x
        self.start_y = event.y

    def on_drag(self, event):
        if self.start_x is not None and self.start_y is not None:
            if len(self.canvas.selected_shapes) > 0 and self.shape_type == "move":
                self.handle_hove(event)
                return

            if self.current_shape:
                self.canvas.delete(self.current_shape)

            width = event.x - self.start_x
            height = event.y - self.start_y

            if self.shape_type == "line":
                width = event.x
                height = event.y

            shape_type = self.shape_type
            color = self.color

            if self.shape_type is None:
                shape_type = "rectangle"
                color = "blue"
                self.current_shape = Shape(shape_type, self.start_x, self.start_y, width, height, color)
                self.drawing_area.select_colliding_shapes()

            # draw shape object
            self.current_shape = self.drawing_area.draw_shape(
                Shape(shape_type, self.start_x, self.start_y, width, height, color))



    def select_shape(self, event):
        selected_shapes = []
        # Ab hier die funktion  bitte nicht weiterlesen
        for shape in self.drawing_area.shapes:
            if shape.shape_type == 'polygon':
                if self.drawing_area.is_point_in_polygon(event.x, event.y, shape.points):
                    shape.selected = True
                    selected_shapes.append(shape)
                    self.drawing_area.draw_shapes()
                    self.drawing_area.selected_shapes = selected_shapes
                    break
                else:
                    shape.selected = False
            else:
                if (shape.x <= event.x <= shape.x + shape.width) and (shape.y <= event.y <= shape.y + shape.height):
                    shape.selected = True
                    selected_shapes.append(shape)
                    self.drawing_area.draw_shapes()
                    self.drawing_area.selected_shapes = selected_shapes
                    break
                else:
                    shape.selected = False

            self.drawing_area.draw_shapes()
            self.drawing_area.selected_shapes = selected_shapes


    def finish_polygon(self, event):
        if self.shape_type != "polygon":
            return

        polygon = Polygon(self.polygon_points, self.color, "white")

        self.drawing_area.shapes.append(polygon)
        self.drawing_area.draw_shapes()

        self.polygon_points = []
        self.shape_type = None
        self.drawing_area.master.config(cursor="arrow")

    def on_release(self, event):
        if self.shape_type is not "polygon":
            self.drawing_area.master.config(cursor="arrow")

        if self.shape_type is None:
            self.canvas.delete(self.current_shape)

        if self.start_x is not None and self.start_y is not None:
            if self.shape_type == "polygon" or self.shape_type == None:
                return

            end_x = event.x
            end_y = event.y

            x = min(self.start_x, end_x)
            y = min(self.start_y, end_y)
            width = abs(end_x - self.start_x)
            height = abs(end_y - self.start_y)

            # This never exsisted, move on
            if self.shape_type == "line":
                x = self.start_x
                y = self.start_y
                width = event.x
                height = event.y

            # Call add_shape method of DrawingArea
            self.drawing_area.add_shape(self.shape_type, x, y, width, height, self.color)

            # Reset for the next shape
            self.start_x = None
            self.start_y = None
            self.current_shape = None
            if self.shape_type != "polygon":
                self.shape_type = None

