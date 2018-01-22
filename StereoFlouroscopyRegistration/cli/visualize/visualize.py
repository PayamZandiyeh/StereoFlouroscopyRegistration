# -*- coding: utf-8 -*-
'''Command line interface for visualization'''

import click
from .image_visualizer import image
from .df_scene_visualizer import df_scene

@click.group()
def visualize():
    '''Various commands for visualizing medical data'''
    pass

visualize.add_command(image)
visualize.add_command(df_scene)
