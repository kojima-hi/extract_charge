#!/bin/usr/env python
# -*- coding: utf-8 -*-
import numpy as np


def check_polymer(all_charge, pol_info):
    num_charges = all_charge.size

    # calculate number of atoms in polymer
    dop_middle = pol_info['dop_go'] - 2
    num_atoms = pol_info['middle']['num'] * dop_middle + pol_info['head']['num'] + pol_info['tail']['num']

    if num_charges == num_atoms:
        return
    else:
        print('Error: contradiction between number of charges and number of atoms.')
        exit(1)


def get_end_info(end_type, num_atom_middle):
    info = {}

    n = num_atom_middle
    average_lst = []
    copy_lst = []
    if 'h' == end_type:
        info['num'] = 1 + num_atom_middle

        # copy info
        info['copy'] = copy_lst

        # average info
        average_lst.append(np.array([2, 3, n+1], dtype=np.int32) - 1)
        info['average'] = average_lst

        # hydrogens info
        info['hydrogens'] = np.array([2, 3, n+1], dtype=np.int32) - 1

    elif 'ch3' == end_type:
        info['num'] = 4 + num_atom_middle

        # copy info
        copy_lst.append(np.array([1, n+1]) - 1) # [from, to]
        copy_lst.append(np.array([2, n+2]) - 1)
        copy_lst.append(np.array([3, n+3]) - 1)
        info['copy'] = copy_lst

        # average info
        average_lst.append(np.array([n+2, n+3, n+4], dtype=np.int32) - 1)
        info['average'] = average_lst

        # hydrogens info
        info['hydrogens'] = np.array([n+2, n+3, n+4], dtype=np.int32) - 1

    else:
        print('Error: ', end_type, 'is not assisted.')
        exit(1)

    return info


def get_average_info(info):
    ave_info = []

    items = info.split(';')
    for item in items:
        nums = np.array(item.split(','), dtype=np.int32)
        nums -= 1 # convert start-number from 1 to 0
        ave_info.append(nums)

    return ave_info

def get_hydrogens_info(info):
    return np.array(info.split(','), dtype=np.int32) - 1 # convert start-number from 1 to 0


def get_polymer_info(path_cnd, dop_go, dop_md):
    pol_info = {'dop_go': dop_go, 'dop_md': dop_md}

    num_atom_middle = None
    with open(path_cnd, 'r') as f:
        for line in f:
            items = (line.strip()).split('=')

            if 'num_atom_middle' == items[0]:
                num_atom_middle = int(items[1])
                pol_info['middle'] = {'num': num_atom_middle}
            elif 'head_type' == items[0]:
                pol_info['head'] = get_end_info(items[1], num_atom_middle)
            elif 'tail_type' == items[0]:
                pol_info['tail'] = get_end_info(items[1], num_atom_middle)
            elif 'average' == items[0]:
                pol_info['middle']['average'] = get_average_info(items[1])
            elif 'hydrogens' == items[0]:
                pol_info['middle']['hydrogens'] = get_hydrogens_info(items[1])
            else:
                print('Error: unknown data in polymer information.')
                exit(1)

    return pol_info


def main():
    return


if __name__ == "__main__":
    main()