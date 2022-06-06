#模块导入区
import json  #json序列化与反序列化模块
import re  #正则表达式库，用于匹配指令
import random
import time
import OlivaDiceCore
import os
import OlivOS
'''
                        _               _  __    _
        /\             | |             | |/ /   | |
       /  \   _ __ ___ | |__   ___ _ __| ' / ___| |_ ___ _ __
      / /\ \ | '_ ` _ \| '_ \ / _ \ '__|  < / _ \ __/ _ \ '__|
     / ____ \| | | | | | |_) |  __/ |  | . \  __/ ||  __/ |
    /_/    \_\_| |_| |_|_.__/ \___|_|  |_|\_\___|\__\___|_|
    Reply文艺复兴  by Dr.Amber and NULL
    问题反馈请加QQ：1761089294
    Email：amberketer@outlook.com

'''


#事件区
class Event(object):
    def init(plugin_event, Proc):
        '''
        初始化内容
        暂时没去理解干啥用的
        未经测试
        '''
        if not os.path.exists("plugin/data/Reply"):
            os.mkdir("plugin/data/Reply")
        try:
            all: dict = ReadJson(Path('Reply'))
        except:
            data = {}
            with open("plugin/data/Reply/Reply.json",
                      "w",
                      encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
        try:
            temp = ReadJson("plugin/data/Reply/ReplyConfig.json")
        except:
            data = {
                "竖线": "|",
                "换行": "\n",
                "空格": " ",
                "client": {
                    "qq": [],
                    "dodo": []
                }
            }
            with open("plugin/data/Reply/ReplyConfig.json",
                      "w",
                      encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

    def private_message(plugin_event, Proc):
        '''
        私聊事件
        '''
        ReplyFunction(plugin_event, Proc)

    def group_message(plugin_event, Proc):
        '''
        群聊事件
        '''
        ReplyFunction(plugin_event, Proc)

    def save(plugin_event, Proc):
        '''
        保存事件
        这里经过各种测试发现毫无必要
        '''
        # WriteJson(Path('Reply'), Reply(plugin_event).all)
        pass


#函数区
def ReadJson(path: str):
    '''
    读取指定地址的json
    '''
    with open(path, "r", encoding='utf8') as f:
        return json.load(f)


def WriteJson(path: str, data: dict):
    '''
    将json写入指定地址
    '''
    with open(path, "w", encoding='utf8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def Path(p: str):
    '''
    用于返回地址
    '''
    return 'plugin/data/Reply/{}.json'.format(p)

def Check_re(re_text: str):
    '''
    检查传入字符串是不是符合正则规范的字符串
    '''
    try:
        re.compile(re_text)
        return True
    except:
        return False



#Reply类
class Reply:
    def __init__(self, plugin_event) -> None:
        '''
        初始化内容
        暂时没理解干啥用的
        未经测试
        '''
        self.p = plugin_event
        self.user: str = str(plugin_event.data.user_id)
        self.group = None  #初始化群聊数据
        if 'host_id' in plugin_event.data.__dict__:  #判断是否存在群聊或频道，若存在，写入id
            self.group = str(plugin_event.data.host_id)
        if 'group_id' in plugin_event.data.__dict__:
            self.group = str(plugin_event.data.group_id)
        self.conf: dict = ReadJson(Path('ReplyConfig'))
        self.conf["nick"] = plugin_event.data.sender["nickname"]
        self.conf["now"] = str(time.time())
        self.all: dict = ReadJson(Path('Reply'))
        self.clientlist: list = self.conf["client"][
            plugin_event.platform['platform']]

    def save(self):
        '''
        保存到指令路径里去
        路径使用path('Reply')获取
        '''
        WriteJson(Path('Reply'), self.all)

    def change(self, res):
        '''
        通过常规测试
        未作发散性测试
        '''
        data = {"reply": [], "user": [], "mode": "unity"}
        if res[1] and res[2]:
            if Check_re(res[1]) == False:   #检查关键词是否符合正则
                return "关键词不符合正则"
            self.all[res[1]] = self.all.get(res[1], data)
            if '|' in res[2]:
                self.all[res[1]]['reply'] = res[2].split('|')
            else:
                self.all[res[1]]['reply'] = [res[2]]
            self.save()
            return '设定词条成功'
        elif res[1] in self.all.keys() and res[2] == '':
            del self.all[res[1]]
            self.save()
            return '删除词条成功'
        elif res[1] not in self.all.keys():
            return '不存在该词条'

    def mode(self, res):
        '''
        这里没理解啥意思
        未经测试
        '''
        if self.all.get(res[1], None):
            if res[2]:
                if res[2] == 'unity' or res[2] == '2':
                    self.all[res[1]]['mode'] = 'unity'
                    self.save()
                elif res[2] == 'group' or res[2] == '1':
                    self.all[res[1]]['mode'] = 'group'
                    self.save()
                elif res[2] == 'private' or res[2] == '0':
                    self.all[res[1]]['mode'] = 'private'
                    self.save()
                return "修改成功"
            else:
                return "未指定模式"
        else:
            return "不存在该词条"

    #开关方法
    def client(self, res, plugin_event): 
        '''
        这里可以重构一下
        把重复的语句给合并起来
        不过我懒了
        通过常规测试和简单发散性测试
        '''
        p = Path('ReplyConfig')
        temp = ReadJson(p)
        if res[1] == 'on':
            if self.group not in self.clientlist:
                self.clientlist.append(self.group)
                temp["client"][
                    plugin_event.platform['platform']] = self.clientlist
                WriteJson(p, temp)
                return "开启reply成功"
            else:
                return "reply已经开启"
        elif res[1] == "off":
            if self.group in self.clientlist:
                self.clientlist.remove(self.group)
                temp["client"][
                    plugin_event.platform['platform']] = self.clientlist
                WriteJson(p, temp)
                return "关闭reply成功"
            else:
                return "reply已经关闭"

    def reply(self, string: str):
        '''
        这里没看懂最后一行啥意思
        只作了常规测试，未全面覆盖
        '''
        keywords_values: dict
        for key, keywords_values in self.all.items():
            temp = re.compile(r'{}'.format(key))
            temp = temp.match(string)
            if temp and keywords_values.get('reply', None):
                length = temp.end()
                if length == len(string):
                    if keywords_values['mode'] == 'group' and self.group == None:
                        return
                    elif keywords_values['mode'] == 'private' and self.group:
                        return
                    if type(keywords_values['reply']) == list:
                        temp_reply:list = keywords_values['reply']
                        for i in temp_reply:
                            temp_str = i
                            re_card = re.compile(r"[\S\s]*(\{[\$%]\S+\})[\S\s]*")
                            temp_card = re_card.match(temp_str)
                            re_draw_key = re.compile(r'\{[\$%](\S+)\}')
                            while temp_card != None:
                                temp_card = temp_card.groups()[0]
                                temp_draw_key = re_draw_key.match(temp_card).groups()[0]
                                temp_draw = OlivaDiceCore.drawCard.draw(temp_draw_key,self.p.bot_info.hash,False)
                                if type(temp_draw) is not str:
                                    temp_draw = ''
                                temp_str = temp_str.replace(temp_card,temp_draw,1)
                                temp_card = re_card.match(temp_str)
                            if temp_str != i:
                                temp_reply.remove(i)
                                temp_reply.append(temp_str)
                        for i in temp_reply:
                            i:str
                            re_weights = re.compile(r"^(::\d+::)")
                            temp_weights = re_weights.match(i)
                            if temp_weights:
                                weights:str = temp_weights.groups()[0]
                                temp_str = i.lstrip(weights)
                                weights = int(weights.strip(':'))
                                temp_reply.remove(i)
                                for j in range(weights):
                                    temp_reply.append(temp_str)
                        r: str = random.choice(temp_reply)
                    else:
                        r: str = keywords_values['reply']
                    return r.format(*temp.groups(), **self.conf)

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


def ReplyFunction(plugin_event, Proc):
    selfid = str(plugin_event.bot_info.id)
    temp = re.compile(r'\s*\*reply(level|leveldel|mode)?\s+(\S+)\s*(\S*)') # 正则匹配reply指令
    string:str = plugin_event.data.message  #接收到的消息内容
    reply = Reply(plugin_event)
    if string.startswith(OlivOS.messageAPI.PARA.at(plugin_event.base_info['self_id']).CQ()):
        string = string.replace(OlivOS.messageAPI.PARA.at(plugin_event.base_info['self_id']).CQ(),'')
    temp = temp.match(string)
    if temp:  # 匹配到了reply开头的指令后的操作
        length = temp.end()
        flag_have_change_permission = Check_admin(plugin_event) #检查是否具有修改权限
        if flag_have_change_permission == True and length == len(string):  # 如果具有修改权限
            res = temp.groups()
            if res:
                if res[0] == 'mode':
                    '''
                    这一段未经测试
                    没理解设计意图
                    '''
                    reply_text = reply.mode(res)
                elif res[1] == 'on' or res[1] == 'off':
                    '''
                    通过常规测试和简单的发散性测试
                    '''
                    reply_text = reply.client(res, plugin_event)
                else:
                    '''
                    通过常规测试和简单的发散性测试
                    '''
                    reply_text = reply.change(res)
                if reply_text:  # 用于返回reply指令处理后的操作
                    plugin_event.reply(reply_text)
    else:  # 正常返回reply内容
        res = reply.reply(string)
        group = None  # 初始化群聊数据
        if 'host_id' in plugin_event.data.__dict__:  #判断是否存在群聊或频道，若存在，写入id
            group = str(plugin_event.data.host_id)
        if 'group_id' in plugin_event.data.__dict__:
            group = str(plugin_event.data.group_id)
        if res and (group in reply.clientlist or group == None):
            plugin_event.reply(res)
