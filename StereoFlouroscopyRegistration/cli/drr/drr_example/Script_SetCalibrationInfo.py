#%%
cal = CalibrationUsingJointTrack.CalibrationTool() # Setting up the image calibration info class. 
cal.SetCalibrationInfo(calibration_files[ii]) # Assign the information from the calibration file to the imageCalibrationInfo class. 

res= cal.GetPixelSize() # The resolution (spacing) along x,y,z directions of output image
spaceOutput = [res[0],res[1],1]
cal.SetOutputImageSize(sizeOutput[0],sizeOutput[1],1)  # Setting the size of the output image. 
cal.SetGlobalOriginForImagePlane()    

focalPoint      = cal.GetFocalPoint()
directionOutput = cal.GetDirectionMatrix()
originOutput    = cal.GetGlobalOriginForImagePlane()