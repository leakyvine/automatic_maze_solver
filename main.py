from window import *

def main():
    win = Window(1280, 900)
    #lin = Line(Point(10, 40), Point(690, 500))
    cell1 = Cell(100,300,200,400, win, True,True,True,False)
    cell2 = Cell(500,700,400,600, win, True,True,True,False)
    #win.draw_line(lin, "purple")
    cell1.draw()
    cell2.draw()
    cell1.draw_move(cell2, True)
    win.wait_for_close()

main()