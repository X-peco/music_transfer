#作为父类
class Identify:
    def __init__(self,name,age):
        self.name=name
        self.age=age
    #年龄增长
    def age_chage(self,num):
        if (num>0):
            self.age+=num
            print(f"now {self.name} is {self.age} year old")
        else:
            print("what the fuck!!")
    #自定义年龄
    def updata(self,new):
        self.age=new
        print(f"now {self.name} is {self.age} year old")

first=Identify("xzh",18)
#作为类属性扩展
class Toy():
    def __init__(self):
        self.battery=100
    #充电
    def battery_charge(self,add):
        if (add>0 and self.battery+add<=100):
            self.battery+=add
        else:
            print("what's wrong with you?!")

#喜好
class Habbit:
    def __init__(self,lib,name):#########注意到不同类之间的处理方式
        self.lib=lib
        self.name=name
    #展示内容
    def show_list(self):
        for x in self.lib:
            print(x)
    #内容查找     
    def check_favor(self,check):
        if(check in self.lib):
            print(f"{check} is {self.name} favourite")
        else:
            print(f"{check} is not found!")

#汇总      
library=['badminton','sleeping','wondering']#初始清单
class More_infor(Identify):
    def __init__(self,name,age,address,a):
        super().__init__(name,age)
        self.address=address
        self.toy=Toy()###################定义喜好的类属性
        self.habbit=Habbit(a,name)#######添加喜好
    #添加性别
    def gender(self,gender):
        self.gender=gender 
        return self.gender
    #查询里程
    def kio(self):
        far=self.toy.battery*1.5
        return far
    
second=More_infor("hcy",19,'china',library)
second.updata(23)
print(second.gender("female"))
print(second.toy.battery)
print(second.kio())
second.habbit.show_list()
second.habbit.check_favor('badminton')