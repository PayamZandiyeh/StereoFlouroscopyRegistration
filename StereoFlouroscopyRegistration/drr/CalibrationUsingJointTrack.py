import numpy
import os
import itk
import sys

class CalibrationTool:
    """Read and store calibration data from camera calibration"""

    def __init__(self):
        
        self.CalibrationFileText = []

        self.principle_dist = 0
        self.x_offset = 0
        self.y_offset = 0
        self.pixel_size = 0

        self.ImageDirectionUp = []
        self.ImageDirectionNormal = []
        self.ImageDirectionHorizontal = []

        self.CameraPath = 0
        self.image_all = []

        self.DirectionMatrix = []
        self.ImageOrigin = []
        
        self.ImageSize = []
        self.ImageFileList = ''
        
        
    
    def SetCalibrationInfo(self, calibrationFileName):
        """SetCalibrationInfo(self,calibrationFileName)
            Loads the calibration text file (according to JointTrack inputs) to the given class. 
            
                INPUTS: 
                    SELF    : The original class
                    FILENAME: The complete name (path+filename) of a text document containing calibration information.
                OUTPUTS: 
                    SELF
            ---------------------
            Parameters Explanation:
            
            
            The first four numbers are the same as 'JT_INTCALIB' files (see 'sample calibration file.txt'):
            
            principal distance;
            x-offset;
            y-offset;
            pixel size/spacing.
            
            
            The next 9 numbers are three vectors:
            
            position of x-ray source;
            image normal;
            image up.
            
            
            ---------------------
            Parameters explained:
            ---------------------
            
            ### External parameters:
            
            # position of x-ray source:
            # image normal            :         The direction of the outward normal of the image, pointing toward the x-ray source. In other words, it is the vector from the Principal Point to the X-ray source point.         
            # image up                :         The direction of the image's 'up' (i.e., the view up direction of the camera/eye).
            
            * ImageNormal and ImageUp do not have to be unit vectors. However, they have to be orthogonal.
            * All three vectors should be described in a world/lab coordinate system however defined by the user.
            * JointTrack currently does not automatically place the models inside the viewing volume (all models are initially placed at (0,0,0)) if external parameters are specified. Therefore, we suggest the world coordinate system such defined that the origin is within the viewing volume. Othrewise, you may need to load a custom kinematics file in order to bring the models into the viewing volume.
            
            ### Internal parameters: (this section is the same as the one in 'sample calibration file.txt').
            
            # principal distance     :          Distance from the x-ray source to the projection/image plane. In actual dimension. Sometimes this is called SID(Source Image Distance).
            # x/y-offset             :          Location of the principal point relative to the center of the image. In actual dimension, not pixels. X points to right and y points up. Principal point is the perpendicular projection of the x-ray source point on the projection/image plane. In other words, the principal point is a point on the image plane, and if you connect the principle point and the x-ray source point with a straight line, the line is perpendicular to the image plane.
            # pixel size/spacing     :          The actual x or y dimension for each pixel on the projection/image plane.


        """
        self.SetCalibrationFileName(calibrationFileName)
        
        open_file = open(self.GetCalibrationFileName(), "r")                                                                    # Reading the file containing the Calibration information. 
        self.CalibrationFileText = open_file.readlines()                                                                        # Text Document loaded from the Calibration file (informative but to be replaced by a private variable rather than public)

        self.SetPrincipalDistance(float(self.CalibrationFileText[1].strip()))                                                   # Source to Image distance (SID) or principal distance. 
        self.SetOffSets(float(self.CalibrationFileText[2].strip()),float(self.CalibrationFileText[3].strip()))                  # Setting the offsets in x and y directions. 
        self.SetPixelSize(float(self.CalibrationFileText[4].strip()),float(self.CalibrationFileText[4].strip()))              # The pixel size in x,y, and z directions. The image is 2D so the third direction is always 1.         
        self.SetFocalPoint([float(x) for x in self.CalibrationFileText[6].strip().split()])                                     # The Focal point of the x-ray (the 3D position of the x-ray in space)       
        self.SetImageDirectionN([float(x) for x in self.CalibrationFileText[7].strip().split()])                                # The normal to the image plane. 
        self.SetImageDirectionU([float(x) for x in self.CalibrationFileText[8].strip().split()])                                # The Upward direction of the 2D image
        self.SetImageDirectionH([float(x) for x in numpy.cross(self.GetImageDirectionU(), self.GetImageDirectionN()).tolist()])                     # The Horizontal direction of the 2D image    UxN = H  
        self.SetDirectionMatrix(numpy.matrix([self.GetImageDirectionH(),self.GetImageDirectionU(),self.GetImageDirectionN()]))
        
    def SetImageHeader(self,inputFileName,outputFileName):
        self.SetImageFileName(inputFileName) # Setting the image file name 
        
        
        inputDimension  = 2                         # The image dimension of the input image. 
        outputDimension = 3                         # The image dimension of the output image. 
    
        pixelType = itk.F
    
        inputImageType  = itk.Image[pixelType, inputDimension ]
    
        
        outputImageType = itk.Image[pixelType, outputDimension]
        
        
        self.JoinSeries(inputImageType,outputImageType,inputFileName)
        self.ChangeInformation(self.GetFilterJoinSeries(),outputImageType)
        self.WriteImageAndHeader(self.GetFilterChangeInformation(),outputImageType,outputFileName)

            
    def SetFilterInfo(self,filterPointer):
        self.FilterInfo = filterPointer
    
    def GetFilterInfo(self):
        return self.FilterInfo
    
    def SetImage(self,inputImage):
        self.Image = inputImage
    
    def GetImage(self):
        return self.Image
        
    def SetGlobalOriginForImagePlane(self):
        '''Calculates the origin of the image plane in the global coordinate system. The origin was defined on bottom left corner '''
        imSize = self.GetOutputImageSize()
        w =  imSize[0]
        h =  imSize[1]
    
        deltaX, deltaY = self.GetOffSets()
        deltaV = (float(w) / 2.0) * self.PixelSize[0]
        deltaU = (float(h) / 2.0) * self.PixelSize[0]
        pdist = self.GetPrincipalDistance()
    
        P = numpy.matrix([deltaX, deltaY, 0])
        Q = numpy.matrix([deltaV, deltaU, 0])
    
        M = numpy.matrix(self.GetDirectionMatrix())
        
        R = M*numpy.transpose(P+Q)                                          # a vector from bottom left corner of image to the principal point.
        N = numpy.transpose(pdist*numpy.matrix(self.GetImageDirectionN()))  # a vector from the x-ray source to the principal point
        F = numpy.transpose(numpy.matrix(self.GetFocalPoint()))             # a vector from global coordinate system to the x-ray source. 
    
        origin = numpy.transpose(F - N - R)                                 # A vector from the global coordinate system to the bottom left origin of the image. 
        
        Origin = itk.Point.D3([origin[0,0],origin[0,1],origin[0,2]])
        
        self.SetImageOrigin(Origin)
    
    def GetGlobalOriginForImagePlane(self):
        '''Redundant but necessary for cleanliness and logical flow of the code. '''
        return self.ImageOrigin
    
    def SetImageOrigin(self, origin):
        self.ImageOrigin = origin
        
    def GetImageOrigin(self):
        return self.ImageOrigin
    
    def SetCalibrationFileName(self,calibrationFileName):
        '''Setting the Calibration Filename '''
        self.CalibrationFileName = calibrationFileName
    
    def GetCalibrationFileName(self):
        '''Retreiving the Calibration Filename'''
        return self.CalibrationFileName
    
    def SetPrincipalDistance(self, principal_distance):
        '''Setting the source to image distance from x-ray to image plane. Also known as principal distance'''
        self.PrincipalDistance = float(principal_distance)
    
    def GetPrincipalDistance(self):
        '''Getting the source to image distance from x-ray to image plane. Also known as principal distance'''
        return(self.PrincipalDistance)
    
    def SetOffSets(self,offset_x,offset_y):
        '''Setting the offsets in x and y direction in the image plane '''
        self.Offset_x = offset_x
        self.Offset_y = offset_y
    
    def GetOffSets(self):
        '''Returing the offset values in x and y directions respectively'''
        return (self.Offset_x , self.Offset_y)
    
    def SetPixelSize(self,res_x,res_y):
        self.PixelSize = [float(res_x),float(res_y)]
        
    def GetPixelSize(self):
        return(self.PixelSize)
    
    def SetFocalPoint(self,fPoints):
        self.FocalPoint = fPoints 
        
    def GetFocalPoint(self):
        return(self.FocalPoint)
    
    def SetImageDirectionH(self,imageDirectionH):
        '''Setting the Horizontal image direction'''
        self.ImageDirectionHorizontal = imageDirectionH
    
    def GetImageDirectionH(self):
        return(self.ImageDirectionHorizontal)
        
    def SetImageDirectionU(self,imageDirectionUp):
        self.ImageDirectionUp = imageDirectionUp
        
    def GetImageDirectionU(self):
        return(self.ImageDirectionUp)
    
    def SetImageDirectionN(self,imageDirectionNormal):
        self.ImageDirectionNormal = imageDirectionNormal
    
    def GetImageDirectionN(self):
        return(self.ImageDirectionNormal)
        
    def SetImageDirectionMatrix(self,inputImage):
        DirectionVnl = inputImage.DirectionMatrix.GetVnlMatrix()
        DirectionVnl.set_identity()
        
        directionMatrix = self.GetDirectionMatrix()
        
        DirectionVnl.put(0,0,directionMatrix.item((0,0)))
        DirectionVnl.put(0,1,directionMatrix.item((0,1)))
        DirectionVnl.put(0,2,directionMatrix.item((0,2)))
    
        DirectionVnl.put(1,0,directionMatrix.item((1,0)))
        DirectionVnl.put(1,1,directionMatrix.item((1,1)))
        DirectionVnl.put(1,2,directionMatrix.item((1,2)))
    
        DirectionVnl.put(2,0,directionMatrix.item((2,0)))
        DirectionVnl.put(2,1,directionMatrix.item((2,1)))
        DirectionVnl.put(2,2,directionMatrix.item((2,2)))
        
        inputImage.Update()
        
        
    def SetDirectionMatrix(self,DirectionMatrix):
        self.DirectionMatrix = DirectionMatrix
        
    def GetDirectionMatrix(self):
        return self.DirectionMatrix
    
    def SetImageFileName(self,imageFileName):
        '''Setting the filename of the image'''
        self.ImageFileName = imageFileName     # Setting the image file name in the class. 
    
    def GetImageFileName(self):
        '''Retreiving the filename of the image'''
        return self.ImageFileName              # Returing the image file name in the class. 
    
    def SetOutputImageSize(self,w,h,z):
        self.OutputImageSize = [w,h,z]
        
    def GetOutputImageSize(self):
        '''Getting the image size'''
        return self.OutputImageSize
    
    def JoinSeries(self,inputImageType,outputImageType,inputFileName):
        
        FilterType = itk.JoinSeriesImageFilter[inputImageType,outputImageType]
        filterJS   = FilterType.New()
        
        ReaderType      = itk.ImageFileReader[inputImageType]
        reader          = ReaderType.New()
            
        reader.SetFileName(inputFileName)
    
        try:
            reader.Update()
            inputImage = reader.GetOutput()
            
            
        except ValueError: 
            print("ERROR: ExceptionObject cauth! \n")
            print(ValueError)
            sys.exit()
        
        region = inputImage.GetLargestPossibleRegion()
        w, h   = region.GetSize()
        z = 1
        
        self.SetOutputImageSize(w,h,z)            # Setting the size of image in the output
        self.SetGlobalOriginForImagePlane()       # Setting the global origin of the image. 
            
        inputImage.SetSpacing(self.GetPixelSize()) # Setting the spacing of the input image according to the calibration information. 
        
        filterJS.SetInput(0, inputImage)   # Adding an image to the join series filter. 
    
    
        filterJS.SetSpacing(1.) # Setting the spacing in the new dimension. 
        filterJS.Update()
        
        self.SetFilterJoinSeries(filterJS)
    
    def SetFilterJoinSeries(self,filterJS):
        self.FilterJoinSeries = filterJS
        
    def GetFilterJoinSeries(self):
        return self.FilterJoinSeries
    
    def ChangeInformation(self,filterJS,outputImageType):
        FilterType = itk.ChangeInformationImageFilter[outputImageType]       # Change Image Information
        filterCI = FilterType.New()                                          # Creating a new pointer for the filter. 
        
        imageJoinSeries = filterJS.GetOutput()
        
        filterCI.SetInput(imageJoinSeries)                                   # Setting the input to 
        filterCI.SetOutputSpacing(imageJoinSeries.GetSpacing())              # Setting the spacing of the output image. 
        filterCI.ChangeSpacingOn()                                           # Enabling the change in the output spacing from the default values. 
        
        filterCI.SetOutputOrigin(self.GetGlobalOriginForImagePlane())        # Setting the origin of the image to the global coordinate. 
        filterCI.ChangeOriginOn()                                            # Enabling the change in the output origin from the default values. 
        
        
        # Setting the direction of the image in the filter        
        
        vnlMatrix = filterCI.GetOutputDirection().GetVnlMatrix()
        newDirection = self.GetDirectionMatrix()
        for i in range(3):
            for j in range(3):
                vnlMatrix.put(i,j,newDirection[i,j])
        
        filterCI.SetOutputDirection(filterCI.GetOutputDirection())           # This line is not even necessary -- It is for cleanliness - previous lines have done the change of direction. 
        filterCI.ChangeDirectionOn()                                         # Enabling the change in the output direction from the default values. 
        
        filterCI.Update()   
        self.SetFilterChangeInformation(filterCI)
        
    def SetFilterChangeInformation(self,filterCI):
        self.FilterChangeDirection = filterCI
    def GetFilterChangeInformation(self):
        return self.FilterChangeDirection
        
    def WriteImageAndHeader(self,filterCI,outputImageType,outputFileName):
        WriterType      = itk.ImageFileWriter[outputImageType]
        writer          = WriterType.New()
        # Writing the output image to the destination
        writer.SetFileName(outputFileName)                                   # Write the output filename
        writer.SetInput(filterCI.GetOutput())                                # Setting the input of the writer. 
        
        try:
            print("Writing image: ")
            writer.Update()
            print("Image Printed Successfully")
        except ValueError: 
            print("ERROR: ExceptionObject cauth! \n")
            print(ValueError)
            sys.exit()
    
#%%
class StackingTool(CalibrationTool): # Stacking tool inherits all from Calibration Tools
    
    def __init__(self,calibrationFileName,inputDirectory,outputFileName):
        self.SetCalibrationInfo(calibrationFileName) # initialize to load all calibration info here. 
        self.SetInputDirectory(inputDirectory)       # Setting the input directory
        self.SetImageHeader(inputDirectory,outputFileName) # Printing the calibration information 
        
    def SetInputDirectory(self,inputDirectory):
        '''Setting the input Directory from which the stack of images will be read '''
        if (os.path.isdir(inputDirectory)!= True):                           # Checking to see if the provided folder is a directory or not. 
            raise ValueError(inputDirectory+" is not a directory")
            return -1
        self.InputDirectory = inputDirectory
        self.SetImageFileList()                      # Setting the list of images to be stacked. 
        
    def GetInputDirectory(self):
        '''Returning the input directory from which the stack of images will be read'''
        return self.InputDirectory
    
    def SetImageFileList(self):
        self.ImageFileList = os.listdir(self.GetInputDirectory())
    
    def GetImageFileList(self):
        return self.ImageFileList
        
    def SetImageHeader(self,inputDirectory,outputFileName):
        #%%
        # Determining the reader and writer
        
        inputDimension  = 2                         # The image dimension of the input image. 
        outputDimension = 3                         # The image dimension of the output image. 
    
        pixelType = itk.F
    
        inputImageType  = itk.Image[pixelType, inputDimension ]
        outputImageType = itk.Image[pixelType, outputDimension]
        
        self.JoinSeries(inputImageType,outputImageType,inputDirectory)
        self.ChangeInformation(self.GetFilterJoinSeries(),outputImageType)
        self.WriteImageAndHeader(self.GetFilterChangeInformation(),outputImageType,outputFileName)
        
    #%%
    def JoinSeries(self,inputImageType,outputImageType,inputDirectory):
    
        FilterType = itk.JoinSeriesImageFilter[inputImageType,outputImageType]
        filterJS   = FilterType.New()
        
        ReaderType      = itk.ImageFileReader[inputImageType]
        reader          = ReaderType.New()
        
        
        #%%
        for ii in range(len(self.ImageFileList)):
            
            reader.SetFileName(os.path.join(inputDirectory,self.GetImageFileList()[ii]))
        
            try:
                reader.Update()
                inputImage = reader.GetOutput()
                
                
            except ValueError: 
                print("ERROR: ExceptionObject cauth! \n")
                print(ValueError)
                sys.exit()
            if ii == 0:
                region = inputImage.GetLargestPossibleRegion()
                w, h   = region.GetSize()
                z = len(self.ImageFileList)               # Number of slides in the z direction is equal to the number of images that we like to stack.
                
                self.SetOutputImageSize(w,h,z)            # Setting the size of image in the output
                self.SetGlobalOriginForImagePlane()       # Setting the global origin of the image. 
            
            inputImage.SetSpacing(self.GetPixelSize()) # Setting the spacing of the input image according to the calibration information. 
            
            filterJS.SetInput(ii, inputImage)   # Adding an image to the join series filter. 
            
            # The progress bar activation
            self.update_progress(float(ii)/z)
            
        #%%
        filterJS.SetSpacing(1.) # Setting the spacing in the new dimension. 
        filterJS.Update()
        
        self.SetFilterJoinSeries(filterJS)
        
   
    def update_progress(self,progress):
        barLength = 10 # Modify this to change the length of the progress bar
        status = ""
        if isinstance(progress, int):
            progress = float(progress)
        if not isinstance(progress, float):
            progress = 0
            status = "error: progress var must be float\r\n"
        if progress < 0:
            progress = 0
            status = "Halt...\r\n"
        if progress >= 1:
            progress = 1
            status = "Done...\r\n"
        block = int(round(barLength*progress))
        text = "\rReading and joining Images in the folder: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
        sys.stdout.write(text)
        sys.stdout.flush()
        
