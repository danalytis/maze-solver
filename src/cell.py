class Cell:
    """
    Initializes a cell in the maze with walls and position.

    Args:
        x1, y1: Coordinates of top-left corner
        x2, y2: Coordinates of bottom-right corner
        win: Window object for drawing
    """

    def __init__(self, x1, y1, x2, y2, win):

        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self.center_point = (
            ((self._x2 - self._x1) // 2) + self._x1,
            ((self._y2 - self._y1) // 2) + self._y1,
        )
        self._win = win

    def draw(self):
        """
        Draws the cell walls based on their current state.
        Walls are drawn in black if present, white if absent.
        """
        if self.has_left_wall:
            self._win.draw_line_coords(self._x1, self._y1, self._x1, self._y2, "black")
        else:
            self._win.draw_line_coords(self._x1, self._y1, self._x1, self._y2, "white")
        if self.has_right_wall:
            self._win.draw_line_coords(self._x2, self._y1, self._x2, self._y2, "black")
        else:
            self._win.draw_line_coords(self._x2, self._y1, self._x2, self._y2, "white")
        if self.has_top_wall:
            self._win.draw_line_coords(self._x1, self._y1, self._x2, self._y1, "black")
        else:
            self._win.draw_line_coords(self._x1, self._y1, self._x2, self._y1, "white")
        if self.has_bottom_wall:
            self._win.draw_line_coords(self._x1, self._y2, self._x2, self._y2, "black")
        else:
            self._win.draw_line_coords(self._x1, self._y2, self._x2, self._y2, "white")

    def _draw_move(self, to_cell, undo=False):
        """
        Draws a line between this cell's center and another cell's center.

        Args:
            to_cell: The destination cell to draw a line to
            undo: If True, draws white line (backtracking),
                  otherwise draws red line (forward movement)
        """
        color = "grey" if undo else "red"
        self._win.draw_line_coords(
            self.center_point[0],
            self.center_point[1],
            to_cell.center_point[0],
            to_cell.center_point[1],
            color,
        )
