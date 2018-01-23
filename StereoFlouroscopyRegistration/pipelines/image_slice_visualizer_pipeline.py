# -*- coding: utf-8 -*-
'''Prebuilt pipeline for visualizing a 2D and 3D medical images.'''

import os
import vtk
from .base_pipeline import BasePipeline

class ImageSliceVisualizer(BasePipeline):
    '''Prebuilt pipeline for visualizing a 2D and 3D medical images.

    Supports window/level, slicing, changing orientation, and chaning
    interpolation order.'''

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
        self.interactor_style.SetInteractionModeToImageSlicing()
        self.interactor_style.KeyPressActivationOn()
        self.interactor.SetInteractorStyle(self.interactor_style)

        # Add ability to switch between active layers
        self.interactor.AddObserver('KeyPressEvent', self._interactor_call_back, -1.0)

    def SetInputConnection(self, port):
        '''Set the input port.

        No tests are performed to validate the input.

        Args:
            port (int): The input connection port

        Returns:
            None
        '''
        self.image_mapper.SetInputConnection(port)

    def SetWindow(self, window):
        '''Set the window for displaying the image.

        No tests are performed to validate the input.

        Args:
            window (float): The window in native units.

        Returns:
            None
        '''
        self.image_property.SetColorWindow(window)

    def GetWindow(self):
        '''Get the window for displaying the image.

        Args:
            None

        Returns:
            float: the window
        '''
        return self.image_property.GetColorWindow()

    def SetLevel(self, level):
        '''Set the level for displaying the image.

        No tests are performed to validate the input.

        Args:
            level (float): The level in native units.

        Returns:
            None
        '''
        self.image_property.SetColorLevel(level)

    def GetLevel(self):
        '''Get the level for displaying the image.

        Args:
            None

        Returns:
            float: the level
        '''
        return self.image_property.GetColorLevel()

    def _determine_window_level(self, image):
        '''Attempt to determine a window and level for an image.

        The window is calculated as the dynamic range of the image data. This
        is different than the dynamic range of the image scalar type. The level
        is determined as half way between the min and max of the dynamic range.

        This function sets the window and level internally.

        Note that you should update the pipeline before calling this function.

        Args:
            image (vtk.vtkImageData):   The vtkImageData to based the window/level on.

        Returns:
            None
        '''
        scalar_ranges = image.GetScalarRange()
        window = scalar_ranges[1] - scalar_ranges[0]
        level = (scalar_ranges[1] + scalar_ranges[0])/2.0
        self.SetWindow(window)
        self.SetLevel(level)

    def set_render_window(self, render_window):
        '''Setup the render window.

        This class also estimates the window and level if an invalid option was given

        Args:
            render_window (vtk.vtkRenderWindow):    The render window created by the holding class.

        Returns:
            vtk.vtkRenderWindowInteractor:          The interactor created by the class with style ImageSlicing
        '''
        # Get Window/Level
        if self.image_property.GetColorLevel() == os.sys.float_info.min:
            # Update mapper and update so we can grab a scalar range
            self.image_mapper.Update()
            self._determine_window_level(self.image_mapper.GetInput())

            # Tell the user
            print('Estimated W/L: {}/{}'.format(self.GetWindow(), self.GetLevel()))

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
                w=self.GetWindow(),
                l=self.GetLevel()))
        elif str(self.interactor.GetKeyCode()) == 'n':
            # Set interpolation to nearest neighbour (good for voxel visualization)
            self.image_property.SetInterpolationTypeToNearest()
            self.interactor.Render()
        elif str(self.interactor.GetKeyCode()) == 'c':
            # Set interpolation to cubic (makes a better visualization)
            self.image_property.SetInterpolationTypeToCubic()
            self.interactor.Render()
