# -*- coding: utf-8 -*-
'''Command line interface for visualization'''

import click
from .image_visualizer import image

@click.group()
def visualize():
    '''Visualize a medical image'''
    pass

visualize.add_command(image)
