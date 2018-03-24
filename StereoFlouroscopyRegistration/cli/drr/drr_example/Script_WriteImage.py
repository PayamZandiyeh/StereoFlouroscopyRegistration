#% ------------------ Writer ------------------------------------
    # The output of the resample filter can then be passed to a writer to
    # save the DRR image to a file.
WriterType = itk.ImageFileWriter[OutputImageType]
writer = WriterType.New()

writer.SetFileName(output_filename[ii])
writer.SetInput(last_filter_output) # set the input as the output of filtering process. 

try:
    print("Writing image: " + output_filename[ii])
    writer.Update()
    print("Image Printed Successfully")
except ValueError: 
    print("ERROR: ExceptionObject cauth! \n")
    print(ValueError)
    sys.exit()

if verbose: 
    print('Details of image: ')
    print(last_filter_output)