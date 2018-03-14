
#% ------------------ Interpolator ------------------------------------
InterpolatorType = itk.LinearInterpolateImageFunction[InputImageType,itk.D]
interpolator = InterpolatorType.New()
 #%%----------------- Resample Image Filter -----------------------
 # In this part the resample image filter to map a 3D image to 2D image plane with desired specs is designed
FilterType = itk.ResampleImageFilter[InputImageType,InputImageType]                     # Defining the resample image filter type. 
resamplefilter = FilterType.New()                                                       # Pointer to the filter
#    R = Functions.get_transform_direction(transform)
#    T = numpy.transpose(t)
#    
outOrigin = inOrigin - t #+ R.dot(numpy.transpose(direction_mat.dot(inOrigin)))
#    transform_matrix = Functions.get_vnl_matrix(transform.GetMatrix().GetVnlMatrix())
#outDirection = transform_matrix.dot(direction_mat)
outDirection = inDirection
scaling = 1 # the scaling factor for the image. 

outSize= [scaling*inSize[0],scaling*inSize[1],inSize[2]]

resamplefilter.SetInput(inputImage)                                                     # Setting the input image data 
resamplefilter.SetDefaultPixelValue(default_pixel_value)                                # Setting the default Pixel value
resamplefilter.SetInterpolator(interpolator)                                            # Setting the interpolator
resamplefilter.SetTransform(transform)                                                  # Setting the transform
resamplefilter.SetSize(outSize)                                                         # Setting the size of the output image. 
resamplefilter.SetOutputSpacing(inSpacing)                                              # Setting the spacing(resolution) of the output image. 
# Functions.change_image_direction(resamplefilter.GetOutputDirection(),outDirection,3)
resamplefilter.SetOutputOrigin(outOrigin)                                               # Setting the output origin of the image
resamplefilter.SetOutputDirection(outDirection)                                         # Setting the output direction of the image. 
resamplefilter.Update()                                                                 # Updating the resample image filter.

if verbose:
    print(resamplefilter)


#%% ------------------ Writer ------------------------------------
# The output of the resample filter can then be passed to a writer to
# save the DRR image to a file.
    
WriterType=itk.ImageFileWriter[InputImageType]
writer=WriterType.New()
writer.SetFileName(output_filename)
writer.SetInput(resamplefilter.GetOutput())

try:
    print("Writing the transformed Volume at : " + output_filename)
    writer.Update()
    print("Volume Printed Successfully")
except ValueError: 
    print("ERROR: ExceptionObject caugth! \n")
    print(ValueError)
    sys.exit()