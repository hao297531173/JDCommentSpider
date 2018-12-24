"""
这个文件将json中的评论信息汇总起来变成一个文件
"""
#coding:utf-8
#encoding:utf-8
import json
import os
import jieba
from collections import Counter


class getCommentInfo:
    """
    这个类用于将json文档中的评论信息提取出来，进行分析
    """

    """
    构造函数
    @:param goodName 商品名称
    """
    def __init__(self, goodName):
       self.goodName = goodName
       self.filePath = "%sdata_sku"%self.goodName
       #获得该目录下所有json文件的名称
       self.filesName = []
       for root, dirs, files in os.walk(self.filePath, topdown=False):
           for name in files:
               self.filesName.append(name)
       self.dict = {}
       #储存txt文件名的字符串
       self.txtName = ""
       #总价格
       self.price = 0
       #获取的商品个数
       self.priceNum = 0
       #获取商品评价总数
       self.commentNum = 0
       #获取商品差评数
       self.badComment = 0
       #词频文件名
       self.seqFileName = "%s/%s词频.json"%(self.filePath, self.goodName)
       #统计词频的字典
       self.seqDict = {}
    """
    析构函数
    """
    def __del__(self):
        pass

    """
    主体转换函数
    """
    def run(self):
        for file in self.filesName:
            print(file)
            if(file[-5:]==".json"):    #如果最后五位字符是‘.json’的话就认为是json
                #进行文档处理
                path = self.filePath+"/"+ str(file)
                #存储评论信息的列表
                com = []
                with open(path, "r", encoding="utf-8") as f:
                    self.dict = json.load(f)
                    for key in self.dict:
                        #获取价格
                        self.price += float(self.dict[key]["price"])
                        print(self.dict[key]["price"])
                        print(self.price)
                        self.priceNum += 1
                        #获取评论数据
                        self.commentNum += len(self.dict[key]["comm_data"]["全部评价"][0])*10000
                        print(self.commentNum)
                        self.badComment += len(self.dict[key]["comm_data"]["差评"].replace("+", ""))
                        self.txtName = key+".txt"
                        for k in self.dict[key]["comment"]:
                            #如果评论信息不是null就添加到列表中
                            if(self.dict[key]["comment"][k][0] != None):
                                com.append(self.dict[key]["comment"][k][0])
                #接着将com的内容写入到txt中
                path = self.filePath + "/" + self.txtName
                with open(path, "w", encoding="utf-8") as f:
                    for i in range(len(com)):
                        if(com[i]!="此用户未填写评价内容"):
                            f.write(com[i] + "\n")
                #统计各个写入的评论中top10的词
                com = []
                with open(path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    for line in lines:
                        com.append([x for x in jieba.cut(line) if len(x)>=2])
                for h in range(len(com)):
                    c = Counter(com[h]).most_common(2)
                    for k in range(len(c)):
                        #如果词典词频里没有这个词
                        if c[k][0] not in self.seqDict:
                            self.seqDict[c[k][0]] = int(c[k][1])
                        else:
                            self.seqDict[c[k][0]] += int(c[k][1])
        #将价格信息写入根目录的文件中
        with open("priceInfo.txt", "a", encoding="utf-8") as f:
            f.write("%s,"%self.goodName + str(self.price//self.priceNum) + "\n")
        #将差评率写入根目录的文件中
        with open("badComment.txt", "a", encoding="utf-8") as f:
            f.write("%s,"%self.goodName + str(self.badComment/self.commentNum) + "\n")
        #将词典信息写入目录中
        with open(self.seqFileName, "w", encoding="utf-8") as f:
            json.dump(obj = self.seqDict, fp = f, ensure_ascii=False, indent=4)

if __name__=="__main__":
    comm = getCommentInfo("小米")
    comm.run()