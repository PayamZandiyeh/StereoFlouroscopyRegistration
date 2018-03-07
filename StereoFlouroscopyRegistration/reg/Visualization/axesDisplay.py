import vtk
import numpy as np    

'''
    dispaly_axes(transformationMat)
    The code takes the 3D image transformation matrix and displays the coordinate system  
    
    Input: 
            transformationMat : 4 x 4 transformation matrix 
                                        - First 3 x 3 is the direction
                                        - Rows 1 to 3 in column 4 is the origin of the image.
    Output: 
            The axes of the coordinate system and it's origin. 

    
    Example:
            # Making artificial Data
            # -------------------------------------------------------------------
            
            directionMat = np.matrix([[1.,0.,0.],[0.,1.,0.],[0.,0.,1.]]) # Direction of matrices in x,y,z in each row
            originArray  = np.array([1.,1.,2.]) # The origin of the axes. 
            inputMatrix = vtk.vtkMatrix4x4(); 
            for i in range(3):
                for j in range(4):
                    if j !=3 :
                        inputMatrix.SetElement(i,j, directionMat[i,j])
                    else :
                        inputMatrix.SetElement(i,3,originArray[i])
            transformationMat = inputMatrix
            # -------------------------------------------------------------------
            display_axes(transfromationMat) # Calling the function
                

'''
def dispaly_axes(transformationMat): 
#%%
    originArray = np.zeros(3)
    for i in range(3):
        originArray[i] = transformationMat.GetElement(i,3)
     
    #create a Sphere
    sphereSource = vtk.vtkSphereSource()
    sphereSource.SetCenter(originArray)
    sphereSource.SetRadius(0.1)
    
    
    #create a mapper
    sphereMapper = vtk.vtkPolyDataMapper()
    sphereMapper.SetInputConnection(sphereSource.GetOutputPort())
     
    #create an actor
    sphereActor = vtk.vtkActor()
    sphereActor.SetMapper(sphereMapper)
     
    #a renderer and render window
    renderer = vtk.vtkRenderer()
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
     
    #an interactor
    renderWindowInteractor = vtk.vtkRenderWindowInteractor() 
    renderWindowInteractor.SetRenderWindow(renderWindow)
     
    #add the actors to the scene
    renderer.AddActor(sphereActor)
    # renderer.SetBackground(.1,.2,.3) # Background dark blue
    
    #Set the transformation to transform the axes+ origin to the desired location
    transform = vtk.vtkTransform()
    transform.SetMatrix(transformationMat)
    
    axes = vtk.vtkAxesActor()
    #  The axes are positioned with a user transform
    axes.SetUserTransform(transform)
         
    renderer.AddActor(axes)
     
    renderer.ResetCamera()
    renderWindow.Render()
     
    renderWindowInteractor.Start()