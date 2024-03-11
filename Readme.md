# Poetry Python  Project

This project contains scripts that produce generative art.

## Installation

To install the project, run the following command:

`poetry install`

##  Usage

To use the project, run the following command:

`poetry run python main.py`

### Usage

#### Mandelbrot
To use the program, run the following command:

```
python mandelbrot.py -it <iterations> -w <width> -hh <height> -x <x> -y <y> -z <zoom>
```
where:
```
-it: Number of iterations (default: 256)
-w: Canvas width in pixels (default: 512)
-hh: Canvas height in pixels (default: 512)
-x: Starting x coordinate (default: 0.5)
-y: Starting y coordinate (default: 0.5)
-z: Number of zoom iterations (default: 200)
```

e.g
```
python mandelbrot.py -it 1000 -w 1024 -hh 1024 -z 200
```

#### Squares
To use the program, run the following command:

```
python squares.py -r <rows> -c <columns> -min <min_size> -max <max_size>
```
where:
```
-r: Number of rows (default: 10)
-c: Number of columns (default: 10)
-min: Minimum size of squares in pixels (default: 10)
-max: Maximum size of squares in pixels (default: 100)
```
eg.:

```
python squares.py -r 20 -c 20 -min 20 -max 100
```

## License

This project is licensed under the MIT License.