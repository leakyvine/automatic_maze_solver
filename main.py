from window import *

def main():
    win = Window(1280, 900)
    lin = Line(Point(10, 40), Point(690, 500))
    win.draw_line(lin, "purple")
    win.wait_for_close()

main()