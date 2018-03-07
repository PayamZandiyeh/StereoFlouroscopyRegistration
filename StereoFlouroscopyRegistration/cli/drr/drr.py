import click
import itk # imports insight Toolkit
import numpy
import sys
import datetime
import StereoFlouroscopyRegistration.util.itk_helpers as Functions
import StereoFlouroscopyRegistration.cli.drr.calibration_joint_track as CalibrationUsingJointTrack
import os

@click.command()

# ARGUMENTS
@click.argument('input_filename', type=click.Path(exists=True), required=True)
@click.argument('output_directory',type=click.Path(exists=True))
@click.argument('calibration_files', nargs=-1, type=click.Path(),required=True)

# OPTIONS
@click.option('--output_extension',default='.nii',help='The extension for the type of image [default : .nii]')
@click.option('--threshold',type=float,default=0.,help='Threshold [default: 0]')
@click.option('--min_out',type=int,default=0,help='Minimum gray scale in the output image.   [default=0  ]')
@click.option('--max_out',type=int,default=255,help='Maximum gray scale in the output image. [default=255]')
@click.option('--default_pixel_value',type=int,default=0,help='Default pixel value in the output image [default=0]')
@click.option('--rot',nargs=3,type=float,default=[0.,0.,0.],help='[float,float,float]: Rotation around x,y,z axes in degrees')
@click.option('--t',nargs=3,type=float,default=[0.,0.,0.],help='[float,float,float]: Translation parameters of the 3D object')
@click.option('--cor',nargs=3,type=float,default=[0.,0.,0.],help='[float,float,float]: The centre of rotation relative to center of volume')
@click.option('--n_cam',type=int,default=2,help='Number of cameras (x-ray sources)')
@click.option('--res',nargs= 2, default=[0.27,0.27],type=float,help='[float, float]: Pixel spacing (resolution) of the output image [default: 0.27x0.27mm]')
@click.option('--size',nargs=2, type=int, default=[512,512],help='[int,int]: Dimension of output image [default : 512x512]')
@click.option('--transformed_vol',default=False,help='prints the  3D volume in the destination folder after the transfomration [default: False]')
# VERBOSE OPTION
@click.option('--verbose','-v',is_flag=True, help="Will print in a verbose mode")


def drr(input_filename,output_directory,calibration_files,output_extension,threshold,min_out,max_out,default_pixel_value,rot,t,cor,n_cam,res,size,transformed_vol,verbose):
    """This function generates digitally reconstructed radiographs based on the 
       Calibration information provided. """
       
    click.echo('  inputFileName         : {}'.format(input_filename))
    click.echo('  out_directory         : {}'.format(output_directory))
    click.echo('  outputExtension       : {}'.format(output_extension))
    click.echo('  Verbose Status        : {}'.format(verbose))
    click.echo('  Pixel Size            : {}'.format(res))
    click.echo('  Output image Size     : {}'.format(size))
    click.echo('  Translation           : {}'.format(t))
    click.echo('  Rotation              : {}'.format(rot))
    click.echo('  Centre of Rotation    : {}'.format(cor))
    click.echo('  Threshold             : {}'.format(threshold))
    click.echo('  Number of Cameras     : {}'.format(n_cam))    
    click.echo('  Minimum Out           : {}'.format(min_out))
    click.echo('  Maximum Out           : {}'.format(max_out))
    click.echo('  Calibration Files     : {}'.format(calibration_files)) 
    
    if len(calibration_files) != n_cam :
        raise Exception('Number of Calibration files', len(calibration_files),'do not correspond with the number of Cameras',n_cam)
    
    #%%------------------ Starting the main body of the code ---------------- 
    # -------------------- Reader -------------------------
    InputPixelType  = itk.ctype("short")
    OutputPixelType = itk.ctype("short")
    ScalarType = itk.D
    DimensionIn  = 3
    DimensionOut = 3
    
    InputImageType  = itk.Image[InputPixelType , DimensionIn ]
    OutputImageType = itk.Image[OutputPixelType, DimensionOut]
    
    
    ReaderType = itk.ImageFileReader[InputImageType]
    reader     = ReaderType.New()
    reader.SetFileName(input_filename)
    
    try:
        print("Reading image: " + input_filename)
        reader.Update()
        print("Image Read Successfully")
    except ValueError: 
        print("ERROR: ExceptionObject cauth! \n")
        print(ValueError)
        sys.exit()
        
    inputImage = reader.GetOutput()
    
    if verbose :
        print(inputImage)
        
    
    #%% ------------------ Transformation 
    # This part is inevitable since the interpolator (Ray-cast) and resample Image
    # image filter uses a Transformation -- Here we set it to identity. 
    TransformType = itk.CenteredEuler3DTransform[itk.D]
    transform     = TransformType.New()
    
    transform.SetRotation(numpy.deg2rad(rot[0]),numpy.deg2rad(rot[1]),numpy.deg2rad(rot[2])) # Setting the rotation of the transform
    transform.SetTranslation(itk.Vector.D3(t))    # Setting the translation of the transform
    transform.SetComputeZYX(True)  # The order of rotation will be ZYX. 
    
    imOrigin = inputImage.GetOrigin()                   # Get the origin of the image.
    inRes    = inputImage.GetSpacing()                  # Get the resolution of the input image.
    inSiz    = inputImage.GetBufferedRegion().GetSize() # Get the size of the input image.
    
    center = itk.Point.D3(imOrigin) + numpy.multiply(inRes,inSiz)/2. # Setting the center of rotation as center of 3D object + offset determined by cor. 
    
    transform.SetCenter(center)                     # Setting the center of rotation. 
    
    if verbose :
        print(transform)
        
       #%% 
    for ii in range(n_cam):
        imageCalibrationInfo = CalibrationUsingJointTrack.CalibrationTool() # Setting up the image calibration info class. 
        imageCalibrationInfo.SetCalibrationInfo(calibration_files[ii]) # Assign the information from the calibration file to the imageCalibrationInfo class. 
        
        spaceOutput= imageCalibrationInfo.GetPixelSize() # The resolution (spacing) along x,y,z directions of output image
        
        imageCalibrationInfo.SetOutputImageSize(size[0],size[1],1)  # Setting the size of the output image. 
        imageCalibrationInfo.SetGlobalOriginForImagePlane()               # Setting the global origin of the output image. 
        
        originOutput = imageCalibrationInfo.GetGlobalOriginForImagePlane() # Setting the output origin. 
        
        directionOutput = imageCalibrationInfo.GetDirectionMatrix() # Direction of Image plane 3x3 matrix. 
        focalPoint = imageCalibrationInfo.GetFocalPoint()  # Position of the x-ray source. 
        
        #%% ----------------- Ray Cast Interpolator 
        # In this part the Ray Cast interpolator is defined and applied to the input
        # image data. 
        
        InterpolatorType = itk.RayCastInterpolateImageFunction[InputImageType,ScalarType]       # Defining the interpolator type from the template. 
        interpolator     = InterpolatorType.New()               # Pointer to the interpolator
        
        interpolator.SetInputImage(inputImage)                  # Setting the input image data
        interpolator.SetThreshold(threshold)                    # Setting the output threshold
        interpolator.SetFocalPoint(itk.Point.D3(focalPoint))    # Setting the focal point (x-ray source location)
        interpolator.SetTransform(transform)                    # Setting the transform (here identity)
        
        if verbose:
            print(interpolator)
        #%%----------------- Resample Image Filter ------------------------
            # In this part the resample image filter to map a 3D image to 2D image plane with desired specs is designed
            
        FilterType = itk.ResampleImageFilter[InputImageType,OutputImageType]                    # Defining the resample image filter type. 
        resamplefilter = FilterType.New()                                                       # Pointer to the filter
        resamplefilter.SetInput(inputImage)                                                     # Setting the input image data 
        resamplefilter.SetDefaultPixelValue(default_pixel_value)                                  # Setting the default Pixel value
        resamplefilter.SetInterpolator(interpolator)                                            # Setting the interpolator
        resamplefilter.SetTransform(transform)                                                  # Setting the transform
        resamplefilter.SetSize([size[0],size[1],1])                                             # Setting the size of the output image. 
        resamplefilter.SetOutputSpacing(itk.Vector.D3([spaceOutput[0],spaceOutput[1],1]))       # Setting the spacing(resolution) of the output image. 
        resamplefilter.SetOutputOrigin(originOutput)                                            # Setting the output origin of the image
        Functions.ChangeImageDirection(oldDirection=resamplefilter.GetOutputDirection(),newDirection=directionOutput,DimensionOut=3)     # Setting the output direction of the image  --- resamplefilter.SetImageDirection(args) was not working properly
        
        resamplefilter.Update()                                                                 # Updating the resample image filter.
        
        if verbose:
            print(resamplefilter)
        #%%---------------- Rescaler Image Filter --------------------------
        RescalerFilterType = itk.RescaleIntensityImageFilter[InputImageType,OutputImageType]    # Defining the rescale image filter. 
        rescaler = RescalerFilterType.New()             # Pointer to the rescale filter
        rescaler.SetOutputMinimum(min_out)               # Minimum output
        rescaler.SetOutputMaximum(max_out)               # Maximum output 
        rescaler.SetInput(resamplefilter.GetOutput())   # Setting the input to the image filter. 
        rescaler.Update() 
        
        if verbose:
            print(rescaler)
        
           #%% ------------------ Writer ------------------------------------
    # The output of the resample filter can then be passed to a writer to
    # save the DRR image to a file.
        WriterType = itk.ImageFileWriter[OutputImageType]
        writer = WriterType.New()
        
        outputPath = os.path.join(output_directory,'Cam')+str(ii+1)
        
        if not os.path.exists(outputPath):
            os.mkdir(outputPath)
        
        if ii == 0:
            time = datetime.datetime.now() 
            dummy = ('rx'+str(int(rot[0]))+'ry'+str(int(rot[1]))+'rz'+str(int(rot[2]))+'tx'
                         + str(int(t[0]))+'ty'+str(int(t[1]))+'tz'+str(int(t[2]))+'y'+str(time.year)+'m'+str(time.month)
                         +'d'+str(time.day)+'hr'+str(time.hour)+'m'+str(time.minute)+'s'+str(time.second)+ output_extension)
            
        outputName = 'Cam'+str(ii+1)+dummy
        output_filename = str(os.path.join(outputPath,outputName))
        
        writer.SetFileName(output_filename)
        # writer.SetFileName('/Volumes/Storage/Payam/Desktop/output.nii')  
        writer.SetInput(rescaler.GetOutput())
        
        try:
            print("Writing image: " + output_filename)
            writer.Update()
            print("Image Printed Successfully")
        except ValueError: 
            print("ERROR: ExceptionObject cauth! \n")
            print(ValueError)
            sys.exit()
        
        
            # Writing the transformed volume
        if transformed_vol:
            WriterType=itk.ImageFileWriter[InputImageType]
            writer3d=WriterType.New()
            
            output_filename3d = os.path.join(output_directory,'TransformedVolume'+output_extension)
            writer3d.SetFileName(output_filename3d)
            writer3d.SetInput(resamplefilter.GetOutput())
            
            try:
                print("Writing the transformed Volume at : " + output_filename3d)
                writer.Update()
                print("Volume Printed Successfully")
            except ValueError: 
                print("ERROR: ExceptionObject cauth! \n")
                print(ValueError)
                sys.exit()
        
if __name__ =='__main__':
    drr()

