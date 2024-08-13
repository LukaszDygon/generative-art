import argparse
import os
from io import BytesIO
import tkinter as tk
import random
import shapely.geometry as geom
from shapely.affinity import rotate, translate
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

random.seed(42)

def main(args):
    save_folder = os.path.join('out', 'heartbeat')
    file_name = f'{args.width}x{args.height}d{args.hb_inflections}.png'
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)

    height = (args.height - args.border * 2)
    width = (args.width - args.border * 2)
    row_height = (args.height - args.border * 2) // args.rows

    if row_height < 5:
        raise(Exception(f'The size of the shape {row_height}px is too small. Decrease space, border or number of columns'))

    image = draw_heartbeat(args.width, args.height, args.border, args.rows, args.magnitude, args.hb_offset, args.hb_length, args.hb_inflections)
    image.save(os.path.join(save_folder, file_name))

def draw_heartbeat(width: int, height: int, border: int, rows: int, magnitude: int, heartbeat_offset: float, heartbeat_length: float, heartbeat_inflections: int) -> Image:
    im = Image.new("RGB", (width, height), '#efeee4')
    canvas = ImageDraw.Draw(im)
    row_height = (args.height - args.border * 2) // args.rows
    inflection_section_width = (width - border * 2) // heartbeat_inflections * heartbeat_length
    inflection_start = border + (width - border * 2) * heartbeat_offset
    for row in range(-magnitude, rows + magnitude):
        color = tuple(np.random.choice(range(30, 256), size=3))
        coords = [(border, border + row_height * row), (inflection_start, border + row_height * row)]
        for inflection in range(0, heartbeat_inflections):
            coords += [(
                coords[-1][0] + inflection_section_width,
                coords[-1][1] + (row_height if inflection % 2 else -row_height) * magnitude * ((heartbeat_inflections - inflection) / heartbeat_inflections)
                )]
        coords += [(width - border, coords[-1][1])]
        coords += [(coord[0], coord[1] + row_height) for coord in coords[::-1]]  # 'bottom' of the shape
        shape = geom.Polygon(coords)
        canvas.polygon(tuple(shape.exterior.coords), fill=color)
    draw_border(canvas, border)

    return im

def draw_border(canvas: ImageDraw.ImageDraw, border: int) -> ImageDraw.ImageDraw:
        canvas.rectangle([(0,0), (canvas.im.size[0],border)], fill='#efeee4')
        canvas.rectangle([(0,canvas.im.size[1]-border), (canvas.im.size[0],canvas.im.size[1])], fill='#efeee4')
        canvas.rectangle([(0,0), (border,canvas.im.size[1])], fill='#efeee4')
        canvas.rectangle([(canvas.im.size[0]-border,0), (canvas.im.size[0],canvas.im.size[1])], fill='#efeee4')


if __name__ == '__main__':
    # Parse the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--width', type=int, default=3000, help='The width of the canvas')
    parser.add_argument('-hh', '--height', type=int, default=3000, help='The height of the canvas')
    parser.add_argument('-b', '--border', type=int, default=100, help='Border size in px')
    parser.add_argument('-m', '--magnitude', type=int, default=4, help='Magnitude of the \'heartbeat\'')
    parser.add_argument('-r', '--rows', type=int, default=20, help='Number of different colored rows')
    # parser.add_argument('-d', '--distortion', type=float, default=0.5, help='Distortion magnitude affecting the alignment after heartbeat')
    parser.add_argument('-ho', '--hb-offset', type=float, default=0.8, help='Offset between 0 and 1 of where in horizontal space the heartbeat should start')
    parser.add_argument('-hl', '--hb-length', type=float, default=0.15, help='Length of the heartbeat, between 0 and 1 in horizontal space the heartbeat should last')
    parser.add_argument('-hi', '--hb-inflections', type=int, default=2, help='Number of inflection points')
    
    args = parser.parse_args()

    # Call the main function
    main(args)