import argparse
from typing import Union
from collections import defaultdict
from math import ceil
from functools import reduce
from fractions import gcd
from time import sleep

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


# calculates the amount of a target chemical that can be produced from a specified amount of ore
def chem_from_ore(reactions:dict, target_chem:str, ore_amount:int) -> int:
    ore_per_fuel = unadjusted_ore_per_chem(reactions, target_chem)
    
    # do a binary seacrch of production amount to find the amount that consumes the most ore without exceeding the available amount
    lower_bound = ore_amount // ore_per_fuel
    upper_bound = ore_amount
    while lower_bound <= upper_bound:
        chemicals = defaultdict(int)
        surplus = defaultdict(int)
        production = lower_bound + (upper_bound - lower_bound)//2
        traverse_chemical_reactions(reactions, target_chem, production, chemicals, surplus)
        spare_ore = ore_amount - chemicals['ORE']
        if spare_ore < ore_per_fuel and spare_ore > 0:
            break
        
        if chemicals['ORE'] > ore_amount:
            upper_bound = production-1
        else:
            lower_bound = production+1
    return production


# calculate the minimum amount of each chemical required to produce 1 of a target chemical
def unadjusted_ore_per_chem(reaction:dict, target_chem:str) -> int:
    chemicals = defaultdict(int)
    surplus = defaultdict(int)
    traverse_chemical_reactions(reactions, target_chem, 1, chemicals, surplus)
    return chemicals['ORE']


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
    parser = argparse.ArgumentParser(prog='Advent of code 2019 - day 14, part 2')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()
    reactions = read_from_file(args.input)
    fuel_production = chem_from_ore(reactions,'FUEL', 10**12)
    print(fuel_production)