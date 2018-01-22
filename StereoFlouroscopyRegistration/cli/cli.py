# -*- coding: utf-8 -*-
'''Command line interface entry point'''

import click
from .visualize.visualize import visualize

@click.group()
def main():
    pass

main.add_command(visualize)
