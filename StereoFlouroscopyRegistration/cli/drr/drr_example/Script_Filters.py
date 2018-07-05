#%----------------- Resample Image Filter ------------------------
    # In this part the resample image filter to map a 3D image to 2D image plane with desired specs is designed
    
FilterType = itk.ResampleImageFilter[InputImageType,OutputImageType]                    # Defining the resample image filter type. 
resamplefilter = FilterType.New()               # Pointer to the filter

resamplefilter.SetInput(inputImage)             # Setting the input image data 
resamplefilter.SetDefaultPixelValue( 10 )      # Setting the default Pixel value
resamplefilter.SetInterpolator(interpolator)    # Setting the interpolator
resamplefilter.SetTransform(transform)          # Setting the transform
resamplefilter.SetSize(sizeOutput)              # Setting the size of the output image. 
resamplefilter.SetOutputSpacing(spaceOutput)    # Setting the spacing(resolution) of the output image. 
resamplefilter.SetOutputOrigin(originOutput)    # Setting the output origin of the image
Functions.change_image_direction(oldDirection=resamplefilter.GetOutputDirection(),newDirection=directionOutput,DimensionOut=3)     # Setting the output direction of the image  --- resamplefilter.SetImageDirection(args) was not working properly
resamplefilter.Update()                         # Updating the resample image filter.

filteringOutput = resamplefilter.GetOutput()

if verbose:
    print(resamplefilter)
#%%---------------- Rescaler Image Filter --------------------------
RescalerFilterType = itk.RescaleIntensityImageFilter[InputImageType,OutputImageType]    # Defining the rescale image filter. 
rescaler = RescalerFilterType.New()             # Pointer to the rescale filter
rescaler.SetOutputMinimum(0)                    # Minimum output
rescaler.SetOutputMaximum(255)                  # Maximum output 
rescaler.SetInput(resamplefilter.GetOutput())   # Setting the input to the image filter. 

filteringOutput = rescaler.GetOutput()

if verbose:
    print(rescaler)

#%%---------------- Flip Axis filter ------------------------------

FlipFilterType = itk.FlipImageFilter[OutputImageType] 
flipfilter = FlipFilterType.New()

flipfilter.SetFlipAxes([0,0,0]) # Flip the axes along x and y but leave z intact.  
flipfilter.SetInput(filteringOutput) # Setting the input to the flip filter.

filteringOutput = flipfilter.GetOutput()

if verbose:
    print(flipfilter)

#%% 
last_filter_output = filteringOutput