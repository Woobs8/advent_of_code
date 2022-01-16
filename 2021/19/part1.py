import argparse
from itertools import chain
from collections import defaultdict, Counter
from itertools import groupby

def read_from_file(fp:str) -> list:
    with open(fp, 'r') as f:
        scanner_reports = []
        scanner = []
        lines = f.read().splitlines()
        for i, line in enumerate(lines):
            if '--- scanner' in line:
                if len(scanner) > 0:
                    scanner_reports.append(scanner)
                scanner = []
            elif line != '':
                x,y,z = line.split(',')
                scanner.append((int(x), int(y), int(z)))
        if len(scanner) > 0:
            scanner_reports.append(scanner)
        return scanner_reports


# Algorithm for mapping scanners
# 1. Find adjacent scanner pairs and overlapping beacons for each pair
# 2. Add scanner 0 to mapped region (it now defines the reference frame)
# 3. Loop while there are mapped scanners whose adjacent scanners have not yet been checked
#   a. Select mapped scanner with unchecked adjacent scanners
#   b. For every scanner adjacent to selected scanner
#       i. If adjacent scanner not already mapped then translate adjacent scanner to reference frame based on overlapping beacons
#       j. Add scanner position and translated beacon to result
def construct_map(scanner_reports: list) -> (list, list):
    beacon_map = [None] * len(scanner_reports)
    beacon_map[0] = scanner_reports[0]
    adjacent_scanners, overlapping_beacons = find_scanner_pairs(scanner_reports)
    scanner_map = [None] * len(scanner_reports)
    scanner_map[0] = [0,0,0]
    mapped_scanners = [0]
    while len(mapped_scanners) > 0:
        ref_scanner_idx = mapped_scanners.pop()
        for scanner_idx in adjacent_scanners[ref_scanner_idx]:
            if scanner_map[scanner_idx] is None:
                scanner_position, translated_beacons = translate_scanner_to_reference_frame(scanner_reports[scanner_idx], beacon_map[ref_scanner_idx], overlapping_beacons[(ref_scanner_idx, scanner_idx)])
                beacon_map[scanner_idx] = translated_beacons
                mapped_scanners.append(scanner_idx)
                scanner_map[scanner_idx] = scanner_position
    return scanner_map, beacon_map

# Algorithm for finding scanner pairs
# 1. Calculate distance between every beacon detected by each scanner
# 2. Find the overlapping beacons between each scanner by assuming the set of intra-scanner manhattan distances between beacon is a unique identifier for a beacon pattern (This does not hold for all scenarios, but works for this exercise)
# 3. If there are overlapping beacons, add the scanners as an adjacent pair
def find_scanner_pairs(scanner_reports: list) -> (dict, dict):
    adjacent_scanners = defaultdict(list)
    overlapping_scanner_beacons = {}
    intra_scanner_distances = calc_intra_scanner_distances(scanner_reports)
    for i, distances1 in enumerate(intra_scanner_distances):
        for j, distances2 in enumerate(intra_scanner_distances):
            if i != j and (not j in adjacent_scanners[i]):
                overlapping_beacons = find_overlapping_beacons(distances1, distances2)
                if len(overlapping_beacons) > 0:
                    adjacent_scanners[i].append(j)
                    overlapping_scanner_beacons[(i,j)] = overlapping_beacons
    return adjacent_scanners, overlapping_scanner_beacons

def calc_intra_scanner_distances(scanner_reports: list) -> list:
    intra_scanner_distances = []
    for beacons in scanner_reports:
        distances = [[] for __ in range(len(beacons))]
        for i, beacon1 in enumerate(beacons):
            for j, beacon2 in enumerate(beacons):
                if i != j:
                    distances[i].append(sum([abs(beacon1[0] - beacon2[0]), abs(beacon1[1] - beacon2[1]), abs(beacon1[2] - beacon2[2])]))
        intra_scanner_distances.append(distances)
    return intra_scanner_distances

# Algorithm for finding the overlapping beacons between two scanners
# 1. For every list of distance corresponding to a beacon in scanner #1, iterate the lists of distances for every beacon in scanner #2
#   a. If beacon #2 is not already matched and if the two beacons have an overlap of 11 or more distances, then they are considered a match
#   b. Add beacon #2 to list of matched beacons
#   c. Add overlapping beacons to result
def find_overlapping_beacons(distances1: list, distances2: list) -> list:
    overlapping_beacons = []
    mapped_beacons = []
    for i, beacon1 in enumerate(distances1):
        for j, beacon2 in enumerate(distances2):
            if (not j in mapped_beacons) and is_overlapping(beacon1, beacon2, 11):
                overlapping_beacons.append((i,j))
                mapped_beacons.append(j)
    return overlapping_beacons if len(overlapping_beacons) >= 11 else []

def is_overlapping(beacon1: list, beacon2: list, overlap_threshold: int) -> bool:
    c1 = Counter(beacon1)
    c2 = Counter(beacon2)
    overlap = 0
    for key in c1.keys():
        overlap += c2[key]
    return overlap >= overlap_threshold

# Algorithm for translating scanner with unknown orientation
# Initialize reference axis as 0
# 1. Loop while scanner's position has unknown dimensions
#   a. For each orientation (axes adn direction)
#       i. Find translation vector along axis for each overlapping beacon by subtracting the local location from the reference location
#       j. If the translation vector is identical for all beacons, the orientation has been found
#   b. Increment reference axis
# 2. Once scanner position and orientation (in the reference frame) has been found, translate each beacon to the reference frame
def translate_scanner_to_reference_frame(scanner_beacons: list, ref_scanner_beacons: list, overlapping_beacons: list) -> ((int, int, int), list):
    scanner_position = [None, None, None]
    orientations = [(0, -1),(0, 1),(1, -1), (1, 1), (2, -1), (2, 1)]
    ref_axis = 0
    scanner_orientation = [None, None, None]
    while None in scanner_position:
        for axis, direction in orientations:
            candidate_translation = [ref_scanner_beacons[ref_i][ref_axis] - scanner_beacons[i][axis]*direction for ref_i, i in overlapping_beacons]
            if all_equal(candidate_translation):
                scanner_position[ref_axis] = candidate_translation[0]
                scanner_orientation[ref_axis] = (axis,direction)
                orientations.remove((axis, direction))
                break
        ref_axis += 1
    translation_vector = (scanner_position[0], scanner_position[1], scanner_position[2])
    return scanner_position, translate_beacons(scanner_beacons, translation_vector, scanner_orientation)
    
def all_equal(iterable):
    g = groupby(iterable)
    return next(g, True) and not next(g, False)

def translate_beacons(beacons: list, translation_vector: tuple, orientation: list) -> list:
    translated_beacons = []
    for beacon in beacons:
        x = orientation[0][1] * beacon[orientation[0][0]] + translation_vector[0]
        y = orientation[1][1] * beacon[orientation[1][0]] + translation_vector[1]
        z = orientation[2][1] * beacon[orientation[2][0]] + translation_vector[2]
        translated_beacons.append((x,y,z))
    return translated_beacons

def unique_beacons(beacon_map: list) -> int:
    return len(set(chain.from_iterable(beacon_map)))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2021 - day 19, part 1')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()
    scanner_reports = read_from_file(args.input)
    scanner_map, beacon_map = construct_map(scanner_reports)
    beacon_count = unique_beacons(beacon_map)
    print(beacon_count)