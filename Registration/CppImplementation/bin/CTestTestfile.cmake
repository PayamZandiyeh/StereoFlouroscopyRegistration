# CMake generated Testfile for 
# Source directory: /Users/Payam/Desktop/BertelsenRegistration/src
# Build directory: /Users/Payam/Desktop/BertelsenRegistration/bin
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(RunPatchedRayCastInterpolateImageFunctionTest "itkPatchedRayCastInterpolateImageFunctionTest")
add_test(RunGradientDifferenceMultiImageToImageMetricTest "itkGradientDifferenceMultiImageToImageMetricTest")
add_test(RunMeanSquaresMultiImageToImageMetricTest "itkMeanSquaresMultiImageToImageMetricTest")
add_test(RunNormalizedGradientCorrelationMultiImageToImageMetricTest "itkNormalizedGradientCorrelationMultiImageToImageMetricTest")
add_test(RunPatternIntensityMultiImageToImageMetricTest "itkPatternIntensityMultiImageToImageMetricTest")
add_test(RunMultiImageToImageRegistrationMethodTest0 "itkMultiImageToImageRegistrationMethodTest0")
add_test(RunMultiImageToImageRegistrationMethodTest1 "itkMultiImageToImageRegistrationMethodTest1" "/Users/Payam/Desktop/BertelsenRegistration/src/Data")
add_test(RunMultiResolutionMultiImageToImageRegistrationMethodTest0 "itkMultiResolutionMultiImageToImageRegistrationMethodTest0")
add_test(RunMultiResolutionMultiImageToImageRegistrationMethodTest1 "itkMultiResolutionMultiImageToImageRegistrationMethodTest1" "/Users/Payam/Desktop/BertelsenRegistration/src/Data")
add_test(RunMultiResolutionMultiImageToImageRegistrationMethodTest1-mov "ImageCompare" "/Users/Payam/Desktop/BertelsenRegistration/src/Data/moving.level0.mha" "/Users/Payam/Desktop/BertelsenRegistration/src/Data/moving.level0.baseline.mha")
add_test(RunMultiResolutionMultiImageToImageRegistrationMethodTest1-LAT "ImageCompare" "/Users/Payam/Desktop/BertelsenRegistration/src/Data/fixedLAT.level0.mha" "/Users/Payam/Desktop/BertelsenRegistration/src/Data/fixedLAT.level0.baseline.mha")
add_test(RunMultiResolutionMultiImageToImageRegistrationMethodTest1-AP "ImageCompare" "/Users/Payam/Desktop/BertelsenRegistration/src/Data/fixedAP.level0.mha" "/Users/Payam/Desktop/BertelsenRegistration/src/Data/fixedAP.level0.baseline.mha")
add_test(RunMultiResolutionMultiImageToImageRegistrationMethodTest2 "itkMultiResolutionMultiImageToImageRegistrationMethodTest2" "/Users/Payam/Desktop/BertelsenRegistration/src/Data")
