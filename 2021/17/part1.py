import argparse
from collections import namedtuple
import math

TargetArea = namedtuple('TargetArea', 'x_min x_max y_min y_max')

def read_from_file(fp:str) -> TargetArea:
    with open(fp, 'r') as f:
        line = ''.join(f.readline().strip())[len('target area: '):]
        x_range, y_range = line.split(', ')
        x_min, x_max = [int(num) for num in x_range[len('x='):].split('..')]
        y_min, y_max = [int(num) for num in y_range[len('y='):].split('..')]
        return TargetArea(x_min, x_max, y_min, y_max)

def find_valid_velocities(target_area: TargetArea) -> list:
    valid_x_velocities = []
    for v in range(1,target_area.x_max + 1):
        overshot = False
        final_velocity = v
        step = 0
        while (not overshot) and final_velocity > 0:
            final_velocity = 0 if v-step < 0 else v-step
            current_position = sum(range(final_velocity, v + 1))
            if target_area.x_min <= current_position <= target_area.x_max:
                valid_x_velocities.append((v, step, step if final_velocity > 0 else math.inf))
            elif current_position > target_area.x_max:
                overshot = True
            step += 1
    valid_velocities = []
    for vx, min_steps, max_steps in valid_x_velocities:
        # stop limit of 200 arbitrarily chosen. Is there a deterministic way to find the limit?
        step_limit = 200 if max_steps == math.inf else max_steps
        step = min_steps
        while step <= step_limit:
            vy = target_area.y_min
            # stop limit of 200 arbitrarily chosen. Is there a deterministic way to find the limit?
            while vy < 200:                    
                current_position = sum(list(range(vy-step, vy, -1)) + list(range(vy-step, vy + 1)))
                if target_area.y_min <= current_position <= target_area.y_max:
                    valid_velocities.append((vx, vy, step))
                vy += 1
            step  += 1
    return valid_velocities

def find_highest_peak(velocities: list) -> int:
    peak = -math.inf
    for __, vy, __ in velocities:
        y_position = sum(range(vy + 1))
        peak = y_position if y_position > peak else peak
    return peak

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2021 - day 17, part 1')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()
    target_area = read_from_file(args.input)
    velocities = find_valid_velocities(target_area)
    peak = find_highest_peak(velocities)
    print(peak)
    