# -*- coding: utf-8 -*-
'''Prebuilt pipeline for visualizing a dual flouroscope scene.'''

from .base_pipeline import BasePipeline
import vtk
from StereoFlouroscopyRegistration.util.vtk_helpers import create_vtkMatrix4x4, GetRGBColor

class DualFlouroSceneVisualizer(BasePipeline):
    '''Prebuilt pipeline for visualizing a dual flouroscope scene.

    To solve the orientation problem, the user must supply a transform in homogeneous
    coordinates. Internally, the orientation of the image data is dropped. This way,
    we visualize the data with proper orientation with respect to each other.
    '''

    def __init__(self):
        super(DualFlouroSceneVisualizer, self).__init__()

        # Remove origin information
        self.xray_changer_1 = vtk.vtkImageChangeInformation()
        self.xray_changer_1.SetOutputOrigin(0, 0, 0)
        self.xray_changer_2 = vtk.vtkImageChangeInformation()
        self.xray_changer_2.SetOutputOrigin(0, 0, 0)
        self.ct_changer = vtk.vtkImageChangeInformation()
        self.ct_changer.SetOutputOrigin(0, 0, 0)

        # Setup mapper and actor for x-ray images
        self.xray_mapper_1 = vtk.vtkImageSliceMapper()
        self.xray_mapper_1.SetInputConnection(self.xray_changer_1.GetOutputPort())
        self.xray_mapper_2 = vtk.vtkImageSliceMapper()
        self.xray_mapper_2.SetInputConnection(self.xray_changer_2.GetOutputPort())

        self.xray_property = vtk.vtkImageProperty()
        self.xray_property.SetInterpolationTypeToNearest()

        self.xray_slice_1 = vtk.vtkImageSlice()
        self.xray_slice_1.SetMapper(self.xray_mapper_1)
        self.xray_slice_1.SetProperty(self.xray_property)

        self.xray_slice_2 = vtk.vtkImageSlice()
        self.xray_slice_2.SetMapper(self.xray_mapper_2)
        self.xray_slice_2.SetProperty(self.xray_property)

        self.marchingCubes = vtk.vtkImageMarchingCubes()
        self.marchingCubes.SetInputConnection(self.ct_changer.GetOutputPort())
        self.marchingCubes.ComputeGradientsOn()
        self.marchingCubes.ComputeNormalsOn()
        self.marchingCubes.ComputeScalarsOn()
        self.marchingCubes.SetNumberOfContours(1)
        self.marchingCubes.SetValue(0, 0)

        self.ct_mapper = vtk.vtkPolyDataMapper()
        self.ct_mapper.SetInputConnection(self.marchingCubes.GetOutputPort())
        self.ct_mapper.ScalarVisibilityOff()
        self.ct_actor = vtk.vtkActor()
        self.ct_actor.SetMapper(self.ct_mapper)
        self.ct_actor.GetProperty().SetInterpolationToGouraud()
        self.ct_actor.GetProperty().SetColor(GetRGBColor('antique_white'))

        self.renderer = vtk.vtkRenderer()
        self.renderer.AddViewProp(self.ct_actor)
        self.renderer.AddViewProp(self.xray_slice_1)
        self.renderer.AddViewProp(self.xray_slice_2)
        self.renderer.SetBackground(0.1, 0.2, 0.3)

        self.interactor = vtk.vtkRenderWindowInteractor()
        self.interactor_style = vtk.vtkInteractorStyleTrackballCamera()
        self.interactor.SetInteractorStyle(self.interactor_style)

    def SetCTInputConnection(self, port):
        '''Set the input port for the CT volume.

        No tests are performed to validate the input.

        Args:
            port (int): The input connection port

        Returns:
            None
        '''
        self.ct_changer.SetInputConnection(port)
        self.marchingCubes.SetUpdateExtentToWholeExtent() # DO NOT REMOVE!

    def SetCam1InputConnection(self, port):
        '''Set the input port for camera 1.

        No tests are performed to validate the input.

        Args:
            port (int): The input connection port

        Returns:
            None
        '''
        self.xray_changer_1.SetInputConnection(port)

    def SetCam2InputConnection(self, port):
        '''Set the input port for camera 2.

        No tests are performed to validate the input.

        Args:
            port (int): The input connection port

        Returns:
            None
        '''
        self.xray_changer_2.SetInputConnection(port)

    def SetCTOrientationMatrix(self, matrix):
        '''Set the display matrix for the CT volume.

        No tests are performed to validate the input.

        Args:
            matrix (np.array):  The rotation and translation in homogeneous coordiantes

        Returns:
            None
        '''
        self.ct_actor.PokeMatrix(create_vtkMatrix4x4(matrix))
        self.marchingCubes.SetUpdateExtentToWholeExtent() # DO NOT REMOVE!

    def SetCam1OrientationMatrix(self, matrix):
        '''Set the display matrix for camera 1.

        No tests are performed to validate the input.

        Args:
            matrix (np.array):  The rotation and translation in homogeneous coordiantes

        Returns:
            None
        '''
        self.xray_slice_1.PokeMatrix(create_vtkMatrix4x4(matrix))

    def SetCam2OrientationMatrix(self, matrix):
        '''Set the display matrix for camera 2.

        No tests are performed to validate the input.

        Args:
            matrix (np.array):  The rotation and translation in homogeneous coordiantes

        Returns:
            None
        '''
        self.xray_slice_2.PokeMatrix(create_vtkMatrix4x4(matrix))

    def SetMarchingCubesValue(self, value):
        '''Set the value for marching cubes.

        A contour is computed through the image data at this value. See
        vtkImageMarchingCubes for more information.

        Args:
            value (float):  The contour value

        Returns:
            None
        '''
        self.marchingCubes.SetValue(0, value)
        self.marchingCubes.SetUpdateExtentToWholeExtent() # DO NOT REMOVE!

    def SetCamWindow(self, window):
        '''Set the window for both camera 1 and 2.

        The camera 1 and 2 have the same window and level.

        Args:
            window (float): The window value

        Returns:
            None
        '''
        self.xray_property.SetColorWindow(window)

    def SetCamLevel(self, level):
        '''Set the level for both camera 1 and 2.

        The camera 1 and 2 have the same window and level.

        Args:
            level (float):  The level value

        Returns:
            None
        '''
        self.xray_property.SetColorLevel(level)

    def set_render_window(self, render_window):
        '''Setup the render window.

        Args:
            render_window (vtk.vtkRenderWindow):    The render window created by the holding class.

        Returns:
            vtk.vtkRenderWindowInteractor:          The interactor created by the class with style ImageSlicing
        '''

        # Add renderer to render window
        render_window.AddRenderer(self.renderer)
        self.interactor.SetRenderWindow(render_window)
        self.renderer.ResetCamera()

        return self.interactor
