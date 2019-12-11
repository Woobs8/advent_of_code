import argparse
from collections import defaultdict
import sys
sys.path.append('..')
from util.print_to_console import print_bw_image_to_console


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
def get_pixels(digits, width, height):
    image_size = width*height
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
def render_image(pixels, width, height):
    # convert the list of pixels into a matrix based on the specified width and height
    image_matrix = [pixels[i:i + width] for i in range(0, len(pixels), width)]
    print_bw_image_to_console(image_matrix, WHITE, BLACK)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2019 - day 8, part 2')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()

    image_digits = read_from_file(args.input)
    pixels = get_pixels(image_digits, IMAGE_WIDTH, IMAGE_HEIGHT)
    render_image(pixels, IMAGE_WIDTH, IMAGE_HEIGHT)