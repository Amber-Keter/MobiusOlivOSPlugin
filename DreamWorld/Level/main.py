 #模块导入区
import json                             #json序列化与反序列化模块
import re                               #正则表达式库，用于匹配指令
import os
from . import Basic
from . import User
from . import LevelLib

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
Basic.lib_dir = 'Level'

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
        try:
            Basic.ReadJson(Basic.path('Data',"Level"))
        except:
            Basic.WriteJson(Basic.path('Data',"Level"),{})
        try:
            Basic.ReadJson(Basic.path('Config',"Level"))
        except:
            data = {
                "Reply":"{nick}在{self}这的权限为{level}",
                "Default":0,
                "Separator":"-",
                "Level":{
                    "0":{
                        "name":"游客",
                        "info":"默认用户模式，可以使用所有基础功能"
                    },
                    "1":{
                        "name":"白名单",
                        "info":"白名单用户，可以使用部分进阶或受限制的功能"
                    },
                    "2":{
                        "name":"管理员",
                        "info":"管理员，可以赋予或删除非管理员的权限并持有管理权限"
                    },
                    "3":{
                        "name":"骰主",
                        "info":"Master，拥有除赋予或删除他人Master身份外的所有权限"
                    }
                },
                "List":{
                    "User":[0,1],
                    "Admin":[2],
                    "Master":[3]
                },
                "Help":{
                    "all":"【DreamWord】权限系统指令简介\n*level help [entry] #获取[entry]的详细信息。如：*level help set\n*level info #获取个人权限信息\n*level set [target] [level] #修改他人权限（仅限管理员）",
                    "set":"*level set [target] [level]:\n将[target]的权限设置为[level]，[target]格式可为@、uid、账号、平台-账号四种格式",
                    "info":"*level info:\n获取当前账号权限信息",
                }
            }
            Basic.WriteJson(Basic.path('Config',"Level"),data)
#这段加文件初始化



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
        self.all = Basic.ReadJson(Basic.path('Data','Level'))       #数据总集
        self.conf = Basic.ReadJson(Basic.path('Config','Level'))    #配置文件
        self.default = self.conf.get('Default',0)
        self.level = self.all.get(self.User.uid,self.default)
    
    def info(self):
        n:dict = self.conf.get('Level',{}).get(str(self.level),{})
        reply:str = self.conf.get('Reply',"{nick}在{self}这的权限为{level}")
        selfname = self.p.get_login_info()
        if selfname == None:
            selfname = {}
        selfname = selfname.get('data',{}).get("name",'')
        res = reply.format(nick=self.User.name,self=selfname,level = self.level)
        name = n.get('name','')
        info = n.get('info','')
        if name:
            separator = self.conf.get('Separator','-')
            res += f"{separator}{name}"
        if info:
            res += f"\n{info}"
        return res
    
    def set(self,uid,level:int):
        s = LevelLib.Level(self.User.uid)
        t = LevelLib.Level(uid)
        l:dict = self.conf.get("List",{})
        target = 'User'
        for k,v in l.items():
            if level in v:
                target = k
                break
        s_admin:bool = s.check('Admin') or s.check('Master') or LevelLib.CheckMaster(self.p)
        s_master:bool = s.check('Master') or LevelLib.CheckMaster(self.p)
        s_botmaster:bool = LevelLib.CheckMaster(self.p)
        t_admin:bool = t.check('Admin') or t.check('Master')
        t_master:bool = t.check('Master')
        if target == 'User':
            if (s_admin and not t_admin) or (s_master and not t_master) or s_botmaster:
                t.set(level)
                res = '设置成功√'
            else:
                res = '设置失败×\n原因：无授权指令'
        elif target == 'Admin':
            if (s_master and not t_master) or s_botmaster:
                t.set(level)
                res = '设置成功√'
            else:
                res = '设置失败×\n原因：无授权指令'
        elif target == 'Master':
            if s_botmaster:
                t.set(level)
                res = '设置成功√'
            else:
                res = '设置失败×\n原因：无授权指令'
        else:
            res = '设置失败×\n原因：未知权限'
        return res
    
    def help(self,entry:str):
        all_entry:dict = self.conf.get('Help',{})
        if entry:
            return all_entry.get(entry,"Error!词条不存在!")
        else:
            return all_entry.get('all',"Error!Help数据缺失!")
        

def ReplyFunction(plugin_event, Proc):
    temp = re.compile(r'\*level\s?(\S+)(\s[\s\S]+)?') # 正则匹配reply指令
    string = plugin_event.data.message  #接收到的消息内容
    reply = Level(plugin_event) 
    temp = temp.match(string)
    if temp:
        if temp.end() == len(string):
            head = temp.groups()[0]
            body = temp.groups()[1]
            if body:
                t = re.compile(r'\s*([\s\S]+)').match(body)
                if t:
                    body = t.groups()[0]
            if head == 'help':
                plugin_event.reply(reply.help(body))
            elif head == 'info':
                plugin_event.reply(reply.info())
            elif head == 'set':
                t = re.compile(r'(\S+)\s*(\S+)').match(body)
                if t:
                    u = t.groups()[0]
                    l = t.groups()[1]
                    l = int(l)
                    u = User.User(plugin_event,u)
                    plugin_event.reply(reply.set(u.uid,l))