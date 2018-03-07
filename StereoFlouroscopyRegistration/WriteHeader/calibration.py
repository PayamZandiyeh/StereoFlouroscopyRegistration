import os
from numpy import matrix as M
from calibration_tool import CalibrationTool

basedir = 'C:\Users\chris\Desktop\Calibration\CadaverData'
cam1_path = '\Cam1'
cam2_path = '\Cam2'
calibration_folder_path = '\Calibration'
file_name_suffix = '_cd001_NM_Calib_UP_0001UNDIST_JTCalibration.txt'
output_path = 'OUTPUT'

camera_1 = CalibrationTool()
camera_1.get_calibration_data(basedir, calibration_folder_path, cam1_path + file_name_suffix)
camera_1.open_directory(basedir, cam1_path)
camera_1.write_new_image(output_path)

camera_2 = CalibrationTool()
camera_2.get_calibration_data(basedir, calibration_folder_path, cam2_path + file_name_suffix)
camera_2.open_directory(basedir, cam2_path)
camera_2.write_new_image(output_path)

test = CalibrationTool()
test.write_3d('C:\Users\chris\Desktop\Calibration\CadaverData\Model\OA-BEADS-CT.nii','C:\Users\chris\Desktop\Calibration\CadaverData\Model\OUTPUT','OA-BEADS-CT.nii')