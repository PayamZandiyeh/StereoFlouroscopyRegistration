# This is the root ITK CMakeLists file.
cmake_minimum_required(VERSION 2.8.9)
if(COMMAND CMAKE_POLICY)
  cmake_policy(SET CMP0003 NEW)
endif()


# This project is designed to be built outside the Insight source tree.
project(RegistrationPayamZandiyeh)

# Find ITK.
find_package(ITK REQUIRED)
include(${ITK_USE_FILE})

add_executable(ImageTransformation RotTranslate.cxx)
target_link_libraries(ImageTransformation ${ITK_LIBRARIES})

add_executable(DigitallyReconstructedRadiograph DRR.cxx)
target_link_libraries(DigitallyReconstructedRadiograph ${ITK_LIBRARIES})

add_executable(ImageConversion ImageConvert.cxx)
target_link_libraries(ImageConversion ${ITK_LIBRARIES})