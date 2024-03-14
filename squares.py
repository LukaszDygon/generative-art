import argparse
import os
from io import BytesIO
import tkinter as tk
import random
import shapely.geometry as geom
from shapely.affinity import rotate, translate
from PIL import Image, ImageDraw, ImageFilter

# random.seed(42)

def main(args):
    save_folder = os.path.join('out', 'squares')
    file_name = f'{args.width}x{args.height}d{args.distortion}.png'
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)

    shape_w = (args.width - args.border * 2) // args.columns - args.space
    rows = (args.height - args.border * 2) // (shape_w + args.space)
    if shape_w < 10:
        raise(Exception(f'The size of the shape {shape_w}px is too small. Decrease space, border or number of columns'))

    image = draw_rectangles(args.width, args.height, shape_w, args.border, args.space, rows, args.columns, args.distortion)
    image.save(os.path.join(save_folder, file_name))

def draw_rectangles(width: int, height: int, shape_w: int, border: int, space: int, rows: int, cols: int, distortion_magnitude: int = 2) -> Image:
    im = Image.new("RGB", (width, height), '#efeee4')
    canvas = ImageDraw.Draw(im)
    for row in range(rows):
        for col in range(cols):
            rotation = (random.random() - 0.5) * distortion_magnitude
            move_x = (random.random() - 0.5)  * distortion_magnitude
            move_y = (random.random() - 0.5) * distortion_magnitude
            shape = geom.Polygon([
                (border + col * (shape_w + space), border + row * (shape_w + space)),
                (border + col * (shape_w + space) + shape_w, border + row * (shape_w + space)),
                (border + col * (shape_w + space) + shape_w, border + row * (shape_w + space) + shape_w),
                (border + col * (shape_w + space), border + row * (shape_w + space) + shape_w)
            ])
            shape = rotate(shape, distortion_magnitude * rotation * row)
            shape = translate(shape, move_x * row, move_y * row)
            canvas.polygon(tuple(shape.exterior.coords),
                                    fill=None,
                                    outline='black',
                                    width=3)

    
    return im

if __name__ == '__main__':
    # Parse the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--width', type=int, default=1000, help='The width of the canvas')
    parser.add_argument('-hh', '--height', type=int, default=1600, help='The height of the canvas')
    parser.add_argument('-b', '--border', type=int, default=200, help='Border size in px')
    parser.add_argument('-s', '--space', type=int, default=10, help='Space between shapes in px')
    parser.add_argument('-c', '--columns', type=int, default=10, help='Number of shapes per row')
    parser.add_argument('-d', '--distortion', type=int, default=2, help='Distortion magnitude affecting rotation and traslation of shapes')
    args = parser.parse_args()

    # Call the main function
    main(args)