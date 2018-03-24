ScalarType = itk.D
InterpolatorType = itk.RayCastInterpolateImageFunction[InputImageType,ScalarType]       # Defining the interpolator type from the template. 
interpolator     = InterpolatorType.New()               # Pointer to the interpolator

interpolator.SetInputImage(inputImage)                  # Setting the input image data
interpolator.SetThreshold(threshold)                    # Setting the output threshold
interpolator.SetFocalPoint(itk.Point.D3(focalPoint))    # Setting the focal point (x-ray source location)
interpolator.SetTransform(transform)                    # Setting the transform -- 

if verbose:
    print(interpolator)