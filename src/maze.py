from cell import *
import random
import time

DIRECTIONS = {
    "N": (0, -1, "top", "bottom"),
    "S": (0, 1, "bottom", "top"),
    "W": (-1, 0, "left", "right"),
    "E": (1, 0, "right", "left"),
}


class Maze:
    """
    Represents a grid-based maze.

    Args:
        x1 (int): Starting x-coordinate for the maze.
        y1 (int): Starting y-coordinate for the maze.
        num_rows (int): Number of rows in the maze.
        num_cols (int): Number of columns in the maze.
        cell_size_x (int): Width of each cell.
        cell_size_y (int): Height of each cell.
        win (Window, optional): Window object for drawing. Defaults to None.
        seed (int, optional): Random seed for maze generation. Defaults to None.
    """

    def __init__(
        self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self._win = win
        self._cells = [[] for _ in range(self.num_cols)]
        self._create_cells()
        self.entrance = None
        self.exit = None

        if seed is not None:
            random.seed(seed)

    def draw(self):
        """
        Draws all cells in the maze.
        """
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._cells[i][j].draw()

    def solve(self):
        """
        Solves the maze starting from the entrance cell (0,0).
        Returns True if the maze was solved, False otherwise.
        """
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        """
        Recursively attempts to solve the maze from cell (i, j).
        Marks visited cells and backtracks if necessary.
        """
        self._animate()
        current = self._cells[i][j]
        current.visited = True

        if current is self.exit:
            return True

        for direction, (di, dj, current_wall, _) in DIRECTIONS.items():
            ni, nj = i + di, j + dj
            if 0 <= ni < self.num_cols and 0 <= nj < self.num_rows:
                next_cell = self._cells[ni][nj]
                if (
                    not getattr(current, f"has_{current_wall}_wall")
                    and not next_cell.visited
                ):
                    current._draw_move(next_cell)
                    if self._solve_r(ni, nj):
                        return True
                    current._draw_move(next_cell, True)

        return False

    def _get_unvisited_neighbors(self, i, j):
        """
        Returns a list of unvisited neighboring cells of the cell at (i, j).
        Each neighbor is represented as a tuple (ni, nj, direction).
        """
        neighbors = []
        for direction, (di, dj, _, _) in DIRECTIONS.items():
            ni, nj = i + di, j + dj
            if 0 <= ni < self.num_cols and 0 <= nj < self.num_rows:
                if not self._cells[ni][nj].visited:
                    neighbors.append((ni, nj, direction))
        return neighbors

    def _break_wall_between(self, i1, j1, i2, j2, direction):
        """
        Removes the wall between two adjacent cells in the given direction.
        Updates both cells to reflect the broken wall.
        """
        _, _, current_wall, next_wall = DIRECTIONS[direction]
        setattr(self._cells[i1][j1], f"has_{current_wall}_wall", False)
        setattr(self._cells[i2][j2], f"has_{next_wall}_wall", False)

    def _reset_cells_visited(self):
        """
        Marks all cells in the maze as unvisited.
        """
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._cells[i][j].visited = False

    def _break_walls_r(self, i, j):
        """
        Recursively visits cells in randomized order to break walls between
        them and generate a complete maze using depth-first search.
        """
        self._cells[i][j].visited = True
        self._cells[i][j].draw()
        self._win.redraw()
        time.sleep(0.002)

        neighbors = self._get_unvisited_neighbors(i, j)
        random.shuffle(neighbors)

        for ni, nj, direction in neighbors:
            if not self._cells[ni][nj].visited:
                self._break_wall_between(i, j, ni, nj, direction)
                self._break_walls_r(ni, nj)

    def _break_entrance_and_exit(self):
        """
        Creates entrance and exit by removing the top wall of the
        first cell and the bottom wall of the last cell.
        Sets self.entrance and self.exit references.
        """
        maze_entrance = self._cells[0][0]
        maze_exit = self._cells[-1][-1]
        maze_entrance.has_top_wall = False
        maze_exit.has_bottom_wall = False
        if self._win is not None:
            maze_entrance.draw()
            maze_exit.draw()

        self.entrance = maze_entrance
        self.exit = maze_exit

    def _create_cells(self):
        """
        fills self._cells with a list of cells. Each top-level list is a column
        of Cell objects. Once the matrix is populated it calls _draw_cell() method
        on each Cell.
        """
        for i in range(self.num_cols):
            # initialize empty column
            self._cells[i] = []

            for j in range(self.num_rows):
                # calculate cell coords
                x1 = self.x1 + i * self.cell_size_x
                y1 = self.y1 + j * self.cell_size_y
                x2 = x1 + self.cell_size_x
                y2 = y1 + self.cell_size_y

                # create the cell
                cell = Cell(x1, y1, x2, y2, self._win)
                self._cells[i].append(cell)

        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._draw_cell(i, j)
            # print(f"drawing cell at {i}, {j}")

    def _draw_cell(self, i, j):
        """
        Draws the cell at position (i, j) in the grid
        """
        cell = self._cells[i][j]

        if self._win is not None:
            cell.draw()
            self._animate()

    def _animate(self):
        """
        calls window's redraw() method, then uses time.sleep()
        for a short amount of time (0.02s)
        """
        self._win.redraw()
        time.sleep(0.002)
