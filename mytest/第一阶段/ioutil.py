#课程名和课程ID需要用字典才生一个对应关系
# 用一个一维数组来存储 Wi，以表示选择这门课的人数
# 用二维矩阵来存储课程之间的冲突关系Cij，表示同时选两门课的人数
#分别求出L
#采用pandas库，更加方便的实现io和计算
#怎样处理输出

##文件格式，这里是已知，每一个同学的选课情况。
##如果采用老师的数据格式，是可以先转成上面的情况，再调用已知函数

import numpy as np
def process(name):
    f = open('./'+name+'.txt','r')
    # f = open('mytest/data01.txt', 'r')
    info = f.readlines()
    f.close()

    stu=dict()
    l = len(info)
    w = np.zeros(l)
    c = np.zeros((l,l))
    for i in range(0,l):
        tem = info[i].split(', ')
        for s in tem:
            w[i]+=1
            if stu.get(s):
                t = stu[s]
                for j in t:
                    c[i][j]+=1
                    c[j][i]+=1
            else:
                stu[s] = []
            stu[s].append(i)
    np.save(name+'_exam.npy',c)
    np.save(name+'_num.npy',w)

def process02(name,l):
    f = open('./' + name + '.csv', 'r')
    # f = open('mytest/data01.txt', 'r')
    info = f.readlines()
    f.close()
    exam = dict()
    exam_index = 0
    stu = dict()

    w = np.zeros(l)
    c = np.zeros((l, l))
    for t in info[1:]:
        item = t[:-1].split(",")
        if not exam.get(item[1]):
            exam[item[1]] = exam_index
            exam_index+=1
        id = exam[item[1]]
        w[id] += 1
        if stu.get(item[2]):
            li = stu.get(item[2])
            for g in li:
                c[g][id]+=1
                c[id][g]+=1
        else:
            stu[item[2]]=[]
        stu[item[2]].append(id)

    np.save(name + '_exam.npy', c)
    np.save(name + '_num.npy', w)


if __name__=='__main__':
    process('data01')
