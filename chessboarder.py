import svgwrite as svg
from svgwrite import cm, mm
import sys, getopt
from math import floor

try:
    import cairosvg
except:
    NO_PDF = True
else:
    NO_PDF = False

class Chessboarder():

    def __init__(self, a, b, x, y, unit_str='mm', print_title=False, color='#000000',
                 color2=None, h=297, w=210, frame_color=None, pdf=False):
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
        self.pdf = pdf

        self.init_swg()
        self.create_chessboard()
        self.add_title()
        self.add_frame()
        self.output()

    def set_unit(self, unit_str):
        self.unit_str = 'mm'
        self.unit = mm
        if unit_str == 'cm':
            self.unit_str = 'cm'
            self.unit = cm

    def output(self):

        self.dwg.filename = self.title + '.svg'
        print('Saved svg chessboard file:\n', self.dwg.filename ,'')
        self.dwg.save()
        if self.pdf:
            cairosvg.svg2pdf(url=self.dwg.filename,
                             write_to= self.title + '.pdf')
            print('Saved pdf chessboard file:\n', self.title + '.pdf' ,'')

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

        self.title = 'chessboard {5}x{6} [wh={0},{1}{4}] [{7}] [xy-offsets={2},{3}{4}]'.format(
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
    if len(sys.argv) <= 1:
        print(help_string)
        print('Generating test chessboards..')
        print(sys.path[0])
        # in mm
        a = b = 10
        x = y = 10
        Chessboarder(a, b, x, y, color2='#acdc42', frame_color='red', print_title=True)
        a = b = 25
        Chessboarder(a, b, x, y)
        exit()

    argv = sys.argv[1:]

    try:
      print('Args to parse:', argv)
      argOptString = 'ha:b:x:y:c:C:tf:X:Y:P'
      argLongOptString = ['help=', '?=', 'x-offset=', 'y-offset=', 'color=', 'color2=',
                          'a-side=', 'b-side=',
                          'paper-width=', 'paper-height=', 'frame-color=', 'pdf=']
      opts, args = getopt.getopt(argv, argOptString, argLongOptString)
      print('Parsed opts:', opts)
      print('Not parsed args:', args)

    except getopt.GetoptError:
        print('chessboarder --help')

    else:
        if opts:
            unit_str='mm'
            title=False
            color='#000000'
            color2=None
            h=297
            w=210
            frame_color=None
            b = None
            x = y = 10
            print_title = None
            pdf = False

            for opt, arg in opts:
                if opt in ('-h', '--help', '-?'):
                    print(self.help_string)
                    sys.exit()
                elif opt in ('-a', '--a-side'):
                    a = float(arg)
                elif opt in ('-b', '--b-side'):
                    b = float(arg)
                elif opt in ('-x', '--x-offset'):
                    x = float()
                elif opt in ('-y', '--y-offset'):
                    y = float(arg)
                elif opt in ('-c', '--color'):
                    color = arg
                elif opt in ('-C', '--color2'):
                    color2 = arg
                elif opt in ('-X', '--paper-width'):
                    w = float(arg)
                elif opt in ('-Y', '--paper-height'):
                    h = float(arg)
                elif opt in ('-f', '--frame-color'):
                    frame_color = arg
                elif opt == '-t':
                    print_title = True
                elif opt in  ('-P', '--pdf'):
                    if NO_PDF == True:
                        print(""">>> cairosvg module not found
>>> You cannot export chessboard.svg to pdf format - generatign svg only.
>>> Please install cairosvg via pip:
>>> $ pip install cairosvg
>>> or download whl for Windows from:
>>> https://pypi.python.org/pypi/CairoSVG""")
                    else:
                        pdf = True

            if b is None:
                b = a
            Chessboarder(a, b, x, y, color=color, color2=color2,
                         h=297, w=210, frame_color=frame_color, print_title=print_title,
                         pdf=pdf)
            exit()


