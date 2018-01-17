# -*- coding: utf-8 -*-
'''Visualization entry point'''

from __future__ import absolute_import, print_function
import argparse
from StereoFlouroscopyRegistration.visualization.basic_visualizer import add_basic_visualizer_sub_parser

AVAILABLE_VISUALIZERS = {}

def main():
    '''Entry point for visualization command line interface.'''

    # Create visualization parsers
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='visualizer', dest='visualizer')
    add_basic_visualizer_sub_parser(subparsers, AVAILABLE_VISUALIZERS)
    args = parser.parse_args()

    AVAILABLE_VISUALIZERS[args.visualizer](args)
