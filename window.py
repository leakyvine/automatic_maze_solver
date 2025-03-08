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
    def __init__(self, _x1, _x2, _y1, _y2, _win, has_left_wall=True, has_right_wall=True, has_top_wall=True, has_bottom_wall=True):
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall
        self._x1 = _x1
        self._x2 = _x2
        self._y1 = _y1
        self._y2 = _y2
        self._win = _win

    def draw(self):
        if self.has_top_wall:
            line = Line(Point(self._x1, self._y1), Point(self._x2, self._y1))
            line.draw(self._win.canvas, "black")
        if self.has_bottom_wall:
            line = Line(Point(self._x1, self._y2), Point(self._x2, self._y2))
            line.draw(self._win.canvas, "black")
        if self.has_left_wall:
            line = Line(Point(self._x1, self._y1), Point(self._x1, self._y2))
            line.draw(self._win.canvas, "black")
        if self.has_right_wall:
            line = Line(Point(self._x2, self._y1), Point(self._x2, self._y2))
            line.draw(self._win.canvas, "black")

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
