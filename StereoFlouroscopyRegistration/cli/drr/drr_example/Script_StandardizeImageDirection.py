import itk
import sys

input_filename = '/Volumes/Storage/Projects/Registration/QuickData/knee_ct_volume.nii'
output_filename = '/Volumes/Storage/Projects/Registration/QuickData/knee_ct_volume_identity.mha'
verbose = True

InputPixelType  = itk.ctype("short")
DimensionOut = 3
DimensionIn  = 3


InputImageType  = itk.Image[InputPixelType , DimensionIn]
OutputImageType = itk.Image[InputPixelType , DimensionOut]

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

#%% Change information image filter. 
FilterType = itk.ChangeInformationImageFilter[InputImageType]
filter = FilterType.New()
filter.SetInput(inputImage)
filter.SetOutputOrigin(inputImage.GetOrigin())
filter.SetOutputSpacing(inputImage.GetSpacing())
filter.ChangeDirectionOn()
filter.Update()
if verbose:
    print(filter)

#%% Thresholding
FilterThresholdType = itk.BinaryThresholdImageFilter[InputImageType,OutputImageType]
filter_threshold = FilterThresholdType.New() 

filter_threshold.SetInput(filter.GetOutput())
filter_threshold.SetLowerThreshold(500)
filter_threshold.Update()

if verbose:
    print(filter_threshold)

#%% Writer
WriterType = itk.ImageFileWriter[OutputImageType]
writer = WriterType.New()

writer.SetFileName(output_filename)
writer.SetInput(filter.GetOutput()) # set the input as the output of filtering process. 

try:
    print("Writing image: " + output_filename)
    writer.Update()
    print("Image Printed Successfully")
except ValueError: 
    print("ERROR: ExceptionObject cauth! \n")
    print(ValueError)
    sys.exit()


