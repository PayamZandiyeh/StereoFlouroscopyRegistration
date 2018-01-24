# -*- coding: utf-8 -*-
'''Command line interface code for initialization of a project'''

import click
from .initialize_df_reg import df_reg

@click.group()
def init():
    '''Various commands for initialization of a project'''
    pass

init.add_command(df_reg)
