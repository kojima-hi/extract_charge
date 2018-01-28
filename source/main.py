#!/bin/usr/env python
# -*- coding: utf-8 -*-
import numpy as np
import os
from IO import get_parse
from charge import get_charges, extract_segment_esp, average_charge, check_neutral, construct_polymer_charge
from polymer import check_polymer, get_polymer_info
from parameter import get_threshold


def main():
    args = get_parse()

    all_charge = get_charges(args.input)

    if args.type == 'polymer':
        pol_info = get_polymer_info(args.condition, args.dop_go, args.dop_md)

        # check polymer by comparing number of atoms
        check_polymer(all_charge, pol_info)

        # extract charges of repeating segment
        segment_charge = extract_segment_esp(all_charge, pol_info)

        # average charges
        segment_charge = average_charge(segment_charge, pol_info['middle']['average'])

        # check neutral of segment
        segment_charge = check_neutral(segment_charge, pol_info['middle']['hydrogens'])

        # construct_polymer_charge
        construct_polymer_charge(segment_charge, pol_info, args.output)

    else:
        print('Error: type must be polymer!')
        exit()

    return


if __name__ == "__main__":
    main()