#!/usr/bin/env python
#coding=utf8

from string import Template
from optparse import OptionParser
from lib.cmdline import parse_args
from lib.scancore import AbstractScan
from lib.report import TEMPLATE_html

if __name__ == '__main__':
    args = parse_args()
    scanner = AbstractScan(args)
    scanner.run()