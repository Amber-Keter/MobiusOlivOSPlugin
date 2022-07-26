#模块导入区
import random
import Basic

'''
                        _               _  __    _
        /\             | |             | |/ /   | |
       /  \   _ __ ___ | |__   ___ _ __| ' / ___| |_ ___ _ __
      / /\ \ | '_ ` _ \| '_ \ / _ \ '__|  < / _ \ __/ _ \ '__|
     / ____ \| | | | | | |_) |  __/ |  | . \  __/ ||  __/ |
    /_/    \_\_| |_| |_|_.__/ \___|_|  |_|\_\___|\__\___|_|
    DW点数模块  by Dr.Amber
    问题反馈请加QQ：1761089294
    Email：amberketer@outlook.com

生成对象：Point(uid，name)
uid     -> 目标uid，通常由User对象的uid属性获取
name    -> 数据文件路径标识

属性：
all                 -> Point系统数据文件
conf                -> Point系统配置文件
uid                 -> 用户唯一身份识别码
point               -> 点数，可自己修改，但须在修改完后使用save方法保存
name                -> Point子数据路径标识

方法：
save()              -> 保存，所有方法均在最后执行，仅在自主修改point属性时需要手动调用
change(x)           -> 改变，x为int型变量，代表point变化的值
set(x)              -> 设置，x为int型变量，point将直接被设定为x
rand(left,right)    -> 随机改变，left、right为int型变量，代表point将变化的区间，两端可取（闭区间）
redirect(name)      -> 重定向数据文件，用于更换数据文件指针
checkClass(i)       -> 检测入参是否符合设定要求（内部函数）
checkPoint()        -> 检测操作后的point是否符合设定要求（内部函数）
'''

#类区
class Point:
    def __init__(self,uid,name = None):
        self.dir = 'Point'
        tmp_dir = Basic.lib_dir
        Basic.lib_dir = self.dir
        self.conf = Basic.ReadJson(Basic.path('Config'))
        self.uid = uid
        if name:
            self.all = Basic.ReadJson(Basic.path('Data-{}'.format(name)))
            self.name = name
        else:
            default = self.conf.get('DefaultPoint','point')
            self.all = Basic.ReadJson(Basic.path('Data-{}'.format(default)))
            self.name = default
        self.point = self.all.get(self.uid,0)
        Basic.lib_dir = tmp_dir


    def save(self):
        tmp_dir = Basic.lib_dir
        Basic.lib_dir = self.dir
        self.all[self.uid] = self.point
        Basic.WriteJson(Basic.path('Data-{}'.format(self.name)),self.all)
        Basic.lib_dir = tmp_dir
    
    def change(self,x:int):
        if self.checkClass(x):
            self.point += x
            self.checkPoint(self.point)
            self.save()
    
    def set(self,x:int):
        if self.checkClass(x):
            self.point = x
            self.checkPoint(self.point)
            self.save()

    def rand(self,left:int,right:int):
        if type(left) is int and type(right) is int:
            x = random.randint(left,right)
            self.point += x
            self.checkPoint(self.point)
            self.save()
    
    def redirect(self,name):
        self.save()
        if type(name) is str:
            self.all = Basic.ReadJson(Basic.path('Data-{}'.format(name)))
            self.point = self.all.get(self.uid,0)
    
    def checkClass(self,i):
        default_rule = self.conf.get('DefaultRule',0)
        rule = self.conf.get('Namespace',{}).get(self.name,{}).get('rule',default_rule)
        if rule == 0 or rule == 1:
            return (type(i) is int)
        elif rule == 2 or rule == 3:
            return (type(i) is float)
    
    def checkPoint(self):
        default_rule = self.conf.get('DefaultRule',0)
        rule = self.conf.get('Namespace',{}).get(self.name,{}).get('rule',default_rule)
        if rule == 0 or rule == 2:
            if self.point < 0:
                if rule == 0:
                    self.point = 0
                else:
                    self.point = 0.0