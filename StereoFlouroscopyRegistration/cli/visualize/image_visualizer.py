# -*- coding: utf-8 -*-
'''Command line interface for slice visualizer'''

import os
import click
import vtk
from StereoFlouroscopyRegistration.io.read_image import get_vtk_reader_from_file_name
from StereoFlouroscopyRegistration.pipelines.image_slice_visualizer import ImageSliceVisualizer

@click.command()
@click.argument('file_name', type=str)
@click.option('--window', type=float, default=0, help='Window to use for rendering')
@click.option('--level', type=float, default=os.sys.float_info.min, help='Level to use for rendering (-1 means to calculate)')
def image(file_name, window, level):
    '''Visualize the slice of a medical image.

    <file_name> is expected to be a two or three dimensional file
    containing a medical image.
    '''
    # Try to read file
    reader = get_vtk_reader_from_file_name(file_name)
    if reader is None:
        os.sys.exit('Cannot find a reader for file \"{}\"'.format(file_name))
    reader.SetFileName(file_name)

    # Print inputs to screen
    click.echo('Arguments:')
    click.echo('  file_name: {}'.format(file_name))
    click.echo('  window:    {}'.format(window))
    click.echo('  level:     {}'.format(level))

    # Setup pipeline
    pipeline = ImageSliceVisualizer()
    pipeline.SetInputConnection(reader.GetOutputPort())
    pipeline.SetWindow(window)
    pipeline.SetLevel(level)

    # Create Actor and visualize
    render_window = vtk.vtkRenderWindow()
    interactor = pipeline.set_render_window(render_window)

    # Start rendering
    interactor.Initialize()
    interactor.Start()
