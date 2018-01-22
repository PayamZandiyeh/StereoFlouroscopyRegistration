# -*- coding: utf-8 -*-
'''Base class for all prebuilt pipeplines'''

from abc import ABCMeta, abstractmethod

class BasePipeline:
    '''Abstract class for implementing'''
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def set_render_window(self, render_window):
        '''All derived classes handle setting the render window'''
        pass
