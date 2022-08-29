 #模块导入区
import json                             #json序列化与反序列化模块
import re                               #正则表达式库，用于匹配指令
import time
import os
import sys
import Basic
import User

'''
                        _               _  __    _
        /\             | |             | |/ /   | |
       /  \   _ __ ___ | |__   ___ _ __| ' / ___| |_ ___ _ __
      / /\ \ | '_ ` _ \| '_ \ / _ \ '__|  < / _ \ __/ _ \ '__|
     / ____ \| | | | | | |_) |  __/ |  | . \  __/ ||  __/ |
    /_/    \_\_| |_| |_|_.__/ \___|_|  |_|\_\___|\__\___|_|
    DW用户系统  by Dr.Amber
    问题反馈请加QQ：1761089294
    Email：amberketer@outlook.com

'''


#事件区
class Event(object):
    def init(plugin_event, Proc):
        if not os.path.exists("plugin/data/DreamWorld"):
            os.mkdir("plugin/data/DreamWorld")
        if not os.path.exists("plugin/data/DreamWorld/Level"):
            os.mkdir("plugin/data/DreamWorld/Level")
        if not os.path.exists("plugin/lib"):
            os.mkdir("plugin/lib")
        if not os.path.exists("plugin/lib/DreamWorldLib"):
            os.mkdir("plugin/lib/DreamWorldLib")
        if 'plugin/lib/DreamWorldLib' not in sys.path:
            sys.path.insert(1,'plugin/lib/DreamWorldLib')
        try:
            Basic.ReadJson(Basic.path('Data'))
        except:
            data={
                    "User":{},
                    'Link':{},
                    'Guest':{},
                    'Help':{
                        'all':"【DreamWord】用户系统指令简介\n*user help [entry] #获取[entry]的详细信息。如：*user help link\n*user info #获取账号信息\n*user nn [NewName] #变更账户昵称为[NewName]\n*user link [Target] #申请与[Target]关联\n*user accept [Token] #接受关联申请\n*user close #断开当前关联",
                        'link':"*user link [Target]:\n申请与[Target]关联，骰娘将返回[Token]，用于被关联账号验证。\n需注意，当已有关联账户时关联其他账户将断开先前的关联\n[Target]格式：@格式、uuid格式、[platform]-[id]、[id]\n其中，[platform]代表目标账户的平台，[id]代表目标的账户，若使用第四种格式，则[platform]默认为当前平台。",
                        'close':"*user close:\n断开当前关联。",
                        'accept':"*user accept [Token]:\n接受关联申请\n[Token]在申请关联时骰娘的回执内容中，格式为[uuid]#[uuid]",
                        'nn':"*user nn [NewName]:\n将你的账号的昵称更改为[NewName]\n需注意，本指令只更改本用户，但更改后的昵称将被所有关联者使用。",
                        'info':"*user info:\n获取你的账号信息。"
                    }
                }
            with open("plugin/data/DreamWorld/User/Data.json","w",encoding="utf-8") as file:
                json.dump(data, file,indent=4,ensure_ascii=False)
        try:
            Basic.ReadJson(Basic.path('Token'))
        except:
            data={}
            with open("plugin/data/DreamWorld/User/Token.json","w",encoding="utf-8") as file:
                json.dump(data, file,indent=4,ensure_ascii=False)
    def private_message(plugin_event, Proc):
        ReplyFunction(plugin_event,Proc)
    #私聊
    def group_message(plugin_event, Proc):
        ReplyFunction(plugin_event,Proc)
    #群聊
    def save(plugin_event,Proc):
        pass

class Level:
    def __init__(self,plugin_event):
        self.p = plugin_event
        self.User = User.User(self.p)
        self.all = Basic.ReadJson(Basic.path('Data'))
        self.conf = Basic.ReadJson(Basic.path('Config'))
        self.default = self.conf.get('Default',0)
        self.level = self.all.get(self.User.uid,self.default)
    
    def info(self):
        n = self.conf.get('Level',{}).get(str(self.level),{})
        res = "{nick}在{self}这的权限为{level}".format(nick=self.User.name,self=self.p.bot_info.name,level = self.level)
        
        
        

def ReplyFunction(plugin_event, Proc):
    pass