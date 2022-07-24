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
    DW好感模块  by Dr.Amber
    问题反馈请加QQ：1761089294
    Email：amberketer@outlook.com

生成对象：Favor(uid)
uid -> 目标uid，通常由User对象的uid属性获取

属性：
all                 ->Favor系统数据文件
uid                 ->用户唯一身份识别码
favor               ->好感度，可自己修改，但须在修改完后使用save方法保存

方法：
save()              ->保存，所有方法均在最后执行，仅在自主修改favor属性时需要手动调用
change(x)           ->改变，x为int型变量，代表favor变化的值
set(x)              ->设置，x为int型变量，favor将直接被设定为x
rand(left,right)    ->随机改变，left、right为int型变量，代表favor将变化的区间，两端可取（闭区间）
'''

#类区
class Favor:
    def __init__(self,uid):
        self.dir = 'Favor'
        tmp_dir = Basic.lib_dir
        Basic.lib_dir = self.dir
        self.all = Basic.ReadJson(Basic.path('Data'))
        self.uid = uid
        self.favor = self.all.get(self.uid,{}).get('favor',0)
        Basic.lib_dir = tmp_dir


    def save(self):
        tmp_dir = Basic.lib_dir
        Basic.lib_dir = self.dir
        if self.all.get(self.uid,False) != False:
            self.all[self.uid]['favor'] = self.favor
        else:
            self.all[self.uid] = {'data':{}}
            self.all[self.uid]['favor'] = self.favor
        Basic.WriteJson(Basic.path('Data'),self.all)
        Basic.lib_dir = tmp_dir
    
    def change(self,x:int):
        if type(x) is int:
            self.favor += x
            self.save()
    
    def set(self,x:int):
        if type(x) is int:
            self.favor = x
            self.save()

    def rand(self,left:int,right:int):
        if type(left) is int and type(right) is int:
            x = random.randint(left,right)
            self.favor += x
            self.save()