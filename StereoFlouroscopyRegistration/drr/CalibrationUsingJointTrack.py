import numpy
import os
import itk

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

        self.camera_path = 0
        self.image_all = []

        self.DirectionMatrix = itk.Matrix[itk.D, 3, 3]()
        self.image_origin = []
        
        self.image_size = []

    def SetCalibration(self, filename):
        """SetCalibration(self,filename)
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
        self.SetCalibrationFileName(filename)
        
        open_file = open(self.GetCalibrationFileName(), "r")                                                                    # Reading the file containing the Calibration information. 
        self.CalibrationFileText = open_file.readlines()                                                                        # Text Document loaded from the Calibration file (informative but to be replaced by a private variable rather than public)

        self.SetPrincipalDistance(float(self.CalibrationFileText[1].strip()))                                                   # Source to Image distance (SID) or principal distance. 
        self.SetOffSets(float(self.CalibrationFileText[2].strip()),float(self.CalibrationFileText[3].strip()))                  # Setting the offsets in x and y directions. 
        self.SetPixelSize(float(self.CalibrationFileText[4].strip()),float(self.CalibrationFileText[4].strip()))              # The pixel size in x,y, and z directions. The image is 2D so the third direction is always 1.         
        self.SetFocalPoint([float(x) for x in self.CalibrationFileText[6].strip().split()])                                     # The Focal point of the x-ray (the 3D position of the x-ray in space)       
        self.SetImageDirectionN([float(x) for x in self.CalibrationFileText[7].strip().split()])                                # The normal to the image plane. 
        self.SetImageDirectionU([float(x) for x in self.CalibrationFileText[8].strip().split()])                                # The Upward direction of the 2D image
        self.SetImageDirectionH([float(x) for x in numpy.cross(self.GetImageDirectionU(), self.GetImageDirectionN()).tolist()])                     # The Horizontal direction of the 2D image    UxN = H  
        self.SetDirectionMatrix(numpy.matrix([self.GetImageDirectionH(),self.GetImageDirectionU(),self.GetImageDirectionN()]))  # The direction matrix of the 2D image in 3D space.
        
    def SetCalibrationFileName(self,filename):
        '''Setting the Calibration Filename '''
        self.CalibrationFileName = filename

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
        
    def SetDirectionMatrix(self,directionMatrix):
        DirectionVnl = self.DirectionMatrix.GetVnlMatrix()
        DirectionVnl.set_identity()

        DirectionVnl.put(0,0,directionMatrix.item((0,0)))
        DirectionVnl.put(0,1,directionMatrix.item((0,1)))
        DirectionVnl.put(0,2,directionMatrix.item((0,2)))

        DirectionVnl.put(1,0,directionMatrix.item((1,0)))
        DirectionVnl.put(1,1,directionMatrix.item((1,1)))
        DirectionVnl.put(1,2,directionMatrix.item((1,2)))

        DirectionVnl.put(2,0,directionMatrix.item((2,0)))
        DirectionVnl.put(2,1,directionMatrix.item((2,1)))
        DirectionVnl.put(2,2,directionMatrix.item((2,2)))

    def GetDirectionMatrix(self):
        return self.DirectionMatrix
        
    def OpenDirectory(self, base_dir, image_path):
        self.camera_path = base_dir + image_path
        self.image_all = os.listdir(self.camera_path)

    def SetImageOrigin(self, origin):
        self.image_origin = origin

    def GetImageOriginX(self):
        return self.image_origin[0]

    def GetImageOriginY(self):
        return self.image_origin[1]

    def GetImageOriginZ(self):
        return self.image_origin[2]

    def SetImageSize(self, inputDir, inputFiles, pixelType):
        image = itk.imread(os.path.join(inputDir,inputFiles[0]),pixelType)
        region = image.GetLargestPossibleRegion()
        w, h = region.GetSize()
        z = len(inputFiles)

        self.image_size = [w, h, z]

    def GetImageSizeW(self):
        return self.image_size[0]

    def GetImageSizeH(self):
        return self.image_size[1]

    def GetImageSizeZ(self):
        return self.image_size[2]

    def GetImageSize(self):
        return self.image_size

    def GetImageOrigin(self):
        return self.image_origin

    def ShiftOrigin(self):
        w = self.GetImageSizeW()
        h = self.GetImageSizeH()
        '''Move the image origin from center to lower left for ITK '''
        deltaV = [x * ((float(w) / 2.0) * self.PixelSize[0]) for x in self.ImageDirectionHorizontal]
        deltaU = [x * ((float(h) / 2.0) * self.PixelSize[0]) for x in self.ImageDirectionUp]
        
        P = numpy.asarray([[float(x) * self.Offset_x for x in self.ImageDirectionHorizontal], [float(y) * self.Offset_y for y in self.ImageDirectionUp], 0])
        Q = numpy.asarray([deltaV, deltaU, 0])

        # origin = self.GetFocalPoint - [x * self.GetPrincipalDistance() for x in self.GetImageDirectionN()] - P - Q

        origin = [0,0,0]
        self.SetImageOrigin(origin)

    def Stack2DImage(self, inputDir):
        inputDimension = 2
        outputDimension = 3

        pixelType = itk.F

        inputImageType = itk.Image[pixelType, inputDimension]
        outputImageType = itk.Image[pixelType, outputDimension]

        reader = itk.ImageFileReader[inputImageType].New()

        img = itk.JoinSeriesImageFilter[inputImageType, outputImageType].New()
        
        inputFiles = os.listdir(inputDir)
        self.SetImageSize(inputDir, inputFiles, pixelType)

        for ii in range(0, self.GetImageSizeZ()):
            image = itk.imread(os.path.join(inputDir,inputFiles[ii]),pixelType)
            image.SetSpacing(self.GetPixelSize())
            img.SetInput(ii, image)
        
        img.SetSpacing(self.GetImageSizeZ())

        outputImg = self.SetMetadataIn3DImage(img, outputImageType)

        return outputImg

    def Write3DImageToFile(self, outputDir, outputName, img):
        outputDimension = 3
        pixelType = itk.F
        outputImageType = itk.Image[pixelType, outputDimension]
        
        index = itk.Index[outputDimension]()
        index.Fill(0)

        region = img.GetLargestPossibleRegion()
        size = region.GetSize()

        region.SetSize(size)
        region.SetIndex(index)

        img.SetRegions(region)
        img.Allocate(True)
        img.Update()

        writer = itk.ImageFileWriter[outputImageType].New()
        writer.SetFileName(os.path.join(outputDir,outputName))
        writer.SetInput(img)
        writer.Update()

    def SetMetadataIn3DImage(self, img, imageType):
        self.ShiftOrigin()
        spacing = img.GetSpacing()

        outputImg = itk.ChangeInformationImageFilter[imageType].New()
        outputImg.SetInput(img.GetOutput())
        
        outputImg.SetOutputSpacing(spacing)
        outputImg.ChangeSpacingOn()

        outputImg.SetOutputOrigin(self.GetImageOrigin())
        outputImg.ChangeOriginOn()
        
        outputImg.SetOutputDirection(self.GetDirectionMatrix())
        outputImg.ChangeDirectionOn()
        
        outputImg.UpdateOutputInformation()
                        
        return outputImg.GetOutput()

    def Get3DImageOutput(self, calibrationDir, inputDir, outputDir, outputFileName):
        self.SetCalibration(calibrationDir)
        img = self.Stack2DImage(inputDir)
        self.Write3DImageToFile(outputDir, outputFileName, img)

