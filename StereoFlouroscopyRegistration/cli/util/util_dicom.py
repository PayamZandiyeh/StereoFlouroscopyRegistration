# -*- coding: utf-8 -*-
'''Command line interface for converting dicom stack to something else'''

import os
from builtins import input
import click
import itk
from StereoFlouroscopyRegistration.io.read_image import get_itk_image_type

@click.command()
@click.argument('input_dicom_directory', type=str)
@click.argument('output_file_name', type=str)
@click.option('-f', '--force', is_flag=True)
@click.option('-v', '--verbose', is_flag=True)
def dicom(input_dicom_directory, output_file_name, force, verbose):
    '''Read a stack of DICOM images and convert to another image type.abs

    This script will order all the DICOM images in <input_dicom_directory>
    into an image stack and write the data out as another image type as
    specified by the extension of <output_file_name>.

    If the flag <force> is set, the script does not check if the output exists.
    Instead, it overwrites the data if it is there.

    If the flag <verbose> is set, the script will print every DICOM file it finds.

    Typically, this can be used for converting to .nii.gz.

    This script is largely based off the ITK example 'Read DICOM Series and Write 3D Image'
    '''

    # Check that the input exists
    if not os.path.isdir(input_dicom_directory):
        os.sys.exit('Input \"{}\" is not a directory. Exiting...'.format(input_dicom_directory))

    # Check if the output exists, prompt to overwrite
    if not force:
        if os.path.exists(output_file_name):
            answer = input('Output file \"{outputImage}\" exists. Overwrite? [Y/n] '.format(outputImage=output_file_name))
            if str(answer).lower() not in set(['yes','y', 'ye', '']):
                os.sys.exit('Will not overwrite \"{inputFile}\". Exiting...'.
                format(inputFile=output_file_name))

    # Create the reader
    click.echo('Gathering dicom names from {}'.format(input_dicom_directory))
    names_generator = itk.GDCMSeriesFileNames.New()
    names_generator.SetInputDirectory(str(input_dicom_directory))
    names_generator.SetGlobalWarningDisplay(False)
    names_generator.SetUseSeriesDetails(True)
    input_file_names = names_generator.GetInputFileNames()

    # Print info
    click.echo('  Found {} files'.format(len(input_file_names)))
    if verbose:
        for idx, file_name in enumerate(input_file_names):
            click.echo('  File {: >8}: {}'.format(idx, file_name))

    # Determine pixel type and read in stack
    click.echo('Reading DICOM files into a stack')
    image_type = get_itk_image_type(input_file_names[0])
    reader = itk.ImageSeriesReader[image_type].New()
    dicomIO = itk.GDCMImageIO.New()
    reader.SetImageIO(dicomIO)
    reader.SetFileNames(input_file_names)
    reader.Update()

    # Write out
    click.echo('Writing to {}'.format(output_file_name))
    itk.imwrite(reader.GetOutput(), str(output_file_name))
