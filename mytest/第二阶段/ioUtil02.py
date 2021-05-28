import numpy as np
def process(name):
    f = open('./' + name + '.csv', 'r')
    info = f.readlines()[1:]
    f.close()

    exams = set([i.split(",")[1] for i in info])
    l = len(exams)
    exam = dict()
    exam_index = 0
    stu = dict()
    exam_class = dict()

    w = np.zeros(l)
    c = np.zeros((l, l))
    for t in info:
        item = t[:-1].split(",")
        if exam.get(item[1],-1) == -1:
            exam[item[1]] = exam_index
            exam_index+=1
        if exam_class.get(item[1],-1)==-1:
            exam_class[item[1]] = []
        if item[0] not in exam_class[item[1]]:
            exam_class[item[1]].append(item[0])
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

    np.save(name + '_cij.npy', c)
    np.save(name + '_num.npy', w)
    np.save(name+'_stu.npy',stu)
    np.save(name+"_exam_index",exam)
    np.save(name+"_exam_class",exam_class)


if __name__=='__main__':
    process('21data-group')
