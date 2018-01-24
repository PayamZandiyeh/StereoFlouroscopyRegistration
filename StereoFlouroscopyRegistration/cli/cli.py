# -*- coding: utf-8 -*-
'''Command line interface entry point'''

import click
from .visualize.visualize import visualize
from .create.create import create
from .util.util import util

@click.group()
def main():
    pass

main.add_command(visualize)
main.add_command(create)
main.add_command(util)
