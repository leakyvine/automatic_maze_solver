import random
import time
from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.root = Tk()
        self.root.title("Automatic Maze Solver")
        self.canvas = Canvas(height=self.height, width=self.width)
        self.canvas.pack()
        self.running = False
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.root.update_idletasks()
        self.root.update()

    def draw_line(self, line, fill_color):
        line.draw(self.canvas, fill_color)
    
    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()
    
    def close(self):
        self.running = False

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.point1.x, self.point1.y, self.point2.x, self.point2.y, fill=fill_color, width=2
        )

class Cell:
    def __init__(self, _x1, _x2, _y1, _y2, _win=None, has_left_wall=True, has_right_wall=True, has_top_wall=True, has_bottom_wall=True):
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall
        self._x1 = _x1
        self._x2 = _x2
        self._y1 = _y1
        self._y2 = _y2
        self._win = _win
        self.visited = False

    def draw(self):
        if self._win is None:
            return
        if self.has_top_wall:
            line = Line(Point(self._x1, self._y1), Point(self._x2, self._y1))
            line.draw(self._win.canvas, "black")
        else:
            line = Line(Point(self._x1, self._y1), Point(self._x2, self._y1))
            line.draw(self._win.canvas, "#D9D9D9")
        if self.has_bottom_wall:
            line = Line(Point(self._x1, self._y2), Point(self._x2, self._y2))
            line.draw(self._win.canvas, "black")
        else:
            line = Line(Point(self._x1, self._y2), Point(self._x2, self._y2))
            line.draw(self._win.canvas, "#D9D9D9")
        if self.has_left_wall:
            line = Line(Point(self._x1, self._y1), Point(self._x1, self._y2))
            line.draw(self._win.canvas, "black")
        else:
            line = Line(Point(self._x1, self._y1), Point(self._x1, self._y2))
            line.draw(self._win.canvas, "#D9D9D9")
        if self.has_right_wall:
            line = Line(Point(self._x2, self._y1), Point(self._x2, self._y2))
            line.draw(self._win.canvas, "black")
        else:
            line = Line(Point(self._x2, self._y1), Point(self._x2, self._y2))
            line.draw(self._win.canvas, "#D9D9D9")

    def draw_move(self, to_cell, undo=False):
        x1 = sum([self._x1, self._x2]) / 2
        y1 = sum([self._y1, self._y2]) / 2
        x2 = sum([to_cell._x1, to_cell._x2]) / 2
        y2 = sum([to_cell._y1, to_cell._y2]) / 2
        fill = "red"
        if undo:
            fill = "gray"
        line = Line(Point(x1, y1), Point(x2, y2))
        line.draw(self._win.canvas, fill)

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        if seed is not None:
            self.seed = random.seed(seed)
        self._create_cells()
        self._break_walls_r(0, 0)
        self._break_entrance_and_exit()
        self._debug_print_walls()

    def _create_cells(self):
        self._cells = []
        for i in range(self.num_rows):
            row = []
            for j in range(self.num_cols):
                cell = Cell(0, 0, 0, 0, self.win, True, True, True, True)
                row.append(cell)
            self._cells.append(row)
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self._draw_cell(i, j)



    def _draw_cell(self, i, j): # i is row, j is column
        x1 = self.x1 + j * self.cell_size_x 
        y1 = self.y1 + i * self.cell_size_y 
        x2 = x1 + self.cell_size_x
        y2 = y1 + self.cell_size_y
        
        cell = self._cells[i][j]
        cell._x1 = x1
        cell._y1 = y1
        cell._x2 = x2
        cell._y2 = y2
        if self.win is not None:
            print("DRAWING CHECK")
            cell.draw()
            self._animate()
        


    def _animate(self):
        self.win.redraw()
        time.sleep(0.005)

    def _break_entrance_and_exit(self):
        start = self._cells[0][0]
        start.has_top_wall = False
        start.draw()

        #print(f"Maze dimensions: {len(self._cells)} rows by {len(self._cells[0])} columns")
        #print(f"Trying to access cell at position: {len(self._cells)-1}, {len(self._cells[0])-1}")

        end = self._cells[-1][-1]
        #print(f"End cell exists: {end is not None}")
        end.has_bottom_wall = False
        end.draw()

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        print(f"DEBUG: Currently at cell {i}/{j}")
        while True:
            to_visit = []
            if i > 0 and not self._cells[i-1][j].visited:
                to_visit.append((i-1, j))
            if i < len(self._cells) -1 and not self._cells[i+1][j].visited:
                to_visit.append((i+1, j))
            if j > 0 and not self._cells[i][j-1].visited:
                to_visit.append((i, j-1))
            if j < len(self._cells[i]) - 1 and not self._cells[i][j+1].visited:
                to_visit.append((i, j+1))
            print(f"DEBUG: to_visit: {to_visit}")
            if not to_visit:
                self._cells[i][j].draw()
                return
            else:
                next_pos = random.choice(to_visit)
                next_i, next_j = next_pos

                if next_i < i:  # next cell is above
                    #print(f"DEBUG: Breaking wall between ({i},{j}) and ({next_i},{next_j}) - TOP")
                    self._cells[i][j].has_top_wall = False
                    self._cells[next_i][next_j].has_bottom_wall = False
                    self._cells[i][j].draw()
                    self._cells[next_i][next_j].draw()
                elif next_i > i:  # next cell is below
                    #print(f"DEBUG: Breaking wall between ({i},{j}) and ({next_i},{next_j}) - BOTTOM")
                    self._cells[i][j].has_bottom_wall = False
                    self._cells[next_i][next_j].has_top_wall = False
                    self._cells[i][j].draw()
                    self._cells[next_i][next_j].draw()
                elif next_j < j:  # next cell is left
                    #print(f"DEBUG: Breaking wall between ({i},{j}) and ({next_i},{next_j}) - LEFT")
                    self._cells[i][j].has_left_wall = False
                    self._cells[next_i][next_j].has_right_wall = False
                    self._cells[i][j].draw()
                    self._cells[next_i][next_j].draw()
                elif next_j > j:  # next cell is right
                    #print(f"DEBUG: Breaking wall between ({i},{j}) and ({next_i},{next_j}) - RIGHT")
                    self._cells[i][j].has_right_wall = False
                    self._cells[next_i][next_j].has_left_wall = False
                    self._cells[i][j].draw()
                    self._cells[next_i][next_j].draw()
                self._animate()
                time.sleep(0.05)
                self._break_walls_r(next_i, next_j)

    def _debug_print_walls(self):
        for i in range(len(self._cells)):
            for j in range(len(self._cells[i])):
                cell = self._cells[i][j]
                print(f"Cell ({i},{j}): T:{cell.has_top_wall} R:{cell.has_right_wall} B:{cell.has_bottom_wall} L:{cell.has_left_wall}")
                