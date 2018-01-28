#!/bin/usr/env python
# -*- coding: utf-8 -*-
import numpy as np
import os
from IO import get_parse
from charge import get_charges, extract_segment_esp, average_charge, check_neutral, neutralize_charge
from polymer import check_polymer, get_polymer_info
from parameter import get_threshold


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


def construct_polymer_charge(middle_charges, pol_info, path):
    middle_repeat = pol_info['dop'] - 2

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
        print('Neutral polymer construction is succeeded.')
        return
    else:
        os.remove(path)
        print('Error: Neutral polymer construction is failed.')
        exit(1)



def main():
    args = get_parse()

    all_charge = get_charges(args.input)

    if args.type == 'polymer':
        pol_info = get_polymer_info(args.condition, args.dop)

        # check polymer
        check_polymer(all_charge, pol_info)

        # extract_inter_esp
        segment_charge = extract_segment_esp(all_charge, pol_info)

        # average charges
        segment_charge = average_charge(segment_charge, pol_info['middle']['average'])

        # check neutral
        segment_charge = check_neutral(segment_charge, pol_info['middle']['hydrogens'])

        # construct_polymer_charge
        construct_polymer_charge(segment_charge, pol_info, args.output)

    else:
        print('Error: type must be polymer!')
        exit()

    return


if __name__ == "__main__":
    main()