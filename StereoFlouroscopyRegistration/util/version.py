# -*- coding: utf-8 -*-
'''Utility functions for getting the software version.'''

from __future__ import absolute_import, print_function
import subprocess

def get_git_version():
    '''
    Return the last tag from git using a subprocess call.

    This function may raise an EnvironmentError.
    '''
    # This defines the git command to grab the tag. Note that git uses grep(7) for
    # matching. This regex is not perfect.
    git_command = ['git', 'describe', '--match', 'v[0-9]*.[0-9]*.[0-9]']

    # Try to execute the git command. Throws a 'CalledProcessError' error if the call
    # returns a non-zero exit status.
    try:
        git_version = subprocess.check_output(
            git_command,
            stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        raise EnvironmentError('git returned non-zero exist status')

    return git_version

def format_version(git_version):
    '''
    Check the version is correct and format it. The checks are as follows:
        1) Starts with a v
        2) Has three components seperated by '.'
        3) Each component is a positive number
    '''
    # Internal util for raise errors
    def raise_bad_tag_error():
        '''Nested function for easy, modifiable error raising inside get_version'''
        raise EnvironmentError('git tag \'{}\' is not a proper version number'.format(git_version))

    if len(git_version) < 1 or git_version[0].lower() != 'v':
        raise_bad_tag_error()
    tag = git_version[1:]
    numbers = tag.split('.')
    if len(numbers) != 3:
        raise_bad_tag_error()

    new_numbers = []
    for number in numbers:
        # Can the string be converted to integer?
        try:
            value = int(number)
        except ValueError:
            raise_bad_tag_error()

        # Must be a positive integer
        if value < 0:
            raise_bad_tag_error()

        # Valid number
        new_numbers.append(value)

    # Format string and return
    version = 'v{0}.{1}.{2}'.format(*new_numbers)
    return version

def get_version():
    '''
    Returns the software version as a string. Versioning is determined by git tag and is
    set in the git pipeline. Version should follow 'v#.#.#' where '#' is a number. The
    three numbers are major, minor, and patch.

    This function may raise an EnvironmentError .
    '''

    return format_version(get_git_version())
