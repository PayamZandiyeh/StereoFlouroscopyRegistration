include(${CMAKE_SOURCE_DIR}/IJMacros.txt)

cmake_minimum_required(VERSION 2.8.9)

if(COMMAND CMAKE_POLICY)
  cmake_policy(SET CMP0003 NEW)
endif()

project(itkMultiImageRegistration)

find_package(ITK REQUIRED)
include(${ITK_USE_FILE})


#The following lines are required to use Dart
enable_testing()
include(Dart)

set(Required_Packages ITK)

include_directories(${CMAKE_CURRENT_SOURCE_DIR})

#Add project's executables
add_executable(ImageCompare ImageCompare.cxx) 
target_link_libraries(ImageCompare ${ITK_LIBRARIES})

add_executable(MultiImageSearch Examples/MultiImageSearch.cxx)
target_link_libraries(MultiImageSearch ${ITK_LIBRARIES})

add_executable(MultiImageRegistration Examples/MultiImageRegistration.cxx)
target_link_libraries(MultiImageRegistration ${ITK_LIBRARIES})


#Add tests
set(DataDirectory ${CMAKE_CURRENT_SOURCE_DIR}/Data)

# Test for the PatchedRayCastInterpolateImageFunction class

add_executable(itkPatchedRayCastInterpolateImageFunctionTest Testing/itkPatchedRayCastInterpolateImageFunctionTest.cxx)
target_link_libraries(itkPatchedRayCastInterpolateImageFunctionTest ${ITK_LIBRARIES})
add_test(RunPatchedRayCastInterpolateImageFunctionTest itkPatchedRayCastInterpolateImageFunctionTest)

# Tests for the MultiImageToImageMetric subclasses

add_executable(itkGradientDifferenceMultiImageToImageMetricTest Testing/itkGradientDifferenceMultiImageToImageMetricTest.cxx)
target_link_libraries(itkGradientDifferenceMultiImageToImageMetricTest ${ITK_LIBRARIES})
add_test(RunGradientDifferenceMultiImageToImageMetricTest itkGradientDifferenceMultiImageToImageMetricTest)

add_executable(itkMeanSquaresMultiImageToImageMetricTest Testing/itkMeanSquaresMultiImageToImageMetricTest.cxx)
target_link_libraries(itkMeanSquaresMultiImageToImageMetricTest ${ITK_LIBRARIES})
add_test(RunMeanSquaresMultiImageToImageMetricTest itkMeanSquaresMultiImageToImageMetricTest)

add_executable(itkNormalizedGradientCorrelationMultiImageToImageMetricTest Testing/itkNormalizedGradientCorrelationMultiImageToImageMetricTest.cxx)
target_link_libraries(itkNormalizedGradientCorrelationMultiImageToImageMetricTest ${ITK_LIBRARIES})
add_test(RunNormalizedGradientCorrelationMultiImageToImageMetricTest itkNormalizedGradientCorrelationMultiImageToImageMetricTest)

add_executable(itkPatternIntensityMultiImageToImageMetricTest Testing/itkPatternIntensityMultiImageToImageMetricTest.cxx)
target_link_libraries(itkPatternIntensityMultiImageToImageMetricTest ${ITK_LIBRARIES})
add_test(RunPatternIntensityMultiImageToImageMetricTest itkPatternIntensityMultiImageToImageMetricTest)


# Tests for the MultiImageToImageRegistrationMethod class

add_executable(itkMultiImageToImageRegistrationMethodTest0 Testing/itkMultiImageToImageRegistrationMethodTest0.cxx)
target_link_libraries(itkMultiImageToImageRegistrationMethodTest0 ${ITK_LIBRARIES})
add_test(RunMultiImageToImageRegistrationMethodTest0 itkMultiImageToImageRegistrationMethodTest0)

add_executable(itkMultiImageToImageRegistrationMethodTest1 Testing/itkMultiImageToImageRegistrationMethodTest1.cxx)
target_link_libraries(itkMultiImageToImageRegistrationMethodTest1 ${ITK_LIBRARIES})
add_test(RunMultiImageToImageRegistrationMethodTest1 itkMultiImageToImageRegistrationMethodTest1 ${DataDirectory})


# Tests for the MultiResolutionMultiImageToImageRegistrationMethod class

add_executable(itkMultiResolutionMultiImageToImageRegistrationMethodTest0 Testing/itkMultiResolutionMultiImageToImageRegistrationMethodTest0.cxx)
target_link_libraries(itkMultiResolutionMultiImageToImageRegistrationMethodTest0 ${ITK_LIBRARIES})
add_test(RunMultiResolutionMultiImageToImageRegistrationMethodTest0 itkMultiResolutionMultiImageToImageRegistrationMethodTest0)

add_executable(itkMultiResolutionMultiImageToImageRegistrationMethodTest1 Testing/itkMultiResolutionMultiImageToImageRegistrationMethodTest1.cxx)
target_link_libraries(itkMultiResolutionMultiImageToImageRegistrationMethodTest1 ${ITK_LIBRARIES})
add_test(RunMultiResolutionMultiImageToImageRegistrationMethodTest1 itkMultiResolutionMultiImageToImageRegistrationMethodTest1 ${DataDirectory})
add_test(RunMultiResolutionMultiImageToImageRegistrationMethodTest1-mov ImageCompare ${DataDirectory}/moving.level0.mha   ${DataDirectory}/moving.level0.baseline.mha)
add_test(RunMultiResolutionMultiImageToImageRegistrationMethodTest1-LAT ImageCompare ${DataDirectory}/fixedLAT.level0.mha ${DataDirectory}/fixedLAT.level0.baseline.mha)
add_test(RunMultiResolutionMultiImageToImageRegistrationMethodTest1-AP  ImageCompare ${DataDirectory}/fixedAP.level0.mha  ${DataDirectory}/fixedAP.level0.baseline.mha)

add_executable(itkMultiResolutionMultiImageToImageRegistrationMethodTest2 Testing/itkMultiResolutionMultiImageToImageRegistrationMethodTest2.cxx)
target_link_libraries(itkMultiResolutionMultiImageToImageRegistrationMethodTest2 ${ITK_LIBRARIES})
add_test(RunMultiResolutionMultiImageToImageRegistrationMethodTest2 itkMultiResolutionMultiImageToImageRegistrationMethodTest2 ${DataDirectory})




