#!/usr/bin/env python
#coding=utf8

import threading
import glob
from Queue import Queue
import sys
import time
import os
from termcolor import colored
from report import TEMPLATE_html, TEMPLATE_li
from string import Template

'''load script class'''
class ScanFrame:
    def __init__(self, ui_list, thread_num, script_name, method):
        self.ui_list = ui_list
        self.thread_num = thread_num
        self.script_name = script_name
        self.method = method

    def scan(self):
        f = open('res.txt', 'w+')
        global rres
        rres = []
        queue = Queue()
        for i in xrange(self.thread_num):
            worker = SriptThread(queue,self.method)
            worker.daemon = True
            worker.start()
        for ui in self.ui_list:
            for scriptn in self.script_name:
                queue.put((ui, f, rres, scriptn))
        queue.join()

    ''' get report '''
    def script_report(self):
        report_name = 'Dscan_' + time.strftime('%Y%m%d_%H%M%S', time.localtime()) + '.html' 
        report_path = os.path.dirname(os.path.dirname(__file__)) + os.sep + 'report' + os.sep
        t_html = Template(TEMPLATE_html)
        t_li = Template(TEMPLATE_li)
        _str = ""
        for ele in rres:
            # _str += t_li.substitute({'href':ele[0], 'scriptname':ele[1], 'msg':ele[2]})
            _str += t_li.substitute({'href':ele[0], 'msg':ele[1]})
        html_doc = t_html.substitute({'content':_str})
        with open(report_path+report_name, 'w') as outFile:
            outFile.write(html_doc)
        print 
        print colored('Report saved to report/%s' % report_name, 'green')


'''script threads'''
class SriptThread(threading.Thread):
    def __init__(self, queue, method):
        threading.Thread.__init__(self)
        self.queue = queue
        self.method = method

    def run(self):
        # sys.path.append("..")
        if self.method == 'exploit':
            while True:
                ui, f, rres, script_name = self.queue.get()
                mod = script_name
                __import__(mod)
                try:
                    res = sys.modules[mod].exploit(ui)
                    if True in res:
                        mlock = threading.Lock()
                        mlock.acquire()
                        rres.append((res[1], mod.split('.')[1], res[2]))
                        # rres.append((res[1], res[2]))
                        print '[+]{0:50}{1}{2}'.format(res[1], mod.split('.')[1] + '.py: ',res[2])
                        f.write(res[1]+'\n')
                        mlock.release()
                    else:
                        mlock = threading.Lock()
                        mlock.acquire()
                        # rres.append((res[1], mod.split('.')[1], res[2]))
                        print '[-]{0:60}{1}{2}'.format(res[1], mod.split('.')[1] + '.py: ',res[2])
                        mlock.release()
                except Exception, e:
                    print str(e)
                    pass
                self.queue.task_done()
        else:
            while True:
                ui, f, rres, script_name = self.queue.get()
                mod = script_name
                __import__(mod)
                try:
                    res = sys.modules[mod].verify(ui)
                    if True in res:
                        mlock = threading.Lock()
                        mlock.acquire()
                        rres.append((res[1], mod.split('.')[1], res[2]))
                        print '[+]{0:60}{1}{2}'.format(res[1], mod.split('.')[1] + '.py: ',res[2])
                        f.write(res[1]+'\n')
                        mlock.release()
                    else:
                        mlock = threading.Lock()
                        mlock.acquire()
                        print '[-]{0:60}{1}{2}'.format(res[1], mod.split('.')[1] + '.py: ',res[2])
                        mlock.release()
                except Exception, e:
                    print str(e)
                    pass
                self.queue.task_done()
