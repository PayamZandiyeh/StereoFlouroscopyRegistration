# -*- coding: utf-8 -*-
'''Command line interface for utility functions'''

import click
from .util_dicom import dicom

@click.group()
def util():
    '''Various commands for utility functions'''
    pass

util.add_command(dicom)
