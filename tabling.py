import numpy as np
import matplotlib.pyplot as plt


class ExamTable:
    cij =None
    w = None
    le = []
    sd = []
    lwd = []
    cost = 0
    solution = None
    exam_num = 0
    times_num = 0
    adj = dict()
    name = ''
    people=[]
    exam = []
    log = []

    def print_helper(self):
        solution_re = dict(zip([i for i in range(self.times_num)],[[] for i in range(self.times_num)]))
        for i in self.solution.keys():
            solution_re[self.solution[i]].append(i)

        with open(self.name+'solution.txt', 'w') as f:
            f.write('{')  # 这样子字典没有自动的大括号要自己加
            for key in solution_re:
                f.write('\n')
                f.writelines('"' + str(key) + '": ' + str(solution_re[key]))
                print("the " + str(key) + ":", end=" ")
                print(solution_re[key])

            c = str(self.people)
            print("the number of students:"+c)
            f.write("\nthe number of students: "+c)

            c = str(self.loss())
            print("loss:" + c)
            f.write('\nloss:' + c + '\n' + '}')

        index = np.arange(self.times_num)
        plt.subplot(211)
        p2 = plt.bar(index, height=self.exam,color='orange')
        p2 = plt.ylabel("exam number")
        p2 = plt.xlabel("time")
        plt.subplot(212)
        p1 = plt.bar(index, height=self.people,color ='blue')
        p1 = plt.ylabel("student_number")
        p1 = plt.xlabel("time")
        plt.show()


    def time_loss(self):
        tij = np.zeros(shape=np.shape(self.cij))
        for i in self.adj.keys():
            for j in self.adj[i]:
                tij[i][j] = abs(self.solution[i]-self.solution[j])
        bij = np.log(tij/self.times_num+1)
        l = sum(sum(bij*self.cij))/(2*self.exam_num)
        # print("time loss:"+str(l))
        return l


    def stu_loss(self):
        p = np.var(self.people)/1000
        print("stu loss:" + str(p))
        return p

    def loss(self):
        return self.time_loss()+self.stu_loss()*0.4

    def n1(self,n):
        choice = np.random.choice(self.exam_num,n)
        time = 0
        n -= 1
        while n>0:
            ifrom = self.solution[choice[n]]
            if self.change_time(choice[n]):
                self.log.append([choice[n],ifrom])
                n -= 1
            else:
                time += 1
            if time > 3:
                n -= 1
                time = 0

    def n2(self, a):
        high = np.argsort(self.people)[-5:]
        choice = []
        for i in range(self.exam_num):
            if self.solution[i] in high:
                choice.append(i)
        time = 0
        len(choice)
        n = min((len(choice)-1), a)
        while n > 0:
            ifrom = self.solution[choice[n]]
            if self.change_time(choice[n]):
                self.log.append([choice[n], ifrom])
                n -= 1
            else:
                time += 1
            if time > 3:
                n -= 1
                time = 0

    def change(self, exam_id, ito):
        self.people[self.solution[exam_id]] -= self.w[exam_id]
        self.exam[self.solution[exam_id]] -= 1
        self.solution[exam_id] = ito
        self.people[ito] += self.w[exam_id]
        self.exam[ito] += 1

    def change_time(self, i):
        j = int(np.random.rand() * self.times_num)
        while j < self.times_num:
            j_flag = True
            for c in self.adj[i]:
                if abs(self.solution[c]-j) < 4:
                    j_flag = False
                    j += 4
                    break
            if j_flag:
                self.people[self.solution[i]] -= self.w[i]
                self.exam[self.solution[i]] -= 1
                self.solution[i] = j
                self.people[j] += self.w[i]
                self.exam[j] += 1
                return True
        return False

    def DAG(self, n, times):
        better_dict = self.solution.copy()
        min_loss = self.loss()
        t = times
        while n>0:
            self.log = []
            self.n1(t)
            self.n2(t)
            print()
            lo = self.loss()
            print(lo)
            if lo < min_loss:
                min_loss = lo
                n -= 1
                t += 5
                if min_loss < 100:
                    break
            else:
                t -= 5
                self.log = self.log[0:int(len(self.log)/2)]
                for item in self.log:
                    self.change(item[0], item[1])
                if t < 0:
                    n -= 0.5
                    t = times

    def first_step(self):
        self.lwd = np.argsort(-sum(self.cij))
        j_count = [0 for i in range(self.times_num)]
        m = int(self.exam_num/self.times_num*3/2)#设置了一个某种颜色最多的考试数量
        for i in self.lwd:
            j = 0
            i_condition = True
            while j < self.times_num:
                j_flag = True
                if j_count[j] >= m:
                    j += 1
                    if j >= self.times_num:
                        j = int(np.random.rand() * self.times_num)
                        i_condition = False
                    continue
                for c in self.adj[i]:
                    if (i_condition and (abs((self.solution.get(c, -8))/4-(j/4)) < 2)) or (not i_condition and self.solution.get(c) == j):     #不在同一天
                        j_flag = False
                        j += 2 if i_condition else 1
                        if j >= self.times_num:
                            j = int(np.random.rand() * self.times_num)
                            i_condition = False
                        break
                if j_flag:
                    self.solution[i] = j
                    self.people[j] += self.w[i]
                    j_count[j] += 1
                    break
        self.exam = j_count
        mytable.print_helper()

    def get_adj(self):
        for i in range(self.exam_num):
            self.adj[i] = (np.where(self.cij[i] > 0))[0].tolist()

    def __init__(self, name, times_num):
        self.name ='data/'+name
        self.cij = np.load(self.name+"_cij.npy")
        self.w = np.load(self.name+"_num.npy")
        print(self.w)
        self.exam_num = len(self.cij)
        self.solution = dict()
        self.times_num = times_num
        self.get_adj()
        self.people = [0 for i in range(self.times_num)]

    def getSolution(self):
        mytable.first_step()
        mytable.DAG(10, 100)
        np.save(self.name+"_solution.npy", self.solution)
        np.save(self.name+"_people_time.npy",self.people)
        np.save(self.name+"_exam_time.npy",self.exam)
        mytable.print_helper()


if __name__ == "__main__":
    mytable = ExamTable("example", 56)
    mytable.getSolution()
