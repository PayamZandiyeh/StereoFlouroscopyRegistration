
inOrigin     = inputImage.GetOrigin()                   # Get the origin of the image.
inSpacing    = inputImage.GetSpacing()                  # Get the resolution of the input image.
inSize       = inputImage.GetBufferedRegion().GetSize() # Get the size of the input image.
inDirection  = inputImage.GetDirection()

#%% ------------------ Transformation 
# This part is inevitable since the interpolator (Ray-cast) and resample Image
# image filter uses a Transformation -- Here we set it to identity. 
TransformType = itk.CenteredEuler3DTransform[itk.D]
transform     = TransformType.New()

direction_mat = Functions.get_vnl_matrix(inDirection.GetVnlMatrix())

#rot = np.dot(-1,rot)           # Due to Direction of transform mapping ( 8.3.1 in the ITK manual)
#t   = np.dot(-1,t  )           # Due to Direction of transform mapping ( 8.3.1 in the ITK manual)
# Since this transform is for the movement of x-ray source and not the rigid body, therefore, no need to invert the rotation. 
#
#
rot = direction_mat.dot(np.transpose(rot))           
t   = direction_mat.dot(np.transpose(t  ))          


transform.SetRotation(np.deg2rad(rot[0]),np.deg2rad(rot[1]),np.deg2rad(rot[2])) # Setting the rotation of the transform
transform.SetTranslation(itk.Vector.D3(t))    # Setting the translation of the transform
transform.SetComputeZYX(True)  # The order of rotation will be ZYX. 

center = direction_mat.dot(inOrigin)+ np.multiply(inSpacing,inSize)/2. # Setting the center of rotation as center of 3D object + offset determined by cor. 
center = direction_mat.dot(center)-t # Convert the image to the local coordinate system. 
transform.SetCenter(center)                     # Setting the center of rotation. 
