
#%% Calculating the correlation between images. 
moving_filename = '/Volumes/Storage/Projects/Registration/QuickData/knee_ct_volume_identity.nii'
fixed_filename  = 'knee_test_cam1.mha'
focal_point     = [0.,0., 1650.]

DimensionIn = 3
InputPixelType = itk.ctype("short")

MovingImageType = itk.Image[InputPixelType , DimensionIn] # Moving image type.
FixedImageType  = itk.Image[InputPixelType , DimensionIn] # Fixed image type. 

MetricType = itk.NormalizedCorrelationImageToImageMetric[FixedImageType,MovingImageType] # Metric for calculating the correlation. 
metric = MetricType.New()

metric.SetFixedImage(itk.imread(fixed_filename))
metric.SetMovingImage(itk.imread(fixed_filename))

transform = itk.IdentityTransform[itk.D, 3].New()
metric.SetTransform(transform)

InterpolatorType = itk.RayCastInterpolateImageFunction[InputImageType,itk.D]       # Defining the interpolator type from the template. 
interpolator     = InterpolatorType.New()               # Pointer to the interpolator
interpolator.SetInputImage(itk.imread(moving_filename))                  # Setting the input image data
interpolator.SetThreshold(0)                    # Setting the output threshold
interpolator.SetFocalPoint(itk.Point.D3(focal_point))    # Setting the focal point (x-ray source location)
interpolator.SetTransform(transform)                    # Setting the transform -- 

metric.SetInterpolator(interpolator)

OptimizerType = itk.GradientDescentOptimizer
optimizer = OptimizerType.New()

print(metric.GetValue(transform.GetParameters()))

if verbose:
    print(metric)