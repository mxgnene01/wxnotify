#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import os
import sys


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == 'publish':
            os.system('make publish')
            sys.exit()
        elif sys.argv[1] == 'release':
            if len(sys.argv) < 3:
                type_ = 'patch'
            else:
                type_ = sys.argv[2]
            assert type_ in ('major', 'minor', 'patch')

            os.system('bumpversion {}'
                      .format(type_))
            sys.exit()

    setup(setup_requires=['pbr'], pbr=True)


if __name__ == '__main__':
    main()
