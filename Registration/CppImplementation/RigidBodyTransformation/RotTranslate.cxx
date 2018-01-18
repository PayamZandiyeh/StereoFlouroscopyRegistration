//CopyRight : Payam Zandiyeh -- August 21 2017 --

#include "itkImage.h"
#include "itkImageFileReader.h"
#include "itkImageFileWriter.h"
#include "itkResampleImageFilter.h"
#include "itkCenteredEuler3DTransform.h"
#include "itkMatrix.h"
#include "itkVector.h"
int ScriptMain_RotateZYXAndMoveToOrigin(int argc , char * argv[]){
    if( argc < 12 )
    {
        std::cerr << "Usage: " << std::endl;
        std::cerr << argv[0] << "  inputImageFile  outputImageFile  thetax thetay thetaz  tx ty tz sx sy sz" << std::endl;
        return EXIT_FAILURE;
    }
    //!!!!! ATTENTION : This code is based on directions of x = -1 0 0 ; y = 0 -1 0; z = 0 0 1; Generally used for the CT images.
    // USE WITH CAUTION. IF YOU HAVE ANOTHER CONVENTION MODIFY ACCORDINGLY (Payam Zandiyeh 3:24 PM -- Aug 21-2017).
    
    const unsigned int Dimension = 3; // inputting the dimension of the CT scan.
    typedef short InputPixelType;
    typedef short OutputPixelType;
    
    typedef itk::Image<InputPixelType, Dimension> InputImageType;
    InputImageType::Pointer image = InputImageType::New();
    
    typedef itk::Image<OutputPixelType,Dimension> OutputImageType;
    
    typedef itk::ImageFileReader<InputImageType> ReaderType;
    ReaderType::Pointer reader = ReaderType::New();
    
    typedef itk::ImageFileWriter<OutputImageType> WriterType;
    WriterType::Pointer writer = WriterType::New();
    
    reader->SetFileName(argv[1]);
    writer->SetFileName(argv[2]);
    
    typedef itk::ResampleImageFilter<InputImageType, OutputImageType> FilterType;
    FilterType::Pointer filter = FilterType::New();
    
    typedef itk::LinearInterpolateImageFunction<InputImageType,double> InterpolatorType;
    InterpolatorType::Pointer interpolator = InterpolatorType::New();
    
    typedef itk::CenteredEuler3DTransform<double> TransformType;
    TransformType::Pointer transform = TransformType::New();
    
    const float d2r = std::atan(1)/45.0;
    TransformType::OutputVectorType angleInRad;
    const float rx =  atof(argv[3]); // rotation in x in degrees
    const float ry =  atof(argv[4]); // rotation in y in degrees
    const float rz = -atof(argv[5]); // rotation in z in degrees
    
    angleInRad[0] = rx*d2r;  // rotation in x
    angleInRad[1] = ry*d2r;  // rotation in y
    angleInRad[2] = rz*d2r;  // rotation in z
    
    
    
    reader->Update();
    image = reader->GetOutput();
    
    InputImageType::PointType       imOrigin    = image->GetOrigin();
    InputImageType::SpacingType     imSpacing   = image->GetSpacing();
    InputImageType::SizeType        imSize      = image->GetLargestPossibleRegion().GetSize();
    InputImageType::DirectionType   imDirection = image->GetDirection();
    
    TransformType::OutputVectorType translation; // Recording the translation scalars.
    //    translation[0] = atof(argv[6]);    // translation absolute value in x
    //    translation[1] = atof(argv[7]);    // translation absolute value in y
    //    translation[2] = -atof(argv[8]);    // translation absolute value in z
    
    translation[0] = imOrigin[0];
    translation[1] = imOrigin[1];
    translation[2] = imOrigin[2];
    
    transform->SetTranslation(translation);
    transform->SetRotation(angleInRad[0], angleInRad[1], angleInRad[2]);
    transform->SetComputeZYX(true);
    
    filter->SetInput(reader->GetOutput());
    writer->SetInput(filter->GetOutput());
    transform->SetTranslation(translation);
    
    
    
    InputImageType::IndexType      originIndex = {{
        translation[0]/imSpacing[0]
        ,translation[1]/imSpacing[1]
        ,-translation[2]/imSpacing[2]
    }};
    
    
    InputImageType::IndexType       centerPixelIndex = {{
        imSize[0]/2+originIndex[0]
        ,imSize[1]/2+originIndex[1]
        ,imSize[2]/2+originIndex[2]
    }}; // TODO: What happens when physical size is odd?
    
    TransformType::InputPointType   coRotation; // the centre of rotation.
    OutputImageType::PointType      outOrigin ; // the origin of the image
    OutputImageType::PointType      outGOrigin; // The physical location of the global image.
    
    image->TransformIndexToPhysicalPoint(centerPixelIndex, coRotation);
    image->TransformIndexToPhysicalPoint(originIndex, outOrigin);
    
    
    const int scaling = 1;
    OutputImageType::SizeType outSize = {{
        scaling*imSize[0],scaling*imSize[1],scaling*imSize[2]}};
    
    transform->SetCenter(coRotation);
    OutputImageType::DirectionType outDirection = transform->GetMatrix();
    
    filter->SetDefaultPixelValue(0.0);
    filter->SetInput(image);
    filter->SetSize(outSize);
    filter->SetTransform(transform);
    filter->SetInterpolator(interpolator);
    filter->SetOutputSpacing(imSpacing);
    filter->SetOutputOrigin(outOrigin);
    filter->SetOutputDirection(imDirection);
    
    filter->SetInput(reader->GetOutput());
    
    std::cout << "Transform Details" << std::endl;
    std::cout << transform << std::endl;
    
    writer->SetInput(filter->GetOutput());
    // Write the image transformed without the origin and direction transformed.
    try {
        writer->Update();
    } catch (itk::ExceptionObject & err) {
        std::cerr << "ERROR : ExceptionObject caught !" << std::endl;
        std::cerr << err << std::endl;
        return EXIT_FAILURE;
    }

    return 0;
} // This function rotates the CT image along Z,Y, and then X axes then translates it to the origin of the image.

int main(int argc , char * argv[])
{
    ScriptMain_RotateZYXAndMoveToOrigin(argc,argv); // The image is rotated along ZYX and then translated to the origin.
    
    return EXIT_SUCCESS;
}

