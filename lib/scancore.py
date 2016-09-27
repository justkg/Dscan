#!/usr/bin/env python
#coding=utf8
import os
import sys
import re
import requests
import urlparse
import ConfigParser
from scanframe import ScanFrame
from cmdline import parse_args

class AbstractScan():
    def __init__(self, args):
        self.args = args

    '''parse url or ip_url'''
    def parse_url(self, url_list):
        url_res = []
        for url in url_list:
            try:
                _ = urlparse.urlparse(url, 'http')
                if not _.netloc:
                    _ = urlparse.urlparse('http://' + url, 'http')
                if _.port == 443:
                    _url = "https://" + _.netloc
                else:
                    _url = _.scheme + '://' + _.netloc
                if _.path:
                    _url += _.path
                else:
                    _url += '/' 
                url_res.append(_url)
            except Exception, e:
                pass
        return url_res

    '''parse script name'''
    def parse_script(self, script_name):
        sn = []
        for script in script_name.split(','):
            try:
                scriptname = "payload"+ os.sep +  script  + ".py"
                if not os.path.exists(scriptname):
                    print "[-]Error Message! %s  Script not exitst!" % script
                    sys.exit()
                else:
                    script = "payload." + script
                    sn.append(script)
            except Exception, e:
                pass
        return sn

    '''get all script name'''
    def getAllscript(self,payload):
        script = []
        f_list = os.listdir(payload)
        for i in f_list:
            if os.path.splitext(i)[1] == '.py':
                if i !="__init__.py":
                    script.append('payload.' + os.path.splitext(i)[0])
        return script

    '''scan use script method'''
    def scan_script(self):
        thread_num = self.args.t
        script_name = self.args.n

        if script_name == "all":
            pay = os.path.dirname(os.path.dirname(__file__)) + os.sep + 'payload' + os.sep
            script_name = self.getAllscript(pay)
        else:
            script_name = self.parse_script(script_name)

        '''handle url file''' 
        if self.args.f:
            url_file = self.args.f
            if not os.path.exists(url_file):
                print "[-]Error Message! Url File not exitst!"
                sys.exit()
            with open(url_file, 'r') as url:
                url_list = url.read().split('\n')
            func = lambda url_list: url_list if ''.join(url_list[-1:]) else url_list[:-1]
            url_list = func(url_list)
            url_list = self.parse_url(url_list)
            # print "--------------------"
            # print url_list
            # print "--------------------"
            sscanner = ScanFrame(url_list, thread_num, script_name,self.args.m)

        '''handle url'''
        if self.args.i:
            site = self.args.i
            url_list = []
            if not site:
                print "[-]Error Message! Url not Found!"
                sys.exit()
            url_list.append(''.join(site))
            url_list = self.parse_url(url_list)
            sscanner = ScriptFrame(url_list, thread_num, script_name,self.args.m)

        sscanner.scan()
        sscanner.script_report()

    '''scanning method'''
    def run(self):
        if self.args.f or self.args.i:
            self.scan_script()
        else:
            raise Exception('[-]Error Message! You should give correct args')
