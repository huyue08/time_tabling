import numpy as np
def process(name):
    name = 'data/'+name
    f = open(name + '.csv', 'r')
    info = f.readlines()[1:]
    f.close()

    exams = set([i.split(",")[1] for i in info])
    l = len(exams)
    exam = dict()
    stu = dict()
    stu_index = 0
    exam_index = 0
    stu_exam = dict()
    exam_class = dict()

    w = np.zeros(l)
    c = np.zeros((l, l))
    for t in info:
        item = t[:-1].split(",")
        if exam.get(item[1],-1) == -1:
            exam[item[1]] = exam_index
            exam_index+=1
        if stu.get(item[2],-1) == -1:
            stu[item[2]] = stu_index
            stu_index+=1


        eid = exam[item[1]]
        sid = stu[item[2]]
        w[eid] += 1
        if exam_class.get(eid,-1)==-1:
            exam_class[eid] = []
        if item[0] not in exam_class[eid]:
            exam_class[eid].append(item[0])

        if stu_exam.get(sid):
            li = stu_exam.get(sid)
            for g in li:
                c[g][eid]+=1
                c[eid][g]+=1
        else:
            stu_exam[sid]=[]
        stu_exam[sid].append(eid)

    np.save(name + '_cij.npy', c)
    np.save(name + '_num.npy', w)
    np.save(name+'_stu_exam.npy',stu_exam)
    np.save(name+"_stu_index",stu)
    np.save(name+ "_exam_index",exam)
    np.save(name+ "_exam_class",exam_class)


if __name__=='__main__':
    process('example')
