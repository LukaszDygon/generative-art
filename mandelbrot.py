import argparse
import os

from PIL import Image
import numpy as np
from typing import Tuple, List

# random.seed(42)
class Madndelbrot():
    iterations: int
    width: int
    height: int
    zoom_on: Tuple[int, int]
    frames: List[np.matrix]
    images: List[Image.Image]
    current_frame: int
    zoom_rate: float
    xmin: float
    xmax: float
    ymin: float
    ymax: float

    def __init__(self, args):
        self.iterations = args.iterations
        self.width = args.width
        self.height = args.height
        self.zoom_on = (args.x, args.y)
        self.frames = []
        self.images = []
        self.current_frame = 0
        self.zoom_rate = 1.1
        self.save_location = f'{self.width}x{self.height}it{self.iterations}'

        self.xmin, self.xmax = -2, 2
        self.ymin, self.ymax = -2 * self.height/self.width, 2 * self.height/self.width

        if not os.path.exists(self.save_location):
            os.mkdir(self.save_location)

    def draw_mandelbrot(self):
        c = self._init_matrix()
        image_arr = self._f(c)
        image = Image.fromarray(image_arr.astype(np.uint8))
        self.frames.append(image_arr)
        self.images.append(image)
        with open(os.path.join(self.save_location, f'{self.current_frame}.tiff'), 'wb+') as f:
            image.save(f)
        self.current_frame += 1
    
    def save_gif(self):
        with open(os.path.join(self.save_location, 'out.gif'), 'wb+') as f:
            self.images[0].save(f, save_all=True, append_images=self.images[1:], duration=100, loop=0)

    def _get_stability_magnitude(self, c: complex) -> int:
        z = 0
        for i in range(self.iterations):
            z = z ** 2 + c
            if abs(z) >= 2:
                return 126 * (1 - i/self.iterations)
        return 0

    def _f(self, c):
        return np.vectorize(self._get_stability_magnitude)(c)

    def _find_closest_boundary(self) -> Tuple[int, int]:
        i, j = int(self.zoom_on[0] * self.width), int(self.zoom_on[1] * self.height)
        to_visit = set()
        visited = set()
        while True:
            if self.frames[-1][j][i] == 0 and self.frames[-1][i-1:i+2,j-1:j+2].max() > 0:
                return i, j
            else:
                visited.add((i,j))
                for i in range(max(0, i-1), min(self.width,i+2)):
                    for j in range(max(0, j-1), min(self.height, i+2)):
                        if (i, j) not in visited:
                            to_visit.add((i,j))
                i, j = to_visit.pop()

    def _init_matrix(self):
        if self.frames:
            center = self._find_closest_boundary()
            center = self.xmin + center[0] / self.width * (self.xmax-self.xmin), self.ymin + center[1] / self.width * (self.ymax-self.ymin)
            self.xmin, self.xmax = \
                center[0] + ( self.xmin-center[0]) / self.zoom_rate, \
                center[0] + ( self.xmax-center[0]) / self.zoom_rate
            
            self.ymin, self.ymax = \
                center[1] + ( self.ymin-center[1]) / self.zoom_rate, \
                center[1] + ( self.ymax-center[1]) / self.zoom_rate

        re = np.linspace(self.xmin, self.xmax, self.width)
        im = np.linspace(self.ymin, self.ymax, self.height)

        return re[np.newaxis, :] + im[:, np.newaxis] * 1j


def main(args):
    mandelbrot = Madndelbrot(args)
    for _ in range(1000):
        mandelbrot.draw_mandelbrot()
    mandelbrot.save_gif()

if __name__ == '__main__':
    # Parse the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-it', '--iterations', type=int, default=256, help='Number of iterations')
    parser.add_argument('-w', '--width', type=int, default=512, help='The width of the canvas')
    parser.add_argument('-hh', '--height', type=int, default=512, help='The height of the canvas')
    parser.add_argument('-x', '--x', type=float, default=0.3, help='starting x coordinate')
    parser.add_argument('-y', '--y', type=float, default=0.3, help='starting y coordinate')

    args = parser.parse_args()

    main(args)