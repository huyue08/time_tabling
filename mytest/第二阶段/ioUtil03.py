import numpy as np
import matplotlib.pyplot as plt

class result:
    solution = None
    people = []
    iClass = []
    stu_id = []
    people_class=[]
    name = ''
    adj = []


    #获得一位同学的考试时间安排
    def get_one_stu(self, id):
        return 0

    def out(self):
        return 9

    #获得最忙的几位同学的考试时间安排
    def get_busiest_stu(self):

        return 0

    #获得这门考试可以调整到的时间
    def available(self, id):
        all = [i for i in range(self.times_num)]
        for i in self.adj[id]:
            all.remove(self.solution[i])
        print("exam "+str(id)+"可调整到时间段:")
        print(all)

    # 查看某一时间段的安排的考试
    def one_day(self, t):
        day = t/4+1
        when = t%4
        print("第"+str(day)+"天，第"+str(when)+"时间段的考试有")
        for i in self.solution_re[t]:
            print("id: "+str(i)+" name: "+self.exam_name[i]+" people: "+str(self.people_exam[i]))

    #将考试(id) 从past调整到now时间段
    def change(self, id,past, now):
        self.solution[id] = now
        self.solution_re[past].remove(id)
        self.solution_re[now].append(now)
        self.people_time[past] -= self.people_exam[id]
        self.people_time[past] += self.people_exam[id]
        return 9

    def __init__(self, name,times_num):
        self.name = name
        self.solution = np.load(name+'_solution.npy', allow_pickle=True).item()
        self.stu_exam = np.load(name+'_stu.npy',allow_pickle=True).item()
        self.exam_class = np.load(name+'_exam_class.npy',allow_pickle=True).item()
        self.exam_index = np.load(name+"exam_index.npy",allow_pickle=True).item()
        self.people_exam = np.load(name+'_num.npy')
        self.people_time = np.load(name+"_people_time.npy")
        self.exam_num = len(self.solution.keys())
        self.times_num = times_num
        self.solution_re = dict(zip([i for i in range(self.times_num)], [[] for i in range(self.times_num)]))
        for i in self.solution.keys():
            self.solution_re[self.solution[i]].append(i)
        self.exam_name = list(self.exam_index.keys())
        self.cij = np.load(name + "_cij.npy")
        for i in range(self.exam_num):
            self.adj[i] = (np.where(self.cij[i] > 0))[0].tolist()
