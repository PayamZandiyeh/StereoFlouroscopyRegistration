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


void usage()
{
    std::cerr << "\n";
    std::cerr << "Usage: DRR <options> [input]\n";
    std::cerr << "  calculates the Digitally Reconstructed Radiograph from a volume. \n\n";
    std::cerr << " where <options> is one or more of the following:\n\n";
    std::cerr << "  <-h>                    Display (this) usage information\n";
    std::cerr << "  <-v>                    Verbose output [default: no]\n";
    std::cerr << "  <-res float float>      Pixel spacing of the output image [default: 1x1mm]  \n";
    std::cerr << "  <-size int int>         Dimension of the output image [default: 501x501]  \n";
    std::cerr << "  <-sid float>            Distance of ray source (focal point) [default: 400mm]\n";
    std::cerr << "  <-t float float float>  Translation parameter of the camera \n";
    std::cerr << "  <-rx float>             Rotation around x,y,z axis in degrees \n";
    std::cerr << "  <-ry float>\n";
    std::cerr << "  <-rz float>\n";
    std::cerr << "  <-normal float float>   The 2D projection normal position [default: 0x0mm]\n";
    std::cerr << "  <-cor float float float> The centre of rotation relative to centre of volume\n";
    std::cerr << "  <-threshold float>      Threshold [default: 0]\n";
    std::cerr << "  <-o file>               Output image filename\n\n";
    std::cerr << "                          by  thomas@hartkens.de\n";
    std::cerr << "                          and john.hipwell@kcl.ac.uk (CISG London)\n\n";
    exit(1);
}

int main( int argc, char *argv[] )
{
    char *input_name = ITK_NULLPTR;
    char *output_name = ITK_NULLPTR;
    std::cout << argv[0] << std::endl;
    bool ok;
    bool verbose = false;
    
    float rx = 0.;
    float ry = 0.;
    float rz = 0.;
    
    float tx = 0.;
    float ty = 0.;
    float tz = 0.;
    
    float cx = 0.;
    float cy = 0.;
    float cz = 0.;
    
    float sid = 400.;
    
    float sx = 1.;
    float sy = 1.;
    
    int dx = 501;
    int dy = 501;
    
    float o2Dx = 0;
    float o2Dy = 0;
    
    double threshold=0;
    
    
    
    // Parse command line parameters
    
    while (argc > 1)
    {
        ok = false;
        
        if ((ok == false) && (strcmp(argv[1], "-h") == 0))
        {
            argc--; argv++;
            ok = true;
            usage();
        }
        
        if ((ok == false) && (strcmp(argv[1], "-v") == 0))
        {
            argc--; argv++;
            ok = true;
            verbose = true;
        }
        
        if ((ok == false) && (strcmp(argv[1], "-rx") == 0))
        {
            argc--; argv++;
            ok = true;
            rx=atof(argv[1]);
            argc--; argv++;
        }
        
        if ((ok == false) && (strcmp(argv[1], "-ry") == 0))
        {
            argc--; argv++;
            ok = true;
            ry=atof(argv[1]);
            argc--; argv++;
        }
        
        if ((ok == false) && (strcmp(argv[1], "-rz") == 0))
        {
            argc--; argv++;
            ok = true;
            rz=atof(argv[1]);
            argc--; argv++;
        }
        
        if ((ok == false) && (strcmp(argv[1], "-threshold") == 0))
        {
            argc--; argv++;
            ok = true;
            threshold=atof(argv[1]);
            argc--; argv++;
        }
        
        if ((ok == false) && (strcmp(argv[1], "-t") == 0))
        {
            argc--; argv++;
            ok = true;
            tx=atof(argv[1]);
            argc--; argv++;
            ty=atof(argv[1]);
            argc--; argv++;
            tz=atof(argv[1]);
            argc--; argv++;
        }
        
        if ((ok == false) && (strcmp(argv[1], "-cor") == 0))
        {
            argc--; argv++;
            ok = true;
            cx=atof(argv[1]);
            argc--; argv++;
            cy=atof(argv[1]);
            argc--; argv++;
            cz=atof(argv[1]);
            argc--; argv++;
        }
        
        if ((ok == false) && (strcmp(argv[1], "-res") == 0))
        {
            argc--; argv++;
            ok = true;
            sx=atof(argv[1]);
            argc--; argv++;
            sy=atof(argv[1]);
            argc--; argv++;
        }
        
        if ((ok == false) && (strcmp(argv[1], "-size") == 0))
        {
            argc--; argv++;
            ok = true;
            dx=atoi(argv[1]);
            argc--; argv++;
            dy=atoi(argv[1]);
            argc--; argv++;
        }
        
        if ((ok == false) && (strcmp(argv[1], "-sid") == 0))
        {
            argc--; argv++;
            ok = true;
            sid=atof(argv[1]);
            argc--; argv++;
        }
        
        if ((ok == false) && (strcmp(argv[1], "-normal") == 0))
        {
            argc--; argv++;
            ok = true;
            o2Dx=atof(argv[1]);
            argc--; argv++;
            o2Dy=atof(argv[1]);
            argc--; argv++;
        }
        
        if ((ok == false) && (strcmp(argv[1], "-o") == 0))
        {
            argc--; argv++;
            ok = true;
            output_name = argv[1];
            argc--; argv++;
        }
        
        if (ok == false)
        {
            
            if (input_name == ITK_NULLPTR)
            {
                input_name = argv[1];
                argc--;
                argv++;
            }
            
            else
            {
                std::cerr << "ERROR: Can not parse argument " << argv[1] << std::endl;
                usage();
            }
        }
    }
    
    const     unsigned int   Dimension = 3;
    typedef short InputPixelType;
    typedef short OutputPixelType;
    
    typedef itk::Image<InputPixelType,Dimension> InputImageType;
    InputImageType::Pointer image = InputImageType::New();
    
    typedef itk::Image<OutputPixelType,Dimension> OutputImageType;
    
    typedef itk::ImageFileReader<InputImageType>  ReaderType;
    ReaderType::Pointer reader = ReaderType::New();
    
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
    
    typedef itk::CenteredEuler3DTransform<double> TransformType;
    TransformType::Pointer transform = TransformType::New();
    
    transform->SetComputeZYX(true);
    TransformType::OutputVectorType translation;
    translation[0] = tx;
    translation[1] = ty;
    translation[2] = tz;
        // constant for converting degrees into radians
    const double dtr = ( std::atan(1.0) * 4.0 ) / 180.0;
    transform->SetTranslation( translation );
    transform->SetRotation( dtr*rx, dtr*ry, dtr*rz );
    
    
    typedef itk::RayCastInterpolateImageFunction<InputImageType,double> InterpolatorType;
    InterpolatorType::Pointer interpolator = InterpolatorType::New();
    
    InterpolatorType::InputPointType focalpoint;
    InputImageType::IndexType desPixelIndx;
    desPixelIndx[0] = (imSize[0]-1.)/2.0; // Find the centre of the volume
    desPixelIndx[1] = (imSize[1]-1.)/2.0; // Find the centre of the volume
    desPixelIndx[2] = (imSize[2]-1.)/2.0; // Find the centre of the volume
    
    image->TransformIndexToPhysicalPoint(desPixelIndx,focalpoint);
    focalpoint[0] = o2Dx;// Location of the principle point in x direction relative to the center of image.
    focalpoint[1] = o2Dy;// Location of the principle point in y direction relative to the center of image.
    focalpoint[2] = sid; // The principal distance or source to image distance.
    
    interpolator->SetTransform(transform);
    interpolator->SetThreshold(threshold);
    interpolator->SetFocalPoint(focalpoint);
    interpolator->Print(std::cout);
    
    
    InputImageType::SizeType size = {{512,512,1}};
    
    typedef itk::ResampleImageFilter<InputImageType, OutputImageType> FilterType;
    FilterType::Pointer filter = FilterType::New();
    
        //----------------------------------------------------------------------------
        // Image Plane Definition : Origin
        //----------------------------------------------------------------------------
    float iOx = 0.0; // The image plane origin in x.
    float iOy = 0.0; // The image plane origin in y.
    float iOz = 0.0; // The image plane origin in z.
    
    desPixelIndx[0] = (size[0]-1.)/2.0;
    desPixelIndx[1] = (size[1]-1.)/2.0;
    desPixelIndx[2] = (size[2]-1.)/1.0;
    
    InputImageType::PointType           outOrigin;
    
    image->TransformIndexToPhysicalPoint(desPixelIndx, outOrigin);
    
    outOrigin[2] = iOz;
//    outOrigin[0] = iOx;
//    outOrigin[1] = iOy;
//    outOrigin[2] = iOz;
//    
    
    
    outOrigin = imDirection*outOrigin; // Projecting it in the desired direction based on the image direction.
    
    InputImageType::SpacingType         outSpacing;
    outSpacing[0] = imSpacing[0];
    outSpacing[1] = imSpacing[1];
    outSpacing[2] = 1.0;
    
    InputImageType::DirectionType      outDirection;
    outDirection = imDirection;
    
    
    filter->SetSize(size);
    filter->SetInterpolator(interpolator);
    filter->SetDefaultPixelValue(0.0);
    filter->SetOutputSpacing(outSpacing);
    filter->SetOutputOrigin(outOrigin);
    filter->SetOutputDirection(imDirection);
    filter->SetTransform(transform);
    filter->SetInput(image);
    
    typedef itk::RescaleIntensityImageFilter<InputImageType,OutputImageType> RescaleFilterType;
    RescaleFilterType::Pointer rescaler = RescaleFilterType::New();
    
    rescaler->SetOutputMinimum(0);
    rescaler->SetOutputMaximum(255);
    rescaler->SetInput(filter->GetOutput());
    
    
    typedef itk::FlipImageFilter< OutputImageType > FlipFilterType;
    FlipFilterType::Pointer flipFilter = FlipFilterType::New();
    
    typedef FlipFilterType::FlipAxesArrayType FlipAxesArrayType;
    FlipAxesArrayType flipArray;
    flipArray[0] = 1; // since X direction was -1 0 0
    flipArray[1] = 1; // since Y direction was 0 -1 0
    
    flipFilter->SetFlipAxes( flipArray );
    flipFilter->SetInput( rescaler->GetOutput() );
    flipFilter->Update();
    
    
    
    typedef itk::ImageFileWriter<OutputImageType> WriterType;
    WriterType::Pointer writer = WriterType::New();
    
    writer->SetFileName(output_name);
    writer->SetInput(flipFilter->GetOutput());
    
    try
    {
    std::cout << "Writing image: " << output_name << std::endl;
    writer->Update();
    }
    catch( itk::ExceptionObject & err )
    {
    std::cerr << "ERROR: ExceptionObject caught !" << std::endl;
    std::cerr << err << std::endl;
    }
    
    
        return EXIT_SUCCESS;
}
