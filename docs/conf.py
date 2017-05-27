#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
my_tcpconn  conf
~~~~~~~~~~~~~~~~~~~~~
@time: 2017/5/27 15:45
@contact: a@b.com
usage:


links:

:copyright: 
:license: BSD 3-Clause License
"""
import sys
import os
from recommonmark.parser import CommonMarkParser

source_parsers = {
    '.md': CommonMarkParser,
}

source_suffix = ['.rst', '.md']