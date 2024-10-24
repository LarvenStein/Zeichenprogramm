import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from UiComponents.DrawingArea import DrawingArea


class ShapeLibrary:
    def __init__(self, app, main_frame, drawing_area):
        super().__init__()
        app.side_menu = ttk.Frame(main_frame, width=100)
        app.side_menu.pack(side=tk.LEFT, fill=tk.Y)
        self.drawing_area = drawing_area

        self.create_side_menu(app=app)

    def create_side_menu(self, app):
        shapes = {
            "rectangle": "⬜",
            "oval": "⭕",
            "diamond": "◆",
            "line": "➖"
        }
        for shape, symbol in shapes.items():
            btn = tk.Button(app.side_menu, text=symbol, font=("Arial", 20),
                            command=lambda s=shape: DrawingArea.set_shape_type(self.drawing_area, s))
            btn.pack(pady=5)
