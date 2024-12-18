import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from UiComponents.DrawingArea import DrawingArea
from tkinter import colorchooser

class ShapeLibrary:
    def __init__(self, app, main_frame, drawing_area):
        super().__init__()
        app.side_menu = ttk.Frame(main_frame, width=100)
        app.side_menu.pack(side=tk.LEFT, fill=tk.Y)
        self.drawing_area = drawing_area
        self.colorpicker_btn = None
        self.create_side_menu(app=app)

    def choose_color(self):
        color_code = colorchooser.askcolor(title="Choose color")
        DrawingArea.set_color(self.drawing_area, color_code)
        self.colorpicker_btn.config(bg=color_code[1], activebackground=color_code[1])

    def create_side_menu(self, app):
        shapes = {
            "rectangle": "Rectangle",
            "oval": "Oval",
            "line": "Line",
            "polygon": "Polygon",
            "flood_fill": "Fill",
            "move": "Move"
        }

        self.colorpicker_btn = tk.Button(app.side_menu, width=10, bg="black", activebackground="black", command=self.choose_color)
        self.colorpicker_btn.pack()

        for shape, symbol in shapes.items():
            btn = tk.Button(app.side_menu, text=symbol, font=("Arial", 12), width=10,
                            command=lambda s=shape: DrawingArea.set_shape_type(self.drawing_area, s))
            btn.pack(pady=5)
