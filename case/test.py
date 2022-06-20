# coding=utf-8

"""
@author: Lyle.Hong
@date: 2022/6/9 10:15
"""
import time

"""
一、装饰器练习题
1、现有有如下功能函数：
    def work2(a,b):
        res = a+b
        print('a+b的结果为:',res)
    # 调用函数当参数类型不能进行相加时，work执行会报错！如：work2(10,‘a’)
    # 需求：在不更改函数代码的前提现，实现调用work函数传入不同类型的参数是函数不报错，
    输出结果：您传入的参数类型不一样，无法正常执行

2、根据下面需求实现rerun装饰器。
    @rerun
    def work(a,b):
        assert a==b
    需求
    被装饰的函数work执行出现AssertionError，则重新再执行一次该函数，
    如果还是执行出现AssertionError，则抛出异常


3、实现一个记录函数调用信息的装饰器log，
    @log
    def work(a,b):
        return a+b
  需求：每一次调用函数，会将执行的函数名，参数，执行时间 输出到控制台


4、(面试笔试题)请实现装饰器count_time的功能

    @count_time(n=2)
    def work():
        time.sleep(1)

    需求：count_time接收一个int类型的参数n，可以用来装饰任何的函数，
    如果函数运行的时间大于参数n，则打印出函数名和函数的运行时间。



二、递归练习题(选做题)
1、 一个球从100米高度自由落下，每次落地后反跳回原高度的一半；再落下，求它在第10次落地时，共经过多少米？(要求递归函数实现)

2、题目：猴子吃桃问题：
猴子第一天摘下若干个桃子，当即吃了一半，还不过瘾，又再吃了一个。第二天早上又将剩下的桃子吃掉一半，再吃了一个。
以后每天早上都吃了前一天剩下的一半  在加一个。
到第10天早上想再吃时，见只剩下一个桃子了。
请通过一段通过代码来计算第一天摘了多少个桃子？（递归实现）

3、题目：小明买了一对刚出生的兔子，兔子从出生后第3个月开始，每个月都生一对兔子，
  每对兔子出生后第三个月开始每个月都会生一对兔子，
  假如兔子都不死，问100个月后小明的兔子为多少对？
  （思路提示：重点在分析出兔子增长的规律，通过递归实现）

"""
print(time.time())
print(time.strftime("%Y-%m-%d",time.localtime()))