import argparse
from collections import defaultdict

IMAGE_WIDTH = 25
IMAGE_HEIGHT = 6


def read_from_file(fp):
    with open(fp) as f:
        return f.readline()


# returns a list of layers with a list of digits for each layer
def get_layers(digits):
    layer_size = IMAGE_HEIGHT*IMAGE_WIDTH
    layer_count = int(len(digits) / layer_size)
    layers = [None]*layer_count
    for i in range(layer_count):
        layers[i] = digits[:layer_size]
        digits = digits[layer_size:]
    return layers


# count the number of pixel values in each layer
def count_pixel_values(layers):
    pixel_count = [defaultdict(int) for __ in range(len(layers))]
    for i, layer in enumerate(layers):
        for digit in layer:
            pixel_count[i][digit] += 1
    return pixel_count


# returns the multiplication of number of digits 1 and 2 in the layer with fewest 0 digits
def validate_image(pixel_count):
    min_layer_count = float('inf')
    for i, layer in enumerate(pixel_count):
        if pixel_count[i]['0'] < min_layer_count:
            min_layer = i
            min_layer_count = pixel_count[i]['0']
    return pixel_count[min_layer]['1'] * pixel_count[min_layer]['2']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2019 - day 8, part 1')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()

    image_digits = read_from_file(args.input)
    layers = get_layers(image_digits)
    pixel_count = count_pixel_values(layers)
    image_val = validate_image(pixel_count)
    print(image_val)