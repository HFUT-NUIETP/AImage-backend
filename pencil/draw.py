#!/usr/bin/env python
# encoding: utf-8

from pencil import pencil_draw,color_draw
import argparse

parser = argparse.ArgumentParser(description='Pencil Drawing Program. '
                                             'You will get the productions at the output folder.')
parser.add_argument('--p', action='store_true', default=False,
                    dest='p', help='for graphic pencil drawing')
parser.add_argument('--c', action='store_true', default=False,
                    dest='c', help='for color pencil drawing')
parser.add_argument('-img', dest='image', type=str, default='pencil/input/input.jpg',
                    help="input image path, default is 'pencil/input/input.jpg'.")
parser.add_argument('-s', dest="gammaS", type=float, default=1,
                    help='Larger when you want the line of strokes darker, default value is 1.')
parser.add_argument('-i', dest='gammaI', type=float, default=1,
                    help='Larger when you want the color of productions deeper, default value is 1.')
args = parser.parse_args()

if not args.p and not args.c:
    args.p = True
# time record
import time
time_start=time.time()

if args.p:
    pencil_draw(path=args.image, gammaS=args.gammaS, gammaI=args.gammaI)
if args.c:
    color_draw(path=args.image, gammaS=args.gammaS, gammaI=args.gammaI)

time_end=time.time()
print('time cost -> ', time_end - time_start)