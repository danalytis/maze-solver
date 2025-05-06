from window import Window
from maze import Maze


def generate_and_solve(win):
    """
    Generates a new maze of fixed dimensions and solves it.
    """
    win.clear()
    maze = Maze(80, 80, 15, 25, 25, 25, win)
    maze._break_entrance_and_exit()
    maze._break_walls_r(0, 0)
    maze._reset_cells_visited()
    maze.draw()
    maze.solve()
    win.show_message(400, 550, "Press 'R' to reload")
    return maze


if __name__ == "__main__":
    win = Window(800, 600)
    maze = [generate_and_solve(win)]

    def on_key(key):
        if key == "r":
            print("Regenerating...")
            maze[0] = generate_and_solve(win)

    win.set_key_callback(on_key)
    win.wait_for_close()
