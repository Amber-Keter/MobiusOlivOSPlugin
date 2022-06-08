'''
                        _               _  __    _
        /\             | |             | |/ /   | |
       /  \   _ __ ___ | |__   ___ _ __| ' / ___| |_ ___ _ __
      / /\ \ | '_ ` _ \| '_ \ / _ \ '__|  < / _ \ __/ _ \ '__|
     / ____ \| | | | | | |_) |  __/ |  | . \  __/ ||  __/ |
    /_/    \_\_| |_| |_|_.__/ \___|_|  |_|\_\___|\__\___|_|
    DW基础模块  by Dr.Amber
    问题反馈请加QQ：1761089294
    Email：amberketer@outlook.com

'''

import json

lib_dir = ""

#读取json文件函数
def ReadJson(path:str):
    with open(path,"r",encoding='utf8') as f:
        res:dict = json.load(f)
        return res

#写入json文件函数
def WriteJson(path:str,data:dict):
    with open(path,"w",encoding='utf8') as f:
        json.dump(data,f,indent=4,ensure_ascii=False)

#地址函数
def path(p:str,dir=lib_dir):
    s:str = 'plugin/data/DreamWorld/{}/{}.json'.format(dir,p)
    return s