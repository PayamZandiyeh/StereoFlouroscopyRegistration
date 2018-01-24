# -*- coding: utf-8 -*-
'''Command line interface for initializing dual floursocopy data.'''

import click
import inspect

@click.command()
@click.argument('input_ct_file_name', type=str)
@click.argument('cam1_directory', type=str)
@click.argument('cam2_directory', type=str)
@click.argument('cam1_calibration_file', type=str)
@click.argument('cam2_calibration_file', type=str)
@click.argument('output_ct_file_name', type=str)
@click.argument('output_cam1_file_name', type=str)
@click.argument('output_cam2_file_name', type=str)
def df_reg(input_ct_file_name, cam1_directory, cam2_directory,
    cam1_calibration_file, cam2_calibration_file, output_ct_file_name,
    output_cam1_file_name, output_cam2_file_name):

    # For now, just print what we are given
    click.echo('Arguments:')
    frame = inspect.currentframe()
    args, _, _, values = inspect.getargvalues(frame)
    for arg in args:
        click.echo('  {arg}: {value}'.format(arg=arg, value=values[arg]))
