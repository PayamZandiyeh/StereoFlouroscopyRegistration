#include "itkImage.h"
#include "itkImageFileReader.h"
#include "itkImageFileWriter.h"
#include "itkResampleImageFilter.h"
#include "itkCenteredEuler3DTransform.h"
#include "itkNearestNeighborInterpolateImageFunction.h"
#include "itkImageRegionIteratorWithIndex.h"
#include "itkRescaleIntensityImageFilter.h"
#include "itkFlipImageFilter.h"
#include "itkMatrix.h"

    // Software Guide : BeginLatex
    //
    // The \code{RayCastInterpolateImageFunction} class definition for
    // this example is contained in the following header file.
    //
    // Software Guide : EndLatex

    // Software Guide : BeginCodeSnippet
#include "itkRayCastInterpolateImageFunction.h"
    // Software Guide : EndCodeSnippet

    //#define WRITE_CUBE_IMAGE_TO_FILE

int main( int argc, char *argv[] )
{

    char *input_name = ITK_NULLPTR;
    input_name = argv[1];

    const     unsigned int   Dimension = 3;

    typedef short InputPixelType;

    typedef short OutputPixelType;

    typedef itk::Image<InputPixelType,Dimension> InputImageType;
    InputImageType::Pointer image = InputImageType::New();

    typedef itk::Image<OutputPixelType,Dimension> OutputImageType;

    typedef itk::ImageFileReader<InputImageType>  ReaderType;
    ReaderType::Pointer reader = ReaderType::New();

    std::cout << input_name << std::endl;
    reader->SetFileName(input_name);


try {
    reader->Update();
} catch (itk::ExceptionObject & err) {
    std::cerr << "ERROR: ExceptionObject caught !" << std::endl;
    std::cerr << err << std::endl;
    return EXIT_FAILURE;
    }
    image = reader->GetOutput();
    
    InputImageType::PointType       imOrigin    = image->GetOrigin();
    InputImageType::SizeType        imSize      = image->GetBufferedRegion().GetSize();
    InputImageType::RegionType      imRegion    = image->GetBufferedRegion();
    InputImageType::DirectionType   imDirection = image->GetDirection();
    InputImageType::SpacingType     imSpacing   = image->GetSpacing();
    
    std::cout << image << std::endl;
    
    return EXIT_SUCCESS;
}
    
    
