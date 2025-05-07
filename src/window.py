from tkinter import Tk, BOTH, Canvas
from line import *


class Window:
    def __init__(self, width, height):
        """
        Initializes a window of specified dimensions for maze visualization.

        Args:
            width: Window width in pixels
            height: Window height in pixels
        """
        self.width = width
        self.height = height
        self.__root = Tk()
        self.__root.title("MazeSolver")
        self.__root.wm_title("MazeSolver")
        self.__canvas = Canvas(self.__root, background="white")
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

        self.__root.geometry(f"{width}x{height}")  # Force window dimensions
        self.__root.resizable(False, False)  # Prevent resizing
        self._key_callback = None

        # Bind key press event to internal method
        self.__root.bind("<Key>", self._on_key)

    def show_message(self, x, y, text):
        """
        Writes a message 'text' in black Helvetica size 16 font at x, y
        """
        self.__canvas.create_text(x, y, text=text, fill="black", font=("Helvetica", 16))

    def _on_key(self, event):
        """
        Internal handler for key press events.
        """
        if self._key_callback:
            self._key_callback(event.char.lower())

    def set_key_callback(self, callback):
        """Registers a callback to be called on keypress."""
        self._key_callback = callback

    def clear(self):
        """Clears the canvas."""
        self.__canvas.delete("all")

    def redraw(self):
        """
        Updates the window to reflect any changes in the drawing.
        """
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        """
        Keeps the window open and updating until manually closed.
        """
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self):
        """
        Sets the running flag to False to allow the program to terminate.
        """
        self.__running = False

    def draw_line(self, line, fill_color):
        """
        Draws a Line object on the canvas with specified color.

        Args:
            line: Line object to draw
            fill_color: Color to draw the line with
        """
        line.draw(self.__canvas, fill_color)

    def draw_line_coords(self, x1, y1, x2, y2, color):
        """
        Convenience method to draw a line using coordinate values.

        Args:
            x1, y1: Starting point coordinates
            x2, y2: Ending point coordinates
            color: Color to draw the line with
        """
        line = Line(Point(x1, y1), Point(x2, y2))
        self.draw_line(line, color)
