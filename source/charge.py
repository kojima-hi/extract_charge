#!/bin/usr/env python
# -*- coding: utf-8 -*-
import numpy as np
from parameter import get_power_float2int, get_digit, get_threshold


def average_charge(charges, average_lst):

    for lst in average_lst:
        extracts = charges[lst]
        average = extracts.mean()
        charges[lst] = average

    return np.round(charges, get_digit())


def neutralize_charge(charges, hydrogens):
    # for calculation on integer
    power_float2int = get_power_float2int()

    # sum charges on integer
    charges_i = (charges * power_float2int).astype(np.int32)
    charge_sum = charges_i.sum()

    # calculate remainder
    num_hydrogens = hydrogens.size
    remainder = charge_sum % num_hydrogens

    # processing for neutralization
    charge_subtract = int((charge_sum - remainder) / num_hydrogens)
    charges_i[hydrogens] -= charge_subtract
    charges_i[hydrogens[:remainder]] -= 1

    return charges_i.astype(np.float32) / power_float2int


def check_neutral(charges, hydrogens):
    charges = neutralize_charge(charges, hydrogens)
    charge_sum = charges.sum()
    if abs(charge_sum) < get_threshold():
        return charges
    else:
        print('Error: segment is not neutral:', charge_sum)
        exit(1)


def get_charges(path):

    identity_string='Charges from ESP fit'
    charges = []
    with open(path, 'r') as f:
        for line in f:
            if identity_string in line:

                # skip lines
                for _ in range(2):
                    f.readline()

                # extract charges
                for line in f:
                    if identity_string in line:
                        break

                    items = (line.strip()).split()
                    charges.append(items[2])

    return np.array(charges, dtype=np.float32)


def extract_segment_esp(all_charge, pol_info):
    # calculate skip atoms for extraction from center
    noa_middle = pol_info['middle']['num']
    noa_head = pol_info['head']['num']
    skip_middle_num = int(((pol_info['dop'] - 1) / 2) - 1)
    skip_atoms = noa_head + (pol_info['middle']['num'] * skip_middle_num)

    # extract
    start = skip_atoms + 0
    segment_charge = np.zeros(noa_middle, dtype=np.float32)
    segment_charge[0: noa_middle] = all_charge[start: start + noa_middle]

    return segment_charge


def main():
    return


if __name__ == "__main__":
    main()