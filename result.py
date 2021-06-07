import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class result:
    solution = None
    people = []
    iClass = []
    stu_id = []
    name = ''
    stu_exam = None
    exam_class = None
    exam_name = []
    stu_name = []
    exam_num = 0
    times_num = 0
    solution_re = None
    cij = None
    adj = dict()
    exam_people = None
    time_people = None

    #获得一位同学的考试时间安排
    def get_one_stu(self, id):
        exam_list = self.stu_exam[id]
        print("id: "+str(id)+" stuID: "+ self.stu_name[id])
        for e in exam_list:
            print("exam_id:"+str(e)+" "+self.exam_name[e]+" : "+str(self.solution[e]))


    #可视化每个时间段对应考试数，学生人数，考试班级数以获得对整个方案的大致了解
    def outline(self):
        index = np.arange(self.times_num)
        plt.subplot(311)
        p2 = plt.bar(index, height=self.exam_time,color='orange')
        p2 = plt.ylabel("exam number")
        p2 = plt.xlabel("time")
        plt.subplot(312)
        p1 = plt.bar(index, height=self.time_people,color ='green')
        p1 = plt.ylabel("student_number")
        p1 = plt.xlabel("time")
        plt.subplot(313)
        exam_class_num = [len(item[1]) for item in self.exam_class.items()]
        class_num = []
        for i in range(self.times_num):
            class_num.append(0)
            for j in self.solution_re[i]:
                class_num[i] += exam_class_num[j]
        p3 = plt.bar(index, height=class_num, color='blue')
        p3 = plt.ylabel("class_number")
        p3 = plt.xlabel("time")
        plt.show()

    #获得最忙的几位同学的考试时间安排
    def get_busiest_stu(self,n):
        num_list = [len(item[1]) for item in self.stu_exam.items()]
        busy = np.argsort(num_list)[-n:]
        for i in busy:
            self.get_one_stu(i)
            print()

    #获得这门考试可以调整到的时间
    def available(self, id):
        all = [i for i in range(self.times_num)]
        for i in self.adj[id]:
            if self.solution[i] in all:
                all.remove(self.solution[i])
        print("exam "+str(id)+" :"+self.exam_name[id]+"可调整到时间段:")
        print(all)

    # 查看某一时间段的安排的考试
    def one_day(self, t):
        day = int(t/4+1)
        when = t%4
        print("第"+str(day)+"天，第"+str(when)+"时间段的考试有")
        for i in self.solution_re[t]:
            print("id: "+str(i)+" name: "+self.exam_name[i]+" people: "+str(self.exam_people[i])+"\nclass:",end='')
            print(self.exam_class[i])
            print()

    #将考试(id) 从past调整到now时间段
    def change(self, id, now):
        for i in self.adj[id]:
            if self.solution[i]==now:
                print("该操作会引起考试冲突，你可以参考下面的信息。")
                self.available(id)
                return
        assert type(id)==int
        past = self.solution[id]
        self.solution[id] = now
        self.solution_re[past].remove(id)
        self.solution_re[now].append(id)
        self.time_people[past] -= self.exam_people[id]
        self.time_people[past] += self.exam_people[id]
        self.exam_time[past]-=1
        self.exam_time[now]+=1

    #输出excle文件。格式为[exam_id|exam_name|time]
    def out(self):
        out = pd.DataFrame.from_dict(self.solution, orient='index',columns=['time'])
        out['exam_name'] = self.exam_name
        out = out.reset_index().rename(columns = {'index':'exam'})
        out = out.sort_values(by = 'time',axis = 0,ascending = True)
        out.to_excel('result.xlsx',index=False)

    def __init__(self, name,times_num):
        name = 'data/'+name
        self.name = name
        self.solution = np.load(name+'_solution.npy', allow_pickle=True).item()
        self.stu_exam = np.load(name+'_stu_exam.npy',allow_pickle=True).item()
        self.exam_class = np.load(name+'_exam_class.npy',allow_pickle=True).item()
        self.exam_people = np.load(name+'_num.npy')
        self.time_people = np.load(name+"_people_time.npy")
        self.exam_num = len(self.solution.keys())
        self.times_num = times_num
        self.solution_re = dict(zip([i for i in range(self.times_num)], [[] for i in range(self.times_num)]))
        for i in self.solution.keys():
            self.solution_re[self.solution[i]].append(i)
        exam_index = np.load(name + "_exam_index.npy", allow_pickle=True).item()
        stu_index = np.load(name + "_stu_index.npy", allow_pickle=True).item()
        self.exam_name = list(exam_index.keys())
        self.stu_name = list(stu_index.keys())
        self.cij = np.load(name + "_cij.npy")
        self.exam_time = np.load(name+"_exam_time.npy")
        for i in range(self.exam_num):
            self.adj[i] = (np.where(self.cij[i] > 0))[0].tolist()
if __name__=='__main__':
    r = result('example',56)
    r.outline()