# -*- coding: utf-8 -*-
'''Prebuilt pipeline for reading in and visualizing a 2D medical image'''

from .base_pipeline import BasePipeline
import vtk

class ImageSliceVisualizer(BasePipeline):
    '''Prebuilt pipeline for visualizaing a 2D image slice'''

    def __init__(self):
        super(ImageSliceVisualizer, self).__init__()

        # Setup pipeline
        self.image_mapper = vtk.vtkImageSliceMapper()
        self.image_mapper.SliceAtFocalPointOn()
        self.image_mapper.SliceFacesCameraOn()

        self.image_property = vtk.vtkImageProperty()
        self.image_property.SetInterpolationTypeToNearest()

        self.image_slice = vtk.vtkImageSlice()
        self.image_slice.SetMapper(self.image_mapper)
        self.image_slice.SetProperty(self.image_property)

        self.renderer = vtk.vtkRenderer()
        self.renderer.AddActor2D(self.image_slice)

        self.interactor = vtk.vtkRenderWindowInteractor()
        self.interactor_style = vtk.vtkInteractorStyleImage()

    def SetInputConnection(self, port):
        self.image_mapper.SetInputConnection(port)

    def SetWindow(self, window):
        self.image_property.SetColorWindow(window)

    def SetLevel(self, level):
        self.image_property.SetColorLevel(level)

    def set_render_window(self, render_window):
        # Get Window/Level
        if self.image_property.GetColorLevel() < 0:
            # Update mapper and update so we can grab a scalar range
            self.image_mapper.Update()
            image = self.image_mapper.GetInput()
            scalar_ranges = image.GetScalarRange()

            # Determine window/level. This is difficult to do, but just using
            # the range works ~50% of the time.
            window = scalar_ranges[1] - scalar_ranges[0]
            level = (scalar_ranges[1] + scalar_ranges[0])/2.0
            self.SetWindow(window)
            self.SetLevel(level)

            # Tell the user
            print('Estimated W/L: {}/{}'.format(window, level))

        # Add renderer to render window
        render_window.AddRenderer(self.renderer)

        self.interactor_style.SetInteractionModeToImageSlicing()
        self.interactor_style.KeyPressActivationOn()

        self.interactor.SetInteractorStyle(self.interactor_style)
        self.interactor.SetRenderWindow(render_window)

        # Add ability to switch between active layers
        self.interactor.AddObserver('KeyPressEvent', self._interactor_call_back, -1.0)

        return self.interactor

    def _interactor_call_back(self, obj, event):
        if str(self.interactor.GetKeyCode()) == 'w':
            # Print the current window and level
            print('Image W/L: {w}/{l}'.format(
                w=self.image_property.GetColorWindow(),
                l=self.image_property.GetColorLevel()))
        elif str(self.interactor.GetKeyCode()) == 'n':
            # Set interpolation to nearest neighbour (good for voxel visualization)
            self.image_property.SetInterpolationTypeToNearest()
            self.interactor.Render()
        elif str(self.interactor.GetKeyCode()) == 'c':
            # Set interpolation to cubic (makes a better visualization)
            self.image_property.SetInterpolationTypeToCubic()
            self.interactor.Render()
