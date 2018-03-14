#%----------------- Resample Image Filter ------------------------
    # In this part the resample image filter to map a 3D image to 2D image plane with desired specs is designed
    
FilterType = itk.ResampleImageFilter[InputImageType,OutputImageType]                    # Defining the resample image filter type. 
resamplefilter = FilterType.New()               # Pointer to the filter

resamplefilter.SetInput(inputImage)             # Setting the input image data 
resamplefilter.SetDefaultPixelValue( 100 )      # Setting the default Pixel value
resamplefilter.SetInterpolator(interpolator)    # Setting the interpolator
resamplefilter.SetTransform(transform)          # Setting the transform
resamplefilter.SetSize(sizeOutput)              # Setting the size of the output image. 
resamplefilter.SetOutputSpacing(spaceOutput)    # Setting the spacing(resolution) of the output image. 
resamplefilter.SetOutputOrigin(originOutput)    # Setting the output origin of the image
Functions.change_image_direction(oldDirection=resamplefilter.GetOutputDirection(),newDirection=directionOutput,DimensionOut=3)     # Setting the output direction of the image  --- resamplefilter.SetImageDirection(args) was not working properly

resamplefilter.Update()                         # Updating the resample image filter.

if verbose:
    print(resamplefilter)
#%---------------- Rescaler Image Filter --------------------------
RescalerFilterType = itk.RescaleIntensityImageFilter[InputImageType,OutputImageType]    # Defining the rescale image filter. 
rescaler = RescalerFilterType.New()             # Pointer to the rescale filter
rescaler.SetOutputMinimum(0)                    # Minimum output
rescaler.SetOutputMaximum(255)                  # Maximum output 
rescaler.SetInput(resamplefilter.GetOutput())   # Setting the input to the image filter. 

if verbose:
    print(rescaler)
