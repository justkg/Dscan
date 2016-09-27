#!/usr/bin/env python
#coding=utf8

import argparse
import sys
import os


p_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def check_args(args):
    if not (args.f or args.i):
        msg = 'Only use -f assign a file or use -i assign a site'
        raise Exception(msg)
    if args.f and not os.path.isfile(args.f):
        msg = 'TargetFile not found: %s' %args.f
        raise Exception(msg)
    if not args.n:
        msg = 'Only use -n assign a Script Name'
        raise Exception(msg)
    if args.m not in ('verify', 'exploit'):
        msg = 'Use -m to choose method'
        raise Exception(msg)


def parse_args():
    parser = argparse.ArgumentParser(prog='Scan',
        formatter_class=argparse.RawTextHelpFormatter,
        description='* Batch Vulnerability Scan Framework. *\n',
        usage='Dscan.py [options]')
    parser.add_argument('-t', metavar='THREADS', type=int, default=20,
        help='Num of scan threads for each scan process, 20 by default')
    parser.add_argument('-i', metavar='URL', type=str, help='input single url')
    parser.add_argument('-f', metavar='URL_FILE', type=str, help='input url file')
    parser.add_argument('-n', metavar='NAME', type=str, help='from payload floder choose a script')
    parser.add_argument('-m', metavar='NAME', type=str, help='select script scan method [verify|exploit]')
    parser.add_argument('-v', action='version', version='%(prog)s 1.0')

    if len(sys.argv) == 1:
        sys.argv.append('-h')
    args = parser.parse_args()
    check_args(args)
    return args