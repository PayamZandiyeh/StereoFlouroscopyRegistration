# -*- coding: utf-8 -*-
'''Command line interface for slice visualizer'''

import click

@click.command()
@click.argument('file_name', type=str)
def image(file_name):
    '''Read in a 2D image and visualize it.

    <file_name> is expected to be a two dimensional file
    containing a medical image.
    '''
    click.echo('Hello {}!'.format(file_name))
