#%%
cal = CalibrationUsingJointTrack.CalibrationTool() # Setting up the image calibration info class. 
cal.SetCalibrationInfo(calibration_files[ii]) # Assign the information from the calibration file to the imageCalibrationInfo class. 

res= cal.GetPixelSize() # The resolution (spacing) along x,y,z directions of output image
spaceOutput = [res[0],res[1],1]
cal.SetOutputImageSize(sizeOutput[0],sizeOutput[1],1)  # Setting the size of the output image. 
cal.SetGlobalOriginForImagePlane()    

inDirection  = inputImage.GetDirection()
direction_mat = Functions.get_vnl_matrix(inDirection.GetVnlMatrix())

focalPoint      = cal.GetFocalPoint()
directionOutput = direction_mat*cal.GetDirectionMatrix()
originOutput    = itk.Point.D3(direction_mat.dot(cal.GetGlobalOriginForImagePlane()))


#focalPoint   = [0.0,0.0,50.0]
#originOutput = [-500,-500,-40.0]
#directionOutput = np.matrix([[ -1.,  0.,  0.],
#                             [  0.,  -1.,  0.],
#                             [  0.,  0.,  1.]])

if verbose:
    print(focalPoint)
    print(directionOutput)
    print(originOutput)