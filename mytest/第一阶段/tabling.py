import numpy as np
class exam_table:
    cij =None
    w = None
    le = []
    sd = []
    lwd = []
    cost = 0
    solution = None
    # solution_re = None
    exam_num = 0
    times_num = 0
    adj = dict()
    name = ''


    def printHelper(self):
        solution_re = dict(zip([i for i in range(self.times_num)],[[] for i in range(self.times_num)]))
        for i in self.solution.keys():
            solution_re[self.solution[i]].append(i)

        with open(self.name+'+不在同一天+限制范围+DAG+100.txt', 'w') as f:
            f.write('{')  # 这样子字典没有自动的大括号要自己加
            for key in solution_re:
                f.write('\n')
                f.writelines('"' + str(key) + '": ' + str(solution_re[key]))
                print("the " + str(key) + ":", end=" ")
                print(solution_re[key])
            c = str(self.loss())
            print("loss:"+c)
            f.write('\nloss:'+c+'\n' + '}')


    def loss(self):
        tij = np.zeros(shape=np.shape(self.cij))
        for i in self.adj.keys():
            for j in self.adj[i]:
                tij[i][j] = abs(self.solution[i]-self.solution[j])
        bij = np.log(abs(tij-20)+1)
        return sum(sum(bij*self.cij))


    def n1(self,n):
        choose = np.random.choice(self.exam_num,n)
        for i in choose:
            j = int(np.random.rand() * self.times_num)
            while j < self.times_num:
                j_flag = True
                for c in self.adj[i]:
                    if abs((self.solution.get(c,-4)/4)-(j/4))<2:
                        j_flag = False
                        j+=4
                        break
                if j_flag:
                    self.solution[i] = j
                    break
        print(self.loss())

    def n2(self):
        return 0

    def n3(self):
        return 0

    def DAG(self,n,times):
        better_dict = self.solution.copy()
        min_loss = self.loss()
        t=times
        while n>0:
            self.n1(t)
            print()
            if self.loss()<min_loss:
                better_dict = self.solution.copy()
                min_loss = self.loss()
                n-=1
                t+=5
            else:
                self.solution = better_dict.copy()
                t-=5
                if t<0:
                    t = int(times/2)

    def first_step(self):
        self.lwd = np.argsort(-sum(self.cij))
        j_count = dict(zip([i for i in range(self.times_num)],[0 for i in range(self.times_num)]))
        m = int(self.exam_num/self.times_num*3/2)#设置了一个某种颜色最多的考试数量
        fail=[]
        for i in self.lwd:
            flag = True
            # for j in range(self.times_num):
            #     j_flag = True
            #     if j_count[j]>=m:
            #         continue
            #     for c in self.adj[i]:
            #         if self.solution.get(c) == j:
            #             j_flag=False
            #             break
            #     if j_flag:
            #         self.solution[i] = j
            #         j_count[j] +=1
            #         break
            j=0
            down_time=0
            while j <self.times_num:
                j_flag = True
                if j_count[j]>=m:
                    j+=1
                    if j >= self.times_num:
                        j = int(np.random.rand() * self.times_num)
                        if down_time>self.times_num:
                                fail.append(i)
                                break
                    continue
                for c in self.adj[i]:
                    if abs((self.solution.get(c,-4)/4)-(j/4))<2:#不在同一天
                        j_flag=False
                        j+=5
                        if j >= self.times_num:
                            j = int(np.random.rand() * self.times_num)
                            down_time+=1
                            if down_time>self.times_num:
                                fail.append(i)
                                j=0
                                j_flag=True
                        break
                if j_flag:
                    self.solution[i] = j
                    j_count[j] +=1
                    break

        for i in fail:
            for j in range(self.times_num-1,0,-1):
                j_flag = True
                for c in self.adj[i]:
                    if abs(self.solution.get(c,-4)-j)<2:
                        j_flag = False
                        break
                if j_flag:
                    self.solution[i] = j
                    break


    def getadj(self):
        for i in range(self.exam_num):
            self.adj[i] = (np.where(self.cij[i] > 0))[0].tolist()

    def __init__(self,name,times_num):
        self.cij = np.load(name+"_exam.npy")
        self.w = np.load(name+"_num.npy")
        self.exam_num = len(self.cij)
        self.solution = dict()
        self.times_num = times_num
        self.getadj()
        self.name=name



if __name__=="__main__":
    # mytable = exam_table("21data-group","21data-group",56)
    mytable = exam_table("data01", 56)
    mytable.first_step()
    mytable.printHelper()
    mytable.DAG(50,100)
    mytable.printHelper()
    # print(mytable.loss())