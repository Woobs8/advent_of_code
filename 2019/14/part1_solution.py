import argparse
from typing import Union
from collections import defaultdict
from math import ceil


def read_from_file(fp:str) -> list:
    with open(fp, 'r') as f:
        unparsed = [line.strip() for line in f.readlines()]
    return parse_reactions(unparsed)


# convert reactions to dictionary mapping chemicals to the input chemicals required to produce them
def parse_reactions(unparsed_strings:list) -> list:
    parsed_reactions = {}
    for i, line in enumerate(unparsed_strings):
        line = line.split('=>')
        output = line[1].strip().split()
        output_amount = int(output[0].strip())
        output_chemical = output[1].strip()

        # the amount of each chemical produced is stored in the first index
        chemicals = [output_amount]

        # the list of chemicals required and the amount of each is added to the list
        for chem in [chem.strip() for chem in line[0].split(',')]:
            amount, chemical = chem.split()
            chemicals.append((chemical.strip(), amount.strip()))        
        parsed_reactions[output_chemical] = chemicals
    return parsed_reactions


# calculate the minimum amount of each chemical required to produce a specified amount of a target chemical
def calc_chemical_amounts(reactions:dict, target_chem:str, target_amount:int) -> Union[dict, dict]:
    chemicals = defaultdict(int)
    surplus = defaultdict(int)
    traverse_chemical_reactions(reactions, target_chem, target_amount, chemicals, surplus)
    return chemicals, surplus


# treat the chain of reactions as a graph and recursively traverse the reactions starting from the desired chemical
def traverse_chemical_reactions(reactions:dict, target_chem:str, target_amount:int, chemicals:defaultdict(int), surplus:defaultdict(int)) -> None:       
    # the amount of each chemical required is stored
    chemicals[target_chem] += target_amount
    if target_chem == 'ORE':
        return 

    production = reactions[target_chem][0]
    reactions_required = ceil( (target_amount-surplus[target_chem]) / production )

    # the amount of surplus chemicals is stored to allow for use in other reactions
    surplus[target_chem] += (reactions_required*production) - target_amount
    for chem, amount in reactions[target_chem][1:]:
        traverse_chemical_reactions(reactions, chem, reactions_required*int(amount), chemicals, surplus)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2019 - day 14, part 1')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()
    reactions = read_from_file(args.input)
    amount, surplus = calc_chemical_amounts(reactions, 'FUEL', 1)
    print(amount['ORE'])