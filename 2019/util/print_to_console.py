# shell colors
PRINT_WHITE = '4;30;47'
PRINT_BLACK = '6;30;40'


def print_bw_image_to_console(image:list, white_identifer, black_identifier):
    for row in range(len(image)):
        for col in range(len(image[0])):
            color = PRINT_WHITE if image[row][col] == white_identifer else PRINT_BLACK
            print('\x1b[{}m \x1b[0m'.format(color), end='')
        print('\n', end='')