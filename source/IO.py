#!/bin/usr/env python
# -*- coding: utf-8 -*-
import argparse


def get_parse():
    parser = argparse.ArgumentParser()

    parser.add_argument('--input', '-i', type=str, required=True,
                        help='Gaussian output file (input)')
    parser.add_argument('--condition', '-c', type=str, required=True,
                        help='Condition file (Input)')
    parser.add_argument('--dop_go', type=int, required=True,
                        help='Degree of polymerization in Gaussian output(Input)')
    parser.add_argument('--dop_md', type=int, required=True,
                        help='Degree of polymerization in MD(Input)')
    parser.add_argument('--output', '-o', type=str, default='esp.dat',
                        help='ESP data (output)')
    parser.add_argument('--type', type=str,
                        choices=['polymer'],
                        help='Extraction type')

    return parser.parse_args()


def main():
    return


if __name__ == "__main__":
    main()