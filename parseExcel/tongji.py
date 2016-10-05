#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xlrd

#打开Excel
data = xlrd.open_workbook('1.xls')
#获取第一个sheet表
table = data.sheets()[0]
#获取表格的总行数，列数
nrows = table.nrows
ncols = table.ncols
#构建方子和对应的所有药物与剂量的dict
d = dict()
for i in range(nrows):
    fang = table.cell(i,2).value.strip()
    d[fang] = {}
    for j in range(ncols):
        if j >= 5 and j % 2 == 0:
            yao = table.cell(i,j - 1).value.strip()
            if not yao:
                continue
            liang = table.cell(i,j).value
            d[fang][yao]  = liang
#生成药名为key和方名、剂量为值的dict
yaoliang = dict()
for fang,yao in d.items():
    for yao,liang in yao.items():
        yaoliang[yao] = dict()

for fang,yao in d.items():
    for yao,liang in yao.items():
        yaoliang[yao][fang] = liang

# print(yaoliang['麻黄'])
with open("统计.txt",'w',encoding = 'utf-8') as f:
    for yao,fangliang in yaoliang.items():
        liangs = list(fangliang.values())
        # print("pre----------------",liangs)
        #剂量只保留float的，过滤掉中文剂量，否则无法取最大值，最小值。
        liangs = list(filter(lambda x: isinstance(x,float),liangs))
        # print("pro----------------",liangs)
        for fang in fangliang.keys():
            #过滤掉剂量为空的（剂量全为中文的）
            if not liangs:
                continue
            if fangliang[fang] == max(liangs):
                f.write("药名：" + yao + "\t方名：" + fang + "\t最大剂量：" + str(fangliang[fang]) + "\n")
            if fangliang[fang] == min(liangs):
                f.write("药名：" + yao + "\t方名：" + fang + "\t最小剂量：" + str(fangliang[fang]) + "\n")
