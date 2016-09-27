##目录结构

    --lib 核心文件库

    --report 报告生成的文件夹

    --payload 里面每一个 py 文件是一个攻击插件

##使用方法
    python Dscan.py
    usage: Dscan.py [options]

    * Batch Vulnerability Scan Framework. *

    optional arguments:
    -h, --help   show this help message and exit
    -t THREADS   Num of scan threads for each scan process, 20 by default
    -i URL       input single url
    -f URL_FILE  input url file
    -n NAME      from payload floder choose a script
    -m NAME      select script scan method [verify|exploit]
    -v           show program's version number and exit


    **示例**
    ```
    python Dscan.py -n zabbix -f url.txt -m verify
    -n 指定 payload 文件夹下的 zabbix.py，-f 指定输入为 url 文件, -m 验证模式。
    ```
    ```
    python Dscan.py -n zabbix -i www.baidu.com -m exploit
    -i 指定输入为单个 url,-m 攻击模式。
    ```
    ```
    python Dscan.py -n all  -f url.txt -m verify
    -n all 指调用 payload 文件夹下所有的插件，-f 指定输入为 url 文件 ( 也可以指定 -i 参数 )。
    ```
    ```
    python Dscan.py -n zabbix,post -f url.txt -m exploit
    -n zabbix,post 指调用 payload 文件夹下多个指定插件 ( 这里指定 zabbix, post 两个插件 )，-f 指定输入为 url 文件 ( 也可以指定 -i 参数 )。
    ```
##安装
pip install -r requirements.txt

##其他

