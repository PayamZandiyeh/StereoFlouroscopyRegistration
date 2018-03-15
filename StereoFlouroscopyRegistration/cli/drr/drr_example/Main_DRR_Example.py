execfile('Script_Libraries.py') # set the import libraries. 

input_filename  = 'transformed_ct.nii' # the ct volume. 

output_filename = ['test_cam1.nii', # output file name 1 
                   'test_cam2.nii'] # output file name 2

sizeOutput = [1000,1000,1] # The size of output image
threshold  = 0. 

rot = [0., 90.,  0.]     # NOT WORKING NOW __ rotation in degrees in x, y, and z direction. 
t   = [150. ,50. ,50.]   # NOT WORKING NOW __ translation in x, y, and z directions. 
cor = [0. ,0. ,0.]   # NOT WORKING NOW __ offset of the rotation from the center of image (3D)

verbose = False      # verbose details of all steps. 

transformed_vol = False # keep it for now -- in the future the transformed volume can be printed. 
calibration_files = ['cal_cam1.txt', # calibration file for camera 1 in sagittal plane
                     'cal_cam2.txt'] # calibration file for camera 2 in frontal plane

execfile('Script_Reader.py')    # Read the files. 
#%%
for ii in range(len(calibration_files)):
#%% Generating the drr 
    execfile('Script_SetCalibrationInfo.py')    # load calibration information of the calibraiton file. 
    execfile('Script_Transformation.py')        # Define the rigid body tansformation. 
    execfile('Script_RayCastInterpolator.py')   # ray cast filter initialize
    execfile('Script_Filters.py')               # resample image filter + rescale image filter. 
    execfile('Script_WriteImage.py')            # write the generated image. 
    
    
#%% For later. 
    #import itk_helpers as Functions 
##%%
## Transferring the 3D image so that the center of rotation of the image is located at global origin. 
#
#Functions.rigid_body_transform3D(input_filename='/Volumes/Storage/Projects/Registration/QuickData/OA-BEADS-CT.nii',\
#                                  output_filename='/Volumes/Storage/Projects/Registration/QuickData/transformed_ct.nii',\
#                                    t =[-1.14648438, 132.85351562, 502.09999385],rot = [-90.,0.,90.])

