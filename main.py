from window import *

def main():
    win = Window(1280, 900)
    #lin = Line(Point(10, 40), Point(690, 500))
    cell = Cell(100,50,200,400, win, True,True,True,False)
    #win.draw_line(lin, "purple")
    cell.draw()
    win.wait_for_close()

main()