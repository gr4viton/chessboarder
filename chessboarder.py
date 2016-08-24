import svgwrite as svg
from svgwrite import cm, mm
import sys, getopt
from math import floor

class Chessboarder():

    def __init__(self, a, b, x, y, unit_str='mm', print_title=False, color='#000000',
                 color2=None, h=297, w=210, frame_color=None):
        self.a = a
        self.b = b
        self.x = x
        self.y = y
        self.set_unit(unit_str)
        self.print_title = print_title
        self.h = h
        self.w = w

        self.color = color
        self.color2 = color2
        self.frame_color = frame_color # e.g 'green'

        self.init_swg()
        self.create_chessboard()
        self.add_title()
        self.add_frame()
        self.output()
    #
    # def __init__(self, opts, help_string):
    #     self.opts = opts
    #     self.help_string = help_string
    #
    #     self.title = False
    #     self.get_opts()
    #
    #     self.init_swg()
    #     self.create_chessboard()
    #     if self.title == True:
    #         self.add_title()
    #     self.output()
    #
    # def get_opts(self):
    #     for opt, arg in self.opts:
    #         if opt in ('-h', '--help', '-?'):
    #             print(self.help_string)
    #             sys.exit()
    #         elif opt in ('-a', '--a-side'):
    #             self.a = arg
    #         elif opt in ('-b', '--b-side'):
    #             self.b = arg
    #         elif opt in ('-x', '--x-offset'):
    #             self.x = arg
    #         elif opt in ('-y', '--y-offset'):
    #             self.y = arg
    #         elif opt in ('-c', '--color'):
    #             self.color = arg
    #         elif opt in ('-C', '--color2'):
    #             self.color2 = arg
    #         elif opt in ('-X', '--paper-width'):
    #             self.w = arg
    #         elif opt in ('-Y', '--paper-height'):
    #             self.h = arg
    #         elif opt in ('-f', '--frame-color'):
    #             self.frame_color = arg
    #         elif opt == '-t':
    #             self.title = True

    def set_unit(self, unit_str):
        self.unit_str = 'mm'
        self.unit = mm
        if unit_str == 'cm':
            self.unit_str = 'cm'
            self.unit = cm

    def output(self):
        self.dwg.filename = self.title + '.svg'
        self.dwg.save()

    def init_swg(self):
        sh = str(self.h)
        sw = str(self.w)
        siz = (sw + self.unit_str,
               sh + self.unit_str)
        print(siz)
        self.dwg = svg.Drawing('chessboard.svg', size=siz, baseProfile="full")

    def add_title(self):
        col = self.color
        if self.color2:
            col+= self.color2

        self.title = 'chessboard {5}x{6} [wh={0},{1}{4}] [xy-offsets={2},{3}{4}] [{7}]'.format(
            self.a, self.b, self.x, self.y, self.unit_str, self.numx, self.numy, col
        )
        print(self.title)

        if self.print_title == True:
            self.dwg.add(self.dwg.text(self.title, insert=(2*mm, 5*mm), fill='red'))

    def add_frame(self):
        u = self.unit
        if self.frame_color:
            self.dwg.add(self.dwg.rect(insert=(0,0),
                                       size=(self.w*u, self.h*u),
                                       stroke=self.frame_color, fill='none'))

    def create_chessboard(self):
        squares = self.dwg.add(self.dwg.g(id='squares_odd', fill=self.color))
        if self.color2:
            squares2 = self.dwg.add(self.dwg.g(id='squares_even', fill=self.color2))


        a = self.a
        b = self.b
        ox = self.x
        oy = self.y
        u = self.unit
        s=1

        self.numx = floor((self.w - 2*ox)/a)
        self.numy = floor((self.h - 2*oy)/b)

        for x in range(self.numx):
            for y in range(self.numy):
                rect = self.dwg.rect(
                            insert=( (ox + x*a) *u, (oy + y*b) *u),
                            size=(a*u, b*u))
                if not (x+y)%2:
                    squares.add(rect)
                else:
                    if self.color2:
                        squares2.add(rect)



if __name__ == '__main__':
    help_string = 'chessboarder -a <a-side> -b <b-side> -x <x-offsets> -y <y-offsets> -c <color-odd> -C <color2-even> -X <paper-width> -Y <paper-height> -[t]itle-print -f <frame-print-color>'
    # args = sys.args
    argv = sys.argv
    # getopt.getopt(args, options, [long_options])

    try:
      opts, args = getopt.getopt(argv, 'ha:bxycCtfXY:',
                                 ['help=', '?=', 'x-offset=', 'y-offset=', 'color=', 'color2=', 'a-side=', 'b-side=', 'paper-width=', 'paper-height=', 'frame-color='])
    except getopt.GetoptError:
        print('chessboarder --help')

    if opts:
        # Chessboarder(opts, help_string)
        unit_str='mm'
        title=False
        color='#000000'
        color2=None
        h=297
        w=210
        frame_color=None

        for opt, arg in self.opts:
            if opt in ('-h', '--help', '-?'):
                print(self.help_string)
                sys.exit()
            elif opt in ('-a', '--a-side'):
                a = arg
            elif opt in ('-b', '--b-side'):
                b = arg
            elif opt in ('-x', '--x-offset'):
                x = arg
            elif opt in ('-y', '--y-offset'):
                y = arg
            elif opt in ('-c', '--color'):
                color = arg
            elif opt in ('-C', '--color2'):
                color2 = arg
            elif opt in ('-X', '--paper-width'):
                w = arg
            elif opt in ('-Y', '--paper-height'):
                h = arg
            elif opt in ('-f', '--frame-color'):
                frame_color = arg
            elif opt == '-t':
                print_title = True
        Chessboarder(a, b, x, y, color='#000000', color2=color2,
                     h=297, w=210, frame_color=frame_color, print_title=print_title)

    else:
        print(help_string)
        print('Generating test chessboards..')
        print(sys.path[0])
        # in mm
        a = b = 10
        x = y = 10
        Chessboarder(a, b, x, y, color2='#acdc42', frame_color='red', print_title=True)
        a = b = 25
        Chessboarder(a, b, x, y)

