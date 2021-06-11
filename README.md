# README

## 说明：

myIO用于处理输入

tabling用于生成考试排表

result用于数据可视化，以及辅助时间调整。

## 使用说明

#### step01

​	使用myIO处理输入，输入放进data文件夹，且需满足这样的格式。[班级号|课程号|学号]（此处默认数据经过加密）

​	在myIO的main函数中输入`process(file-name)#文件名`运行

#### step02

​	 使用tabling进行排表基本生成。在tabling.pyde的main函数中输入

```python
mytable = ExamTable("file-name", 56) #文件名
mytable.getSolution()
```

结果具有随机性，会实时输出损失函数，如果对结果不满意，可多次运行。

#### step03

​	使用result进行可视化和局部调整。首先需要创建result对象，需在前两步运行至少一次的基础上进行。

```python
r = result('file-name',56)	#创建对象时，需要文件名和考试时间段数
```

命令说明（推荐在命令行使用，以实时调整）

```python
  	#通过 id 获得一位同学的考试时间安排
    def get_one_stu(self, id)
    
    #可视化每个时间段对应考试数，学生人数，考试班级数以获得对整个方案的大致了解
    def outline(self)
        
    #获得最忙的n位同学的考试时间安排
    def get_busiest_stu(self,n)

    #获得这门考试可以调整到的时间
    def available(self, id)

    # 查看某一时间段的安排的考试
    def one_day(self, t)
       
    #将考试(id) 调整到now时间段
    def change(self, id, now)
        
	#输出excle文件。格式为[exam_id|exam_name|time]
    def out(self)
```

示例

![example](https://box.nju.edu.cn/f/c02232631cba405db7fc/?dl=1)

outline()结果

![outline](https://box.nju.edu.cn/f/fa3df0b381a5470ab95b/?dl=1)

.out方法以excle格式输出最终结果。

