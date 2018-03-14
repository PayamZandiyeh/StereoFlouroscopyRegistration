
# -------------------- Reader -------------------------
InputPixelType  = itk.ctype("short")
DimensionIn  = 3
DimensionOut = 3

InputImageType  = itk.Image[InputPixelType , DimensionIn ]
OutputImageType = itk.Image[InputPixelType , DimensionOut]

ReaderType = itk.ImageFileReader[InputImageType]
reader     = ReaderType.New()
reader.SetFileName(input_filename)

try:
    print("Reading image: " + input_filename)
    reader.Update()
    print("Image Read Successfully")
except ValueError: 
    print("ERROR: ExceptionObject cauth! \n")
    print(ValueError)
    sys.exit()
    
inputImage = reader.GetOutput()

if verbose :
    print(inputImage)
