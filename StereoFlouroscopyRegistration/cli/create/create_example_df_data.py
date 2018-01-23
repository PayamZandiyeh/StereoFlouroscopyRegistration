# -*- coding: utf-8 -*-
'''Command line interface for creating some example dual flouro data'''

import os
from builtins import input
import click
import itk

@click.command()
@click.argument('ct_file_name', type=str)
@click.argument('cam1_file_name', type=str)
@click.argument('cam2_file_name', type=str)
@click.option('--force', is_flag=True)
def df_example(ct_file_name, cam1_file_name, cam2_file_name, force):
    '''Create example dual flouro data.'''

    # Test if inputs exist
    if not force:
        for file_name in [ct_file_name, cam1_file_name, cam2_file_name]:
            if os.path.exists(file_name):
                answer = input('Output file \"{outputImage}\" exists. Overwrite? [Y/n]'.format(outputImage=file_name))
                if str(answer).lower() not in set(['yes','y', 'ye', '']):
                    os.sys.exit('Will not overwrite \"{inputFile}\". Exiting...'.
                    format(inputFile=file_name))

    # Create the image type
    dimension = 3
    pixel_type = itk.F
    ct_image_type = itk.Image[pixel_type, dimension]

    # Create orientation matricies
    cam1_direction = itk.Matrix[itk.D, dimension, dimension]()
    cam2_direction = itk.Matrix[itk.D, dimension, dimension]()

    # Create orientation such that x<-x', y<-z'
    cam1_vnl = cam1_direction.GetVnlMatrix()
    cam1_vnl.set_identity()
    cam1_vnl.put(0, 0, 0)
    cam1_vnl.put(1, 1, 0)
    cam1_vnl.put(2, 2, 0)
    cam1_vnl.put(0, 2, 1)
    cam1_vnl.put(1, 0, 1)
    cam1_vnl.put(2, 1, 1)

    # Create orientation such that x<-y', y<-z'
    cam2_vnl = cam2_direction.GetVnlMatrix()
    cam2_vnl.set_identity()
    cam2_vnl.put(0, 0, 0)
    cam2_vnl.put(1, 1, 0)
    cam2_vnl.put(2, 2, 0)
    cam2_vnl.put(0, 0, 1)
    cam2_vnl.put(1, 2, -1)
    cam2_vnl.put(2, 1, 1)

    cam1_dx = 150
    cam2_dy = 150

    # Create a Gaussian image for the CT image
    ct_source = itk.GaussianImageSource[ct_image_type].New()
    ct_source.NormalizedOff()
    ct_source.SetSigma([5, 15, 25])
    ct_source.SetScale(255)
    ct_source.SetSpacing([1, 1, 1])
    ct_source.SetOrigin([0, 0, 0])
    ct_source.SetSize([100, 100, 100])
    ct_source.SetMean([50, 50, 50])

    # Create cam1
    cam1_source = itk.GaussianImageSource[ct_image_type].New()
    cam1_source.NormalizedOff()
    cam1_source.SetSigma([5, 15, 25])
    cam1_source.SetScale(255)
    cam1_source.SetSpacing([1, 1, 1])
    cam1_source.SetOrigin([0+cam1_dx, 0, 0])
    cam1_source.SetSize([100, 100, 1])
    cam1_source.SetMean([0+cam1_dx, 50, 50])
    cam1_source.SetDirection(cam1_direction)

    # Create cam2
    cam2_source = itk.GaussianImageSource[ct_image_type].New()
    cam2_source.NormalizedOff()
    cam2_source.SetSigma([5, 15, 25])
    cam2_source.SetScale(255)
    cam2_source.SetSpacing([1, 1, 1])
    cam2_source.SetOrigin([0, 0+cam2_dy, 0])
    cam2_source.SetSize([100, 100, 1])
    cam2_source.SetMean([50, 0+cam2_dy, 50])
    cam2_source.SetDirection(cam2_direction)

    # Write them all out
    itk.imwrite(ct_source.GetOutput(), str(ct_file_name))
    itk.imwrite(cam1_source.GetOutput(), str(cam1_file_name))
    itk.imwrite(cam2_source.GetOutput(), str(cam2_file_name))
