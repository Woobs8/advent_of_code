import argparse
from collections import defaultdict


# image dimensions
IMAGE_WIDTH = 25
IMAGE_HEIGHT = 6


# pixel values
BLACK = '0'
WHITE = '1'
TRANSPARENT = '2'


# shell colors
PRINT_WHITE = '4;30;47'
PRINT_BLACK = '6;30;40'


def read_from_file(fp):
    with open(fp) as f:
        return f.readline()


# returns the pixel values after applying overlaying layers
def get_pixels(digits):
    image_size = IMAGE_HEIGHT*IMAGE_WIDTH
    layer_count = int(len(digits) / image_size)
    pixels = [None]*image_size
    for i in range(image_size):
        for j in range(layer_count):
            digit = digits[j*image_size+i]
            if digit == BLACK or digit == WHITE:
                pixels[i] = digit
                break
    return pixels


# renders the image in the terminal
def render_image(pixels):
    for row in range(IMAGE_HEIGHT):
        for pixel in pixels[row*IMAGE_WIDTH:(row+1)*IMAGE_WIDTH]:
            color = PRINT_WHITE if pixel==WHITE else PRINT_BLACK
            print('\x1b[{}m \x1b[0m'.format(color), end='')
        print('\n', end='')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2019 - day 8, part 2')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()

    image_digits = read_from_file(args.input)
    pixels = get_pixels(image_digits)
    render_image(pixels)