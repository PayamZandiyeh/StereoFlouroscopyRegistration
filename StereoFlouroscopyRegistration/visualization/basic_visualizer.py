# -*- coding: utf-8 -*-
'''Basic visualizer to show a demo'''

import vtk

def add_basic_visualizer_sub_parser(subparsers, available_visualizers):
    '''Add the parser for basic_visualizer'''
    cli_name = 'basic_visualizer'

    available_visualizers[cli_name] = basic_visualizer
    parser = subparsers.add_parser(
        cli_name,
        help='Perform a basic visualization of a CT volume with two x-ray images')

    parser.add_argument(
        '-c',
        '--ct',
        required=True,
        action='store',
        dest='ct_file_name',
        help='File name for the CT volume')

    parser.add_argument(
        '-f1',
        '--file1',
        required=True,
        action='store',
        dest='first_file_name',
        help='Filename for the first x-ray image')

    parser.add_argument(
        '-f2',
        '--file2',
        required=True,
        action='store',
        dest='second_file_name',
        help='Filename for the second x-ray image')

def basic_visualizer(args):
    '''Entry point for the basic visualizer'''
    print(args)