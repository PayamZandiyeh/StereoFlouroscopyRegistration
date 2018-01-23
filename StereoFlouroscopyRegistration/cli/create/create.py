# -*- coding: utf-8 -*-
'''Command line interface for creating'''

import click
from .create_example_df_data import df_example

@click.group()
def create():
    '''Various commands for creating example data'''
    pass

create.add_command(df_example)