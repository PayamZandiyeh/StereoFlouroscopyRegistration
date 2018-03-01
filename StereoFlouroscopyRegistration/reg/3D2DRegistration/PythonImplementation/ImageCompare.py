'''ImageCompare.py based on ImageCompare.cxx writen by Bertelsen
Payam Zandiyeh Feb 16 2018 '''

#                                           Python Code
#-----------------------------------------------------------------------------------------

#%% IMPORTS 
import itk
import click
import os

#%% COMMAND LINE PREPARATIONS
@click.command()
@click.argument('file_name', type=str)
@click.option('--window', type=float, default=0, help='Window to use for rendering')
@click.option('--level', type=float, default=os.sys.float_info.min, help='Level to use for rendering (-1 means to calculate)')
def image(file_name, window, level):
    '''Visualize the slice of a medical image.'''
    click.echo('Hello World')

    
















