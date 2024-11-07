class Polygon:
    def __init__(self, points, color, fill):
        self.shape_type = "polygon"
        self.points = points
        self.color = color
        self.fill = fill
        self.selected = False
