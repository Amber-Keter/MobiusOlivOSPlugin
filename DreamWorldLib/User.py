#模块导入区
import re                               #正则表达式库，用于匹配指令
import Basic

'''
                        _               _  __    _
        /\             | |             | |/ /   | |
       /  \   _ __ ___ | |__   ___ _ __| ' / ___| |_ ___ _ __
      / /\ \ | '_ ` _ \| '_ \ / _ \ '__|  < / _ \ __/ _ \ '__|
     / ____ \| | | | | | |_) |  __/ |  | . \  __/ ||  __/ |
    /_/    \_\_| |_| |_|_.__/ \___|_|  |_|\_\___|\__\___|_|
    DW用户模块  by Dr.Amber
    问题反馈请加QQ：1761089294
    Email：amberketer@outlook.com

生成对象：User(plugin_event,target=None,if_find_root=True)
target      -> 目标账户（符合MID格式的四类身份识别码，用于获取初始uid）仅用于重定向用户
if_find_root-> 是否转到根节点数据，默认为是

属性：
uid         -> 用户唯一识别ID
name        -> 用户名
id          -> 用户账户ID
platform    -> 用户账户平台
child       -> 子节点uid（即自身）
root        -> 根节点uid
hasRoot     -> 是否有关联用户
all         -> 用户系统数据文件

方法：
toChild()   -> 将uid、name、id、platform属性变更为子节点用户数据
toRoot()    -> 将uid、name、id、platform属性变更为根节点用户数据（若无根，仍为子节点用户数据）
'''

#函数区
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
        User:dict = Basic.ReadJson(Basic.path('Data'))
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
    uid:str = User.get('Guest',{}).get(platform,{}).get(id,None)
    if uid:         #正常
        res:tuple = (True,uid)
        return res
    else:           #异常处理
        res:tuple = (False,"无记录用户")
        return res

#类区
class User:
    def __init__(self,plugin_event,target=None,if_find_root=True):
        self.dir = 'User'
        tmp_dir = Basic.lib_dir
        Basic.lib_dir = self.dir
        self.p = plugin_event
        self.error = None
        self.all = Basic.ReadJson(Basic.path("Data","User"))
        self.uid = MID(target,self.p,self.all)
        if self.uid[0] == False:
            self.error = self.uid[1]
        self.uid = self.uid[1]
        self.child = self.uid
        tmp_user = self.all.get("User",{}).get(self.uid,{})
        self.platform = tmp_user.get('platform',None)
        self.id = tmp_user.get('id',None)
        self.name = tmp_user.get('name',None)
        tmp_father = self.all.get('Link',{}).get(self.platform,{}).get(self.id,'guest')
        tmp_uid = self.uid
        while tmp_father != 'guest':    #寻找根节点
            tmp_uid = tmp_father
            tmp = self.all.get("User",{}).get(tmp_uid,{})
            tmp_id = tmp.get('id',None)
            tmp_platform = tmp.get('platform',None)
            tmp_father = self.all.get('Link',{}).get(tmp_platform,{}).get(tmp_id,'guest')
        if tmp_uid == self.uid:     #无根节点（即自身为根节点）
            self.root = self.uid
            self.hasRoot = False
        else:                       #有根节点
            self.root = tmp_uid
            self.hasRoot = True
        if if_find_root:
            self.uid = self.root
            tmp_user = self.all.get("User",{}).get(self.uid,{})
            self.platform = tmp_user.get('platform',None)
            self.id = tmp_user.get('id',None)
            self.name = tmp_user.get('name',None)
        Basic.lib_dir = tmp_dir

    def toRoot(self):
        self.uid = self.root
        tmp_user = self.all.get("User",{}).get(self.uid,{})
        self.platform = tmp_user.get('platform',None)
        self.id = tmp_user.get('id',None)
        self.name = tmp_user.get('name',None)
        return self
    
    def toChild(self):
        self.uid = self.child
        tmp_user = self.all.get("User",{}).get(self.uid,{})
        self.platform = tmp_user.get('platform',None)
        self.id = tmp_user.get('id',None)
        self.name = tmp_user.get('name',None)
        return self