# This script generates Digitally Reconstructed Radiograph (DRR) from a given 
# 3D image to given 2D image plane(s)


#%% -------------------------------- INPUTS ----------------------------------- 
input_filename  = '/Volumes/Storage/Projects/Registration/QuickData/OA-BEADS-CT.nii'
output_directory = '/Volumes/Storage/Projects/Registration/QuickData/'
output_extension = '.nii' # Store the output image in nifti format. 
threshold  = 0.
default_pixel_value = 0
min_out = 0
max_out = 255

rot = [90.,0.,0.]   # Rotation in degrees in x, y, and z direction. 
t   = [10. ,10. ,10.]   # translation in x, y, and z directions. 
cor = [2. ,4. ,6.]   # offset of the rotation from the center of image (3D)

size = [512,512] # The size of output image


verbose = False      # Verbose details of all steps. 

n_cam = 2 # Number of cameras 
calibration_files = ['/Volumes/Storage/Projects/Registration/QuickData/OAKneeCadaverCd001_NM_Cam1.txt' ,    # Calibration file for Camera 1
                   '/Volumes/Storage/Projects/Registration/QuickData/OAKneeCadaverCd001_NM_Cam2.txt' ]    # Calibration file for Camera 2
transformed_vol = False # To print the transformed volume with the name TransformedVolume

#%% ------------------------------- Import Libraries ------------------------
import itk # imports insight Toolkit
import numpy
import sys
import datetime
import StereoFlouroscopyRegistration.util.itk_helpers as Functions
import StereoFlouroscopyRegistration.cli.drr.calibration_joint_track as CalibrationUsingJointTrack
import os

#%%


 

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
    Functions.change_image_direction(oldDirection=resamplefilter.GetOutputDirection(),newDirection=directionOutput,DimensionOut=3)     # Setting the output direction of the image  --- resamplefilter.SetImageDirection(args) was not working properly
    
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
        
        outputName = ('Cam'+str(ii+1)+'rx'+str(int(rot[0]))+'ry'+str(int(rot[1]))+'rz'+str(int(rot[2]))+'tx'
                     + str(int(t[0]))+'ty'+str(int(t[1]))+'tz'+str(int(t[2]))+'y'+str(time.year)+'m'+str(time.month)
                     +'d'+str(time.day)+'hr'+str(time.hour)+'m'+str(time.minute)+'s'+str(time.second)+ output_extension)
    
    output_filename = os.path.join(outputPath,outputName)
    
    writer.SetFileName(output_filename)
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