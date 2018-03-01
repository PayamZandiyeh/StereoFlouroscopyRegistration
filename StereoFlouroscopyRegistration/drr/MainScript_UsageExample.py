#%%
import CalibrationUsingJointTrack as Calibration

#% -------------------------------- INPUTS --------------------------------- 
inputFileName  = "/Volumes/Storage/Projects/Registration/QuickData/Cam1_Trial2_N_FxBk_cd001_0001UNDIST.tif"
# '/Volumes/Storage/Projects/Registration/QuickData/OA-BEADS-CT.nii'
outputFileName = '/Volumes/Storage/Projects/Registration/QuickData/Output.nii'

calibrationFile = ['/Volumes/Storage/Projects/Registration/QuickData/OAKneeCadaverCd001_NM_Cam1.txt' ,    # Calibration file for Camera 1
                   '/Volumes/Storage/Projects/Registration/QuickData/OAKneeCadaverCd001_NM_Cam2.txt' ]    # Calibration file for Camera 2


inputDirectory =  '/Volumes/Storage/Projects/Registration/Data/CadaverKnee/DFData/Cam1UndistHist'

#%% Some Examples on how to generate appropriate codes. 

# Stacking example 
StackedImage = Calibration.StackingTool(calibrationFile[0],inputDirectory,outputFileName)
# With this line of code a 3D image will be generated with a correct meta data
#%%

# Example for writing a header file on a single 2D image (converts it to 3D)
ImageWithHeader = Calibration.CalibrationTool()
ImageWithHeader.SetCalibrationInfo(calibrationFile[0])
ImageWithHeader.SetImageHeader(inputFileName,outputFileName)
