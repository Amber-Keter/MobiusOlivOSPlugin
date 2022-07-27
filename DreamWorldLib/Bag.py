#模块导入区
import Basic
import random

'''
                        _               _  __    _
        /\             | |             | |/ /   | |
       /  \   _ __ ___ | |__   ___ _ __| ' / ___| |_ ___ _ __
      / /\ \ | '_ ` _ \| '_ \ / _ \ '__|  < / _ \ __/ _ \ '__|
     / ____ \| | | | | | |_) |  __/ |  | . \  __/ ||  __/ |
    /_/    \_\_| |_| |_|_.__/ \___|_|  |_|\_\___|\__\___|_|
    DW背包模块  by Dr.Amber
    问题反馈请加QQ：1761089294
    Email：amberketer@outlook.com

生成对象：Bag(target,footer)
target              -> 目标数据文件名标识
footer              -> 目标数据文件夹标识

属性：
path                -> 目标数据文件地址
all                 -> Bag系统数据文件
conf                -> Bag系统配置文件
mode                -> 数据存储模式
default             -> 默认数据

方法：
save()              -> 保存，所有方法均在最后执行，仅在自主修改all属性时需要手动调用
get(key,default)    -> 获取key键的值，缺失时返回default
change(key,value)   -> 改变key键的值，需为数字型变量
set(key,value)      -> 设置key键的值，类型不限
count()             -> 获取所有value的总值
rand(num)           -> 随机获取num个key，key池中key的数量由value决定
randGet(num)        -> 随机获取num个[key,value]序列
'''

class Bag:
    def __init__(self,target,footer = 'default'):
        self.dir = 'Bag'
        tmp_dir = Basic.lib_dir
        Basic.lib_dir = self.dir
        if (type(footer) is str) and (footer != ''):
            target = footer + '/' + target
        self.path = Basic.path(target)
        self.all = Basic.ReadJson(self.path)
        self.conf = Basic.ReadJson(Basic.path('Config'))
        if (type(footer) is not str) or (footer == ''):
            self.mode = 4
            self.default = None
        else:
            tmp = self.conf.get(footer,{})
            default_mode = self.conf.get('DefaultMode',0)
            self.mode = tmp.get('mode',default_mode)
            if (self.mode == 0) or (self.mode == 1):
                default = 0
            elif (self.mode == 0) or (self.mode == 1):
                default = 0.0
            else:
                default = None
            self.default = tmp.get('default',default)
        Basic.lib_dir = tmp_dir

    def save(self):
        tmp_dir = Basic.lib_dir
        Basic.lib_dir = self.dir
        Basic.WriteJson(self.path,self.all)
        Basic.lib_dir = tmp_dir

    def get(self,key,default = None):
        if default == None:
            default = self.default
        res = self.all.get(key,default)
        return res

    def count(self):
        c = 0
        if (self.mode == 0) or (self.mode == 2):
            for i in self.all.values():
                c += i
            return c

    def change(self,key,value):
        if (self.mode == 0) or (self.mode == 1):
            if type(value) is not int:
                return
        elif (self.mode == 2) or (self.mode == 3):
            if type(value) is not float:
                return
        else:
            return
        tmp = self.get(key,self.default) + value
        if (self.mode == 0) or (self.mode == 2):
            if tmp < 0:
                if self.mode == 0:
                    tmp = 0
                elif self.mode == 2:
                    tmp = 0.0
        self.all[key] = tmp
        self.save()
    
    def set(self,key,value):
        if (self.mode == 0) or (self.mode == 1):
            if type(value) is not int:
                return
        elif (self.mode == 2) or (self.mode == 3):
            if type(value) is not float:
                return
        if (self.mode == 0) or (self.mode == 2):
            if value < 0:
                if self.mode == 0:
                    value = 0
                elif self.mode == 2:
                    value = 0.0
        self.all[key] = value
        self.save()
    
    def rand(self,num = 1):
        if self.mode == 0:
            count = self.count()
            if count >= num:
                tmp_list = []
                tmp_dict = self.all.copy()
                for key,value in tmp_dict.items():
                    while value > 0:
                        tmp_list.append(key)
                        value -= 1
                res = []
                while num > 0:
                    tmp_rand = random.choice(tmp_list)
                    res.append(tmp_rand)
                    tmp_list.remove(tmp_rand)
                    num -= 1
                if len(res) == 1:
                    res = res[0]
                return res
    
    def randGet(self,num = 1):
        tmp_list = []
        tmp_dict = self.all.copy()
        count = 0
        for key,value in tmp_dict.items():
            tmp_list.append([key,value])
            count += 1
        res = []
        if count >= num:
            while num > 0:
                tmp_rand = random.choice(tmp_list)
                res.append(tmp_rand)
                tmp_list.remove(tmp_rand)
                num -= 1
            if len(res) == 1:
                res = res[0]
            return res