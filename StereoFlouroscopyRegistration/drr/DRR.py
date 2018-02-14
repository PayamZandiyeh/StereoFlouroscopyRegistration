# This script generates Digitally Reconstructed Radiograph (DRR) from a given 
# 3D image to given 2D image plane(s)

# ISSUES - 
# 1- I don't know how to set the direction of the output image

import itk # imports insight Toolkit
import numpy as np
import sys
from Functions import ChangeImageDirection



#%% -------------------------------- Generated Inputs --------------------------------- 
direction = np.identity(3,dtype=np.double)
#direction[0,:] = [np.sqrt()/2,-np.sqrt(1)/2,0.] # Creating a non identity direction output just for testing. 
#direction[1,:] = [np.sqrt(1)/2, np.sqrt(3)/2,0.] # Creating a non identity direction output just for testing. 


#%% -------------------------------- INPUTS --------------------------------- 
input_filename  = '/Volumes/Storage/Projects/Registration/QuickData/OA-BEADS-CT.nii'
output_filename = '/Volumes/Storage/Projects/Registration/QuickData/test.nii'


sizeOutput = [512,512,1] # The size of output image
spaceOutput= [0.3,0.3,1] # The resolution (spacing) along x,y,z directions of output image
originOutput = [0.0,0.0,0.0] # The origin of the output 2D image plane

threshold  = 0.

rot = [90.,0.,0.]   # Rotation in degrees in x, y, and z direction. 
trs = [10. ,10. ,10.]   # translation in x, y, and z directions. 
cor = [2. ,4. ,6.]   # offset of the rotation from the center of image (3D)


directionOutput = direction # Direction of Image plane 3x3 matrix. 

focalPoint = [80.,80.,100.]  # Position of the x-ray source. 
verbose = False      # Verbose details of all steps. 

nCam = 2 # Number of cameras 


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

transform.SetRotation(np.deg2rad(rot[0]),np.deg2rad(rot[1]),np.deg2rad(rot[2])) # Setting the rotation of the transform
transform.SetTranslation(itk.Vector.D3(trs))    # Setting the translation of the transform
transform.SetComputeZYX(True)  # The order of rotation will be ZYX. 

imOrigin = inputImage.GetOrigin()                   # Get the origin of the image.
inRes    = inputImage.GetSpacing()                  # Get the resolution of the input image.
inSiz    = inputImage.GetBufferedRegion().GetSize() # Get the size of the input image.

center = itk.Point.D3(imOrigin) + np.multiply(inRes,inSiz)/2. # Setting the center of rotation as center of 3D object + offset determined by cor. 

transform.SetCenter(center)                     # Setting the center of rotation. 

if verbose :
    print(transform)
    
    
    
    
    
    
    
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
resamplefilter = FilterType.New()               # Pointer to the filter
resamplefilter.SetInput(inputImage)             # Setting the input image data 
resamplefilter.SetDefaultPixelValue( 0 )        # Setting the default Pixel value
resamplefilter.SetInterpolator(interpolator)    # Setting the interpolator
resamplefilter.SetTransform(transform)          # Setting the transform
resamplefilter.SetSize(sizeOutput)              # Setting the size of the output image. 
resamplefilter.SetOutputSpacing(spaceOutput)    # Setting the spacing(resolution) of the output image. 
resamplefilter.SetOutputOrigin(originOutput)    # Setting the output origin of the image
ChangeImageDirection(oldDirection=resamplefilter.GetOutputDirection(),newDirection=directionOutput,DimensionOut=3)     # Setting the output direction of the image  --- resamplefilter.SetImageDirection(args) was not working properly

resamplefilter.Update()                         # Updating the resample image filter.

if verbose:
    print(resamplefilter)
#%%---------------- Rescaler Image Filter --------------------------
RescalerFilterType = itk.RescaleIntensityImageFilter[InputImageType,OutputImageType]    # Defining the rescale image filter. 
rescaler = RescalerFilterType.New()             # Pointer to the rescale filter
rescaler.SetOutputMinimum(0)                    # Minimum output
rescaler.SetOutputMaximum(255)                  # Maximum output 
rescaler.SetInput(resamplefilter.GetOutput())   # Setting the input to the image filter. 

if verbose:
    print(rescaler)

#%% ------------------ Writer ------------------------------------
    # The output of the resample filter can then be passed to a writer to
    # save the DRR image to a file.
WriterType = itk.ImageFileWriter[OutputImageType]
writer = WriterType.New()

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
    