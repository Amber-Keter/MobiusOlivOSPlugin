#模块导入区
import Basic
import Level

'''
                        _               _  __    _
        /\             | |             | |/ /   | |
       /  \   _ __ ___ | |__   ___ _ __| ' / ___| |_ ___ _ __
      / /\ \ | '_ ` _ \| '_ \ / _ \ '__|  < / _ \ __/ _ \ '__|
     / ____ \| | | | | | |_) |  __/ |  | . \  __/ ||  __/ |
    /_/    \_\_| |_| |_|_.__/ \___|_|  |_|\_\___|\__\___|_|
    DW开关模块  by Dr.Amber
    问题反馈请加QQ：1761089294
    Email：amberketer@outlook.com

生成对象：Switch(plugin_event)
plugin_event        -> 插件事件

属性：
p                   -> 插件事件
platform            -> 平台标识
group               -> 群聊/频道标识
all                 -> Switch系统数据文件
conf                -> Switch系统配置文件
uid                 -> 用户唯一身份识别码
main                -> 总开关标识符
default             -> 默认开关状态
main_default        -> 总开关默认开关状态

方法：
check(name)         -> 检查开关状态，name为str型数据，代表子开关标识。只有主开关与子开关同时开时返回True
'''

class Switch:
    def __init__(self,plugin_event):
        self.p = plugin_event
        self.platform = plugin_event.platform['platform']
        self.group = None
        if 'host_id' in plugin_event.data.__dict__:            
            self.group = str(plugin_event.data.host_id)
        if 'group_id' in plugin_event.data.__dict__ :
            self.group = str(plugin_event.data.group_id)
        self.dir = 'Switch'
        tmp_dir = Basic.lib_dir
        Basic.lib_dir = self.dir
        self.all = Basic.ReadJson(Basic.path('Data'))
        self.conf = Basic.ReadJson(Basic.path('Config'))
        self.main = self.conf.get('MainSwitch','dw')
        self.default = self.conf.get('DefaultSwitch',False)
        self.main_default = self.conf.get(self.main,{}).get('default',self.default)
        Basic.lib_dir = tmp_dir
    
    def check(self,name):
        default = self.conf.get(name,{}).get('default',self.default)
        main_switch = self.all.get(self.platform,{}).get(self.group,{}).get(self.main,self.main_default)
        if self.main == name:
            name_switch = main_switch
        else:
            name_switch = self.all.get(self.platform,{}).get(self.group,{}).get(name,default)
        return (main_switch and name_switch)
