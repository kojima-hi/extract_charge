#!/bin/usr/env python
# -*- coding: utf-8 -*-
import numpy as np
from parameter import get_power_float2int, get_digit, get_threshold


def construct_end_charge(middle_charges, end_charges, end_info):
    # copy charge
    end_charges[0:middle_charges.size] = middle_charges[0:middle_charges.size]
    for copy in end_info['copy']:
        end_charges[copy[1]] = middle_charges[copy[0]]

    # average
    end_charges = average_charge(end_charges, end_info['average'])

    # neutralize
    end_charges = check_neutral(end_charges, end_info['hydrogens'])

    return end_charges


def check_neutral_file(path):

    with open(path, 'r') as f:
        n_atom = int(f.readline())
        chg_sum = 0.0
        for _ in range(n_atom):
            chg = float(f.readline())
            chg_sum += chg

    if abs(chg_sum) < get_threshold():
        return True
    else:
        return False


def write_each_parts(path, head_charges, middle_charges, tail_charges):

    strs = ['middle:', 'head:', 'tail:']
    chg_parts = [middle_charges, head_charges, tail_charges]
    with open(path, 'w') as f:
        for str, chg_part in zip(strs, chg_parts):
            f.write('%s\n'%(str))
            for chg in chg_part:
                f.write('%10.6f\n'%(chg))
            f.write('\n')

    return


def construct_polymer_charge(middle_charges, pol_info, path):
    middle_repeat = pol_info['dop_md'] - 2

    head_charges = np.zeros(pol_info['head']['num'], dtype=np.float32)
    head_charges = construct_end_charge(middle_charges, head_charges, pol_info['head'])

    tail_charges = np.zeros(pol_info['tail']['num'], dtype=np.float32)
    tail_charges = construct_end_charge(middle_charges, tail_charges, pol_info['tail'])

    n_atom = head_charges.size + middle_charges.size*middle_repeat + tail_charges.size
    with open(path, 'w') as f:
        f.write('%10i\n'%(n_atom))
        for chg in head_charges:
            f.write('%10.6f\n'%(chg))
        for _ in range(middle_repeat):
            for chg in middle_charges:
                f.write('%10.6f\n'%(chg))
        for chg in tail_charges:
            f.write('%10.6f\n'%(chg))

    if check_neutral_file(path):
        write_each_parts(path+'.segment', head_charges, middle_charges, tail_charges)
        print('Neutral polymer construction is succeeded.')
        return
    else:
        os.remove(path)
        print('Error: Neutral polymer construction is failed.')
        exit(1)



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
    skip_middle_num = int(((pol_info['dop_go'] - 1) / 2) - 1)
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