# -*- coding: utf-8 -*-
'''Prebuilt pipeline for visualizing a dual flouroscope scene.'''

from .base_pipeline import BasePipeline
import vtk
from StereoFlouroscopyRegistration.util.vtk_helpers import create_vtkMatrix4x4, GetRGBColor

class DualFlouroSceneVisualizer(BasePipeline):
    '''Prebuilt pipeline for visualizing a dual flouroscope scene.

    Interactivity rotates the scene around.'''

    def __init__(self):
        super(DualFlouroSceneVisualizer, self).__init__()

        # Setup mapper and actor for x-ray images
        self.xray_mapper_1 = vtk.vtkImageSliceMapper()
        self.xray_mapper_2 = vtk.vtkImageSliceMapper()

        self.xray_property = vtk.vtkImageProperty()
        self.xray_property.SetInterpolationTypeToNearest()

        self.xray_slice_1 = vtk.vtkImageSlice()
        self.xray_slice_1.SetMapper(self.xray_mapper_1)
        self.xray_slice_1.SetProperty(self.xray_property)

        self.xray_slice_2 = vtk.vtkImageSlice()
        self.xray_slice_2.SetMapper(self.xray_mapper_2)
        self.xray_slice_2.SetProperty(self.xray_property)

        self.marchingCubes = vtk.vtkImageMarchingCubes()
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

        self.interactor = vtk.vtkRenderWindowInteractor()
        self.interactor_style = vtk.vtkInteractorStyleTrackballCamera()
        self.interactor.SetInteractorStyle(self.interactor_style)

        # Add ability to switch between active layers
        self.interactor.AddObserver('KeyPressEvent', self._interactor_call_back, -1.0)

    def SetCTInputConnection(self, port):
        self.marchingCubes.SetInputConnection(port)
        self.marchingCubes.SetUpdateExtentToWholeExtent() # DO NOT REMOVE!

    def SetCam1InputConnection(self, port):
        self.xray_mapper_1.SetInputConnection(port)

    def SetCam2InputConnection(self, port):
        self.xray_mapper_2.SetInputConnection(port)

    def SetCam1OrientationMatrix(self, matrix):
        self.xray_slice_1.PokeMatrix(create_vtkMatrix4x4(matrix))

    def SetCam2OrientationMatrix(self, matrix):
        self.xray_slice_2.PokeMatrix(create_vtkMatrix4x4(matrix))

    def SetCTOrientationMatrix(self, matrix):
        self.ct_actor.PokeMatrix(create_vtkMatrix4x4(matrix))
        self.marchingCubes.SetUpdateExtentToWholeExtent() # DO NOT REMOVE!

    def SetMarchingCubesValue(self, value):
        self.marchingCubes.SetValue(0, value)
        self.marchingCubes.SetUpdateExtentToWholeExtent() # DO NOT REMOVE!

    def SetCamWindow(self, window):
        self.xray_property.SetColorWindow(window)

    def SetCamLevel(self, level):
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

    def _interactor_call_back(self, obj, event):
        '''Call back function for keyboard interaction.

        The following functionally is defined:
            w   Print the window/level to screen
            n   Set interpolation type to nearest neighbour
            c   Set interpolation type to cubic

        Args:
            obj (vtk.vtkRenderWindowInteractor):    The object which called the function
            event (str):                            A string containing the event name

        Returns:
            None
        '''
        if str(self.interactor.GetKeyCode()) == 'w':
            # Print the current window and level
            print('Image W/L: {w}/{l}'.format(
                w=self.GetCamWindow(),
                l=self.GetCamLevel()))
        elif str(self.interactor.GetKeyCode()) == 'n':
            # Set interpolation to nearest neighbour (good for voxel visualization)
            self.xray_property.SetInterpolationTypeToNearest()
            self.interactor.Render()
        elif str(self.interactor.GetKeyCode()) == 'c':
            # Set interpolation to cubic (makes a better visualization)
            self.xray_property.SetInterpolationTypeToCubic()
            self.interactor.Render()
