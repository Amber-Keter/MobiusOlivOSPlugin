#模块导入区
import json                             #json序列化与反序列化模块
import re                               #正则表达式库，用于匹配指令
import random
import os
import uuid
import OlivOS
import OlivaDiceCore
import time

#事件区
class Event(object):
    def init(plugin_event, Proc):
        if not os.path.exists("plugin/data/DreamWorld"):
            os.mkdir("plugin/data/DreamWorld")
        if not os.path.exists("plugin/data/DreamWorld/Favor"):
            os.mkdir("plugin/data/DreamWorld/Favor")
        try:
            ReadJson(path('Data','User'))
        except:
            print("Error!未找到用户数据")
        try:
            ReadJson(path('Data'))
        except:
            data={}
            with open("plugin/data/DreamWorld/Favor/Data.json","w",encoding="utf-8") as file:
                json.dump(data, file,indent=4,ensure_ascii=False)
        try:
            ReadJson(path('Favor'))
        except:
            data={}
            with open("plugin/data/DreamWorld/Favor/Favor.json","w",encoding="utf-8") as file:
                json.dump(data, file,indent=4,ensure_ascii=False)
        try:
            ReadJson(path('Config'))
        except:
            data={}
            with open("plugin/data/DreamWorld/Favor/Config.json","w",encoding="utf-8") as file:
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
        json.dump(data,f)

#地址函数
def path(p:str,dir = 'Favor'):
    return 'plugin/data/DreamWorld/{}/{}.json'.format(dir,p)

#词条抽取函数
def Rand(s):
    if s is list:
        t = []
        for i in s:
            if i is dict:
                权重 = i.get('weights',1)
                for j in range(权重):
                    t.append(i)
            else:
                t.append(i)
        return random.choice(t)
    else:
        return s          

#用户UID获取函数
def GetUser(uid):
    user:dict = ReadJson(path('Data','User'))
    if uid in user.get('User',{}).keys():
        return user['User'][uid]

#用户类
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
        self.User:dict = ReadJson(path('Data','User'))
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
        WriteJson(path('Data','User'),self.User)   #写入到指定文件里去

#主体类
class Favor:
    def __init__(self,plugin_event) -> None:
        self.p = plugin_event
        self.User = User(plugin_event)
        if self.User.User.get('Link',{}).get(self.User.platform,{}).get(self.User.id,'guest') != 'guest':
            self.uid = self.User.User.get('Link',{}).get(self.User.platform,{}).get(self.User.id,'guest')
        else:
            self.uid = self.User.uid
        self.Favor:dict = ReadJson(path('Data'))
        self.conf = ReadJson(path('Config'))
        self.conf["nick"] = plugin_event.data.sender["nickname"]
        self.conf["now"] = str(time.time())
        self.conf['selfid'] = plugin_event.bot_info.id



    def save(self):
        WriteJson(path('Data'),self.Favor)   #写入到指定文件里去

    #开关函数
    def switch(self,change,group = None,platform = None):
        if group == None:
            group = self.User.group
        if platform == None:
            platform = self.User.platform
        platform = str(platform)
        group = str(group)
        if self.Favor.get(platform,None) == None:
            self.Favor[platform] = {}
        self.Favor[platform][group] = change
        self.save()
        if change == 'on':
            r = '开启'
        else:
            r = '关闭'
        res = "已{}在{}-{}的好感度系统。".format(r,platform,group)
        return res
    
    def reply(self,string):
        if self.User.group and self.Favor.get(self.User.platform,{}).get(self.User.group,'off') == 'off':
            return
        reply_file:dict = ReadJson(path('Favor'))
        for k,v in reply_file.items():
            re_temp = re.compile(k).match(string)
            if re_temp:
                if re_temp.end() != len(string):
                    continue
                if v is not dict:
                    return Rand(v)
                v:dict
                mode = v.get('mode','unity')
                if mode == 'group' and self.User.group == None:
                    return
                if mode == 'private' and self.User.group:
                    return
                user = GetUser(self.uid)
                max_default = v.get('max',None)
                cd_default = v.get('cd',None)
                r = v.get('return',None)
                data = self.Favor.get(self.uid,{}).get('data',{}).get(k,{})
                last_triggered = data.get('last_triggered',0)
                today_frequency = data.get('today_frequency',0)
                now = time.time()
                difference = now - last_triggered
                if r is not dict:
                    res = Rand(r)
                else:
                    r:dict
                    type_list = ['special','level','favor','common']
                    key_exist = False
                    for i in type_list:
                        if i in r.keys():
                            key_exist = True
                    if key_exist == False:
                        res = r
                    else:
                        r_special = r.get('special',None)
                        r_level = r.get('level',None)
                        r_favor = r.get('favor',None)
                        r_common = r.get('common',None)
                        favor = self.Favor.get(self.uid,{}).get('favor',0)
                        try:
                            level_data:dict = ReadJson(path('Data','Level'))
                            level_config:dict = ReadJson(path('Config','Level'))
                            level_default = level_config.get('default',1)
                            level = level_data.get(self.uid,level_default)
                        except:
                            level = 1
                        if r_common:
                            if r_common is list:
                                res = Rand(r_common)
                            else:
                                res = r_common
                            r_class = 'common'
                        if r_favor:
                            if r_favor is not list:
                                temp_list = []
                                temp_list.append(r_favor)
                                temp_list,r_favor = r_favor,temp_list
                            for i in r_favor:
                                i:dict
                                interval = i.get('interval',[None,None])
                                if interval is int and favor == interval:
                                    res = i.get('reply',None)
                                    r_class = 'favor'
                                    break
                                elif interval is list:
                                    left = True
                                    right = True
                                    if interval[0] and favor < interval[0]:
                                        left = False
                                    if interval[1] and favor > interval[1]:
                                        right = False
                                    if left and right:
                                        res = i.get('reply',None)
                                        t_class = 'favor'
                                        break
                        if r_level:
                            if r_level is not list:
                                temp_list = []
                                temp_list.append(r_level)
                                temp_list,r_level = r_level,temp_list
                            for i in r_level:
                                i:dict
                                interval = i.get('interval',[None,None])
                                if interval is int and level == interval:
                                    res = i.get('reply',None)
                                    r_class = 'level'
                                    break
                                elif interval is list:
                                    left = True
                                    right = True
                                    if interval[0] and level < interval[0]:
                                        left = False
                                    if interval[1] and level > interval[1]:
                                        right = False
                                    if left and right:
                                        res = i.get('reply',None)
                                        t_class = 'level'
                                        break
                        if r_special:
                            if r_special is not list:
                                temp_list = []
                                temp_list.append(r_special)
                                temp_list,r_special = r_special,temp_list
                            for i in r_special:
                                uid_list = i.get('uid',[])
                                if uid_list is str and self.uid == uid_list:
                                    res = i.get('reply',None)
                                    r_class = 'special'
                                    break
                                elif uid_list is list:
                                    if self.uid in uid_list:
                                        res = i.get('reply',None)
                                        r_class = 'special'
                                        break
                if res is dict:
                    cd = res.get('cd',cd_default)
                    max = res.get('max',max_default)
                    change = res.get('change',0)
                    success = res.get('success',True)
                else:
                    cd = cd_default
                    max = max_default
                    change = 0
                    success = True    
                all_interval = ['special','level','favor','common']    
                if cd is list:
                    cd:list
                    num = cd.count()
                    if num == 2:
                        cd_reply = cd[1]
                        cd_interval = all_interval
                    elif num == 3:
                        cd_reply = cd[1]
                        cd_interval = cd[2]
                    else:
                        cd_reply = None
                        cd_interval = all_interval
                    cd = cd[0]
                elif cd is int:
                    cd_reply = None
                    cd_interval = all_interval
                elif cd is dict:
                    cd = cd.get(r_class,[0,None])
                    if cd is list:
                        cd:list
                        num = cd.count()
                        if num == 2:
                            cd_reply = cd[1]
                            cd_interval = r_class
                        elif num == 3:
                            cd_reply = cd[1]
                            cd_interval = cd[2]
                        else:
                            cd_reply = None
                            cd_interval = r_class
                        cd = cd[0]
                    elif cd is int:
                        cd_reply = None
                        cd_interval = r_class
                if max is list:
                    max:list
                    num = max.count()
                    if num == 2:
                        max_reply = max[1]
                        max_interval = all_interval
                    elif num == 3:
                        max_reply = max[1]
                        max_interval = max[2]
                    else:
                        max_reply = None
                        max_interval = all_interval
                    max = max[0]
                elif max is int:
                    max_reply = None
                    max_interval = all_interval
                elif max is dict:
                    max = max.get(r_class,[0,None])
                    if max is list:
                        max:list
                        num = max.count()
                        if num == 2:
                            max_reply = max[1]
                            max_interval = r_class
                        elif num == 3:
                            max_reply = max[1]
                            max_interval = max[2]
                        else:
                            max_reply = None
                            max_interval = r_class
                        max = max[0]
                    elif max is int:
                        max_reply = None
                        max_interval = r_class
                left_cd = cd - difference
                if cd > 0:
                    if r_class == cd_interval or r_class in cd_interval:
                        if left_cd > 0:
                            if cd_reply is str:
                                cd_reply:str
                                cd_reply = cd_reply.format(时间差值 = left_cd,**self.conf)
                            return cd_reply
                now_date = time.strftime("%Y-%m-%d", time.time())
                last_date = time.strftime("%Y-%m-%d", last_triggered)
                if max > 0:
                    if r_class == max_interval or r_class in max_interval:
                        if now_date == last_date:
                            if today_frequency >= max:
                                if max_reply is str:
                                    max_reply:str
                                    max_reply = cd_reply.format(一日上限 = max,**self.conf)
                                return max_reply
                        else:
                            today_frequency = 0
                res = Rand(res.get('reply',None))
                if res is dict:
                    res:dict
                    change = res.get("change",change)
                    success = res.get('success',success)
                    res = Rand(res.get('str',None))
                if self.Favor.get(self.uid,False) == False:
                    self.Favor[self.uid] = {'favor':0,'data':{}}
                if success:
                    today_frequency += 1
                    self.Favor[self.uid]['data'][k] = {'last_triggered':time.time(),'today_frequency':today_frequency}
                if change is list:
                    change_max = 10000
                    if change[0] == None:
                        change[0] = -change_max
                    if change[1] == None:
                        change[1] = change_max
                    change = random.randint(change[0],change[1])
                if change != 0:
                    change_reply = self.conf.get('FavorChange',None)
                    self.Favor[self.uid]['favor'] += change
                    change_abs = abs(change)
                    if change_reply is dict:
                        change_reply:dict
                        if change > 0:
                            change_reply = change_reply.get('up',None)
                        else:
                            change_reply = change_reply.get('down',None)
                    change_reply:str
                    change_reply = '\n' + change_reply.format(change=change,change_abs=change_abs,now_favor=self.Favor[self.uid]['favor'],favor=favor,**self.conf)
                res:str
                res = res.format(*re_temp.groups(),**self.conf)
                self.save()
                if change_reply:
                    res += change_reply
                return res


def Check_admin(plugin_event):
    '''
    检查权限
    是不是master、群主、管理
    '''
    if 'role' in plugin_event.data.sender:
        if plugin_event.data.sender['role'] in ['owner', 'admin']:
            flag_is_from_group_admin = True
    flag_is_from_master = OlivaDiceCore.ordinaryInviteManager.isInMasterList(
            plugin_event.bot_info.hash,
            OlivaDiceCore.userConfig.getUserHash(
                plugin_event.data.user_id, 'user',
                plugin_event.platform['platform']))  #检测是不是master
    return flag_is_from_master or flag_is_from_group_admin

def ReplyFunction(plugin_event,Proc):
    string = plugin_event.data.message  #接收到的消息内容
    selfid = str(plugin_event.bot_info.id)
    temp_re = r'\s*\*favor\s*(on|off)'
    if string.startswith(OlivOS.messageAPI.PARA.at(plugin_event.base_info['self_id']).CQ()):
        string = string.replace(OlivOS.messageAPI.PARA.at(plugin_event.base_info['self_id']).CQ(),'')
    temp = re.compile(temp_re) # 正则匹配reply指令
    reply = Favor(plugin_event)
    temp = temp.match(string)
    if temp:  # 匹配到了reply开头的指令后的操作
        length = temp.end()
        flag_have_change_permission = Check_admin(plugin_event) #检查是否具有修改权限
        if flag_have_change_permission == True and length == len(string):  # 如果具有修改权限
            res = temp.groups()
            plugin_event.reply('[cq:at,id=1761089294]')
            if res:               
                if res[1] == 'on' or res[1] == 'off':
                    reply_text = reply.switch(res[1])
                if reply_text:  # 用于返回reply指令处理后的操作
                    plugin_event.reply(reply_text)
    else:  # 正常返回reply内容
        res = reply.reply(string)
        if res:
            plugin_event.reply(res)