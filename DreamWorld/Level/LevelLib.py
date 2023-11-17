#模块导入区
from . import Basic

'''
                        _               _  __    _
        /\             | |             | |/ /   | |
       /  \   _ __ ___ | |__   ___ _ __| ' / ___| |_ ___ _ __
      / /\ \ | '_ ` _ \| '_ \ / _ \ '__|  < / _ \ __/ _ \ '__|
     / ____ \| | | | | | |_) |  __/ |  | . \  __/ ||  __/ |
    /_/    \_\_| |_| |_|_.__/ \___|_|  |_|\_\___|\__\___|_|
    DW权限模块  by Dr.Amber
    问题反馈请加QQ：1761089294
    Email：amberketer@outlook.com

依赖模块：OlivaDiceCore

生成对象：Level(uid)
uid -> 目标uid，通常由User对象的uid属性获取

属性：
all                 ->Level系统数据文件
conf                ->Level系统配置文件
uid                 ->用户唯一身份识别码
default             ->权限默认值
level               ->权限等级，可自己修改，但须在修改完后使用save方法保存

方法：
save()                      ->保存，所有方法均在最后执行，仅在自主修改level属性时需要手动调用
change(x)                   ->改变，x为int型变量，代表level变化的值
set(x)                      ->设置，x为int型变量，level将直接被设定为x
check(target)               ->判断权限，target为int型变量时，判断level是否等于target，为str型变量时，寻找'List'词条下的[target]序列，判断level是否为该序列成员。
checkAdmin(plugin_event)    ->判断是否为Admin
checkMaster(plugin_event)   ->判断是否为Master
'''

try:            #OlivaDiceCore模块导入与权限判断函数声明
    import OlivaDiceCore
    def CheckMaster(plugin_event):
        flag_is_from_master = OlivaDiceCore.ordinaryInviteManager.isInMasterList(
                plugin_event.bot_info.hash,
                OlivaDiceCore.userConfig.getUserHash(
                    plugin_event.data.user_id, 'user',
                    plugin_event.platform['platform']))  #检测是不是master
        return flag_is_from_master
except:         #OlivaDiceCore模块缺失处理
    def CheckMaster(plugin_event):
        return False

#类区
class Level:
    def __init__(self,uid):
        self.dir = 'Level'
        tmp_dir = Basic.lib_dir
        Basic.lib_dir = self.dir
        self.all = Basic.ReadJson(Basic.path('Data','Level'))
        self.conf = Basic.ReadJson(Basic.path('Config','Level'))
        self.uid = uid
        self.default = self.conf.get('Default',0)
        self.level = self.all.get(self.uid,self.default)
        Basic.lib_dir = tmp_dir


    def save(self):
        tmp_dir = Basic.lib_dir
        Basic.lib_dir = self.dir
        self.all[self.uid] = self.level
        Basic.WriteJson(Basic.path('Data','Level'),self.all)
        Basic.lib_dir = tmp_dir
    
    def change(self,x:int):
        if type(x) is int:
            self.level += x
            self.save()
    
    def set(self,x:int):
        if type(x) is int:
            self.level = x
            self.save()

    def check(self,target:int or str):
        if type(target) is int:
            if target == self.level:
                return True
            else:
                return False
        elif type(target) is str:
            level_list = self.conf.get('List',{}).get(target,[])
            if self.level in level_list:
                return True
            else:
                return False
    
    def checkAdmin(self,plugin_event):
        dw_admin = self.check('Admin')
        ovo_master = CheckMaster(plugin_event)
        dw_master = self.check('Master')
        return dw_admin or ovo_master or dw_master
    
    def checkMaster(self,plugin_event):
        ovo_master = CheckMaster(plugin_event)
        dw_master = self.check('Master')
        return ovo_master or dw_master