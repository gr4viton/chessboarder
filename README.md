# chessboarder
Generates chessboard svg files using the python module svgwrite.

User can specify its dimensions in [mm], x and y offsets. The script can print a frame around the paper, as well as informatic title header.

## Requirements
Install module svgwrite

`$ pip install svgwrite`

## Command prompt
Can be used from the terminal

`$ chessboarder -a <a-side> -b <b-side> -x <x-offsets> -y <y-offsets> -c <color-odd> -C <color2-even> -X <paper-width> -Y <paper-height> -[t]itle-print -f <frame-print-color>`

Square colors are specified in hex format (`#ffffff` for white)
`frame-print-color` is svg name-color (`green` for green)
