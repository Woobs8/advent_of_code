import argparse
from itertools import chain

def read_from_file(fp:str) -> (list, list):
    with open(fp, 'r') as f:
        algorithm = f.readline().strip()
        f.readline()
        image = []
        for line in f.read().splitlines():
            image.append(line)
        return algorithm, image

def sequential_enhances(image: list, algorithm: list, n_times: int) -> list:
    output_image = image
    out_of_bounds = '.'
    for __ in range(n_times):
        output_image, out_of_bounds = enhance(output_image, algorithm, out_of_bounds)
    return output_image

def enhance(image: list, algorithm: list, out_of_bounds: str) -> list:
    output_image = []
    height = len(image)
    width = len(image[0])
    for y in range(-1,height + 1):
        row = []
        for x in range(-1,width + 1):
            pixel_value = calc_pixel_value((x,y), image, out_of_bounds)
            row.append(algorithm[pixel_value])
        output_image.append(row)
    out_of_bounds = algorithm[int(''.join(['1' if bit == '#' else '0' for bit in out_of_bounds*9]), 2)]
    return output_image, out_of_bounds

def calc_pixel_value(pixel: tuple, image: list, out_of_bounds: str) -> int:
    x, y = pixel
    pixel_value = ''
    for yi in range(y-1,y+2):
        for xi in range(x-1, x+2):
            pixel_value += image[yi][xi] if 0 <= yi < len(image) and 0 <= xi < len(image[yi]) else out_of_bounds
    return int(''.join(['1' if bit == '#' else '0' for bit in pixel_value]), 2)

def print_image(image: list) -> None:
    for line in image:
        print(''.join(line))

def count_lit_pixels(image: list) -> int:
    lit_pixels = 0
    for pixel in chain.from_iterable(image):
        lit_pixels += 1 if pixel == '#' else 0
    return lit_pixels

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2021 - day 20, part 1')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()
    algorithm, image = read_from_file(args.input)
    enhanced_image = sequential_enhances(image, algorithm, 2)
    lit_pixels = count_lit_pixels(enhanced_image)
    print(lit_pixels)