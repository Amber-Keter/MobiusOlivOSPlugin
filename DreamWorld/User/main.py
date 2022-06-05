 #模块导入区
import json                             #json序列化与反序列化模块
import re                               #正则表达式库，用于匹配指令
import time
import OlivaDiceCore
import os
import uuid
import sys


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
        if not os.path.exists("plugin/data/DreamWorld/User"):
            os.mkdir("plugin/data/DreamWorld/User")
        try:
            ReadJson(path('Data'))
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
            ReadJson(path('Token'))
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



#函数区
#读取json文件函数
def ReadJson(path:str):
    with open(path,"r",encoding='utf8') as f:
        return json.load(f)

#写入json文件函数
def WriteJson(path:str,data:dict):
    with open(path,"w",encoding='utf8') as f:
        json.dump(data,f,indent=4,ensure_ascii=False)

#地址函数
def path(p:str):
    return 'plugin/data/DreamWorld/User/{}.json'.format(p)

#MID函数
def MID(s:str,plugin_event = None,User = None):
    platform = plugin_event.platform['platform']
    reList = [r'\[cq:at,qq=(\S+)\]',r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})']
    reL = []
    for i in reList:
        i = re.compile(i).match(s)
        if i :
            if i.end() != len(s):
                reL.append(False)
                continue
        reL.append(i)
    if type(User) is not dict:
        User:dict = ReadJson(path('Data'))
    if reL[0]:
        id = reL[0].groups()[0]
    elif reL[1]:
        uid = reL[1].groups()[0]
        if uid in User.get('User',{}).keys():
            return (True,uid)
        else:
            return (False,"无记录用户")
    else:
        if '-' in s:
            t = s.split('-')
            platform = t[0]
            id = t[1]
        else:
            id = s
    uid = User.get('Guest',{}).get(platform,{}).get(id,None)
    if uid:
        return (True,uid)
    else:
        return (False,"无记录用户")



#User类
class User:
    def __init__(self,plugin_event) -> None:
        self.p = plugin_event
        self.id:str = str(plugin_event.data.user_id)
        self.platform = plugin_event.platform['platform']
        self.group = None
        if 'host_id' in plugin_event.data.__dict__:            
            self.group = str(plugin_event.data.host_id)
        if 'group_id' in plugin_event.data.__dict__ :
            self.group = str(plugin_event.data.group_id)
        self.name = plugin_event.data.sender["nickname"]
        self.User:dict = ReadJson(path('Data'))
        if self.id not in self.User.get('Link',{}).get(self.platform,{}).keys():
            if self.User['Link'].get(self.platform,None) == None:
                self.User['Link'][self.platform] = {}
            if self.User['Guest'].get(self.platform,None) == None:
                self.User['Guest'][self.platform] = {}
            self.User['Link'][self.platform][self.id] = 'guest'
            uid = str(uuid.uuid4())
            while uid in self.User.get('User',{}).keys():
                uid = str(uuid.uuid4())
            self.User['Guest'][self.platform][self.id] = uid
            t = {'id':self.id,'platform':self.platform,'name':self.name}
            self.User['User'][uid] = t
            self.uid = uid
            self.save()
        else:
            self.uid = self.User['Guest'][self.platform][self.id]
            self.name = self.User['User'][self.uid]['name']



    def save(self):
        WriteJson(path('Data'),self.User)   #写入到指定文件里去

    def help(self,entry=None):
        all_entry:dict = self.User.get('Help',{})
        if entry:
            return all_entry.get(entry,"Error!词条不存在!")
        else:
            return all_entry.get('all',"Error!Help数据缺失!")
        
    
    def nn(self,name):
        self.name = name
        self.User['User'][self.uid]['name'] = name
        self.save()
        return "修改成功"

    def info(self):
        d = {
            'name':self.name,
            'platform':self.platform,
            'id':self.id,
            'uid':self.uid
        }
        s = "用户名：{name}\n平台：{platform}\n账号：{id}\n用户ID：{uid}".format(**d)
        c = self.User.get('Link',{}).get(self.platform,{}).get(self.id,'guest')
        if c != 'guest':
            s += "\n关联用户ID：{}".format(c)
        return s

    def link(self,how,s=None):
        if how == "close":
            t = self.User.get('Link',{}).get(self.platform,{}).get(self.id,'guest')
            if t != 'guest':
                self.User["Link"][self.platform][self.id] = 'guest'
                self.save()
                return "已断开与[{}]的关联。".format(t)
            else:
                return "无可断开的关联。"
        elif how == 'to':
            uid = MID(s,self.p,self.User)
            if uid[0]:
                uid = uid[1]
            else:
                return uid[1]
            u = self.User.get('User',{}).get(uid,{})
            id = u.get('id',None)
            platform = u.get('platform',None)
            if id == self.id and platform == self.platform:
                return "Error!不能关联自己!"
            if id and platform:
                t_To = [id,platform]
                t_From = [self.id,self.platform]
                k = str(uuid.uuid4())
                Temp:dict = ReadJson(path('Token'))
                while k in Temp.keys():
                    k = str(uuid.uuid4())
                r = {
                    'to':t_To,
                    'from':t_From,
                    'time':time.time()
                }
                token = k + '#' + str(uuid.uuid4())
                r['token'] = token
                Temp[k] = r
                WriteJson(path('Token'),Temp)
                reply = "已记录申请。\n请使用要关联的账号向本骰娘发送验证指令以确定关联。\nToken：{}".format(token)
                cid = self.User.get('Link',{}).get(self.platform,{}).get(self.id,'guest')
                if cid != 'guest':
                    reply += "\n警告！您的账号正与[{}]关联！执行本操作将断开原关联！".format(cid)
                return reply
        elif how == 'accept':
            s:str
            token = s.split('#')
            Temp = ReadJson(path('Token'))
            if token[0] not in Temp.keys():
                return "Error！未知申请！"
            body = Temp[token[0]]
            t_To = body['to']
            t_From = body['from']
            if self.id != t_To[0] or self.platform != t_To[1]:
                return ''
            if body['time'] + 300 < time.time():
                del Temp[token[0]]
                WriteJson(path('Token'),Temp)
                return "Error！申请已过期！"
            if body['token'] != s:
                return "Error！Token错误！"
            uid = self.User['Guest'][t_To[1]][t_To[0]]
            self.User['Link'][t_From[1]][t_From[0]] = uid
            self.save()
            return "关联成功√"


            


        
    
    
    



def ReplyFunction(plugin_event,Proc):
    temp = re.compile(r'\*user\s?(\S+)(\s[\s\S]+)?') # 正则匹配reply指令
    string = plugin_event.data.message  #接收到的消息内容
    reply = User(plugin_event) 
    temp = temp.match(string)
    if temp:
        if temp.end() == len(string):
            head = temp.groups()[0]
            body = temp.groups()[1]
            if body:
                t = re.compile(r'\s*(\S+)').match(body)
                body = t.groups()[0]
            if head == 'help':
                plugin_event.reply(reply.help(body))
            elif head == 'info':
                plugin_event.reply(reply.info())
            elif head == 'nn':
                plugin_event.reply(reply.nn(body))
            elif head == 'link':
                plugin_event.reply(reply.link('to',body))
            elif head == 'close':
                plugin_event.reply(reply.link('close'))
            elif head == 'accept':
                r = reply.link(head,body)
                if r:
                    plugin_event.reply(r)

            