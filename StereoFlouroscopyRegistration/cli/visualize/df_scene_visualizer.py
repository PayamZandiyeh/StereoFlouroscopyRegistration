# -*- coding: utf-8 -*-
'''Command line interface for visualizing a dual flouroscopy scene'''

import os
import click
import vtk
from StereoFlouroscopyRegistration.io.read_image import \
    get_vtk_reader_from_file_name, get_itk_homogeneous_coordinate_matrix
from StereoFlouroscopyRegistration.pipelines.df_scene_visualizer_pipeline \
    import DualFlouroSceneVisualizer

@click.command()
@click.argument('ct_file_name', type=str)
@click.argument('cam1_file_name', type=str)
@click.argument('cam2_file_name', type=str)
@click.option('--window', type=float, default=65067, help='Window to use for rendering the x-ray images')
@click.option('--level', type=float, default=32533, help='Level to use for rendering the x-ray images')
@click.option('--value', type=float, default=400, help='Value for marching cubes of the CT volume')
def df_scene(ct_file_name, cam1_file_name, cam2_file_name, window, level, value):
    '''Visualize a dual flouroscope scene.

    <ct_file_name> is expected to be a 3D file containing a CT volume.
    It will be visualized using marching cubes. Note that marching cubes
    can be slow for large volumes.

    <cam1_file_name> is expected to be a 2D file containign a X-ray image from
    the first camera. It will be visualized using a window/level transform.

    <cam2_file_name> is expected to be a 2D file containign a X-ray image from
    the second camera. It will be visualized using a window/level transform.
    '''
    # Read the files in
    readers = []
    coordinates = []
    for file_name in [ct_file_name, cam1_file_name, cam2_file_name]:
        # Read image
        reader = get_vtk_reader_from_file_name(file_name)
        if reader is None:
            os.sys.exit('Cannot find a reader for file \"{}\"'.format(file_name))
        reader.SetFileName(file_name)
        readers.append(reader)

        # Read coordinates
        coords = get_itk_homogeneous_coordinate_matrix(str(file_name))
        if coords is None:
            os.sys.exit('Cannot find an orientation matrix for file \"{}\"'.format(file_name))
        coordinates.append(coords)

    # Setup pipeline
    pipeline = DualFlouroSceneVisualizer()
    pipeline.SetCTInputConnection(readers[0].GetOutputPort())
    pipeline.SetCTOrientationMatrix(coordinates[0])
    pipeline.SetCam1InputConnection(readers[1].GetOutputPort())
    pipeline.SetCam1OrientationMatrix(coordinates[1])
    pipeline.SetCam2InputConnection(readers[2].GetOutputPort())
    pipeline.SetCam2OrientationMatrix(coordinates[2])
    pipeline.SetCamWindow(window)
    pipeline.SetCamLevel(level)
    pipeline.SetMarchingCubesValue(value)

    # Create Actor and visualize
    render_window = vtk.vtkRenderWindow()
    interactor = pipeline.set_render_window(render_window)

    # Start rendering
    interactor.Initialize()
    interactor.Start()
