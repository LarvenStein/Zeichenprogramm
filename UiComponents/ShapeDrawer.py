from Objects.Shape import Shape


class ShapeDrawer:
    def __init__(self, canvas, drawing_area):
        self.canvas = canvas
        self.drawing_area = drawing_area
        self.start_x = None
        self.start_y = None
        self.current_shape = None
        self.shape_type = None

    def set_shape_type(self, shape_type):
        self.shape_type = shape_type

    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def on_drag(self, event):
        if self.start_x is not None and self.start_y is not None:
            if self.current_shape:
                self.canvas.delete(self.current_shape)

            width = event.x - self.start_x
            height = event.y - self.start_y

            if self.shape_type == "line":
                width = event.x
                height = event.y

            # draw shape object
            self.current_shape = self.drawing_area.draw_shape(
                Shape(self.shape_type, self.start_x, self.start_y, width, height))

    def on_release(self, event):
        if self.start_x is not None and self.start_y is not None:
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
            self.drawing_area.add_shape(self.shape_type, x, y, width, height)

            # Reset for the next shape
            self.start_x = None
            self.start_y = None
            self.current_shape = None