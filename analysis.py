"""
这个文件就是boson的接口，所有的分析爬虫都写在这里
秘钥
"""

import requests
import json
import os
import time
from bs4 import BeautifulSoup
from pyecharts import Bar
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
class Analysis:
    """
    所有的在线分析方法都写在这个类里
    """
    """
    构造函数
    """
    def __init__(self, goodName):
        self.goodName = goodName
        #情感分析接口api
        self.sentimentUrl = "https://api.bosonnlp.com/sentiment/analysis"
        #头文件信息
        self.headers={
            "X-Token" : "PgvyhuAo.32343.VQka8tdRfaxI",
            "Content-Type": "application/json"
        }
        #储存评论信息的列表
        self.comment = []
        #path
        self.filePath = "%sdata_sku"%self.goodName
        #获得该目录下所有json文件的名称
        self.filesName = []
        for root, dirs, files in os.walk(self.filePath, topdown=False):
            for name in files:
               self.filesName.append(name)
        #情感分析数据存放路径
        self.anaFilePath = "%sanalysis"%(self.goodName)
        exist = os.path.exists(self.anaFilePath)
        if not exist:
            os.makedirs(self.anaFilePath)
        self.anaPath = "anaImage"
        exist = os.path.exists(self.anaPath)
        if not exist:
            os.makedirs(self.anaPath)
        #词云字体路径(根据自己的情况填写)
        self.fontPath = "C://Windows//Fonts//simhei.ttf"
    """
    析构函数
    """
    def __del__(self):
        pass

    """
    获取评论数据
    @:param goodNum 最多获取的商品数量
    """
    def getcommentInfo(self, goodNum=2):
        for file in self.filesName:
            if(file[-4:]==".txt" and file!="data-sku%s.txt"%(self.goodName)):
                goodNum -= 1
                if(goodNum == 0):
                    return
                path = self.filePath + "/" + file
                with open(path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    for line in lines:
                        line = line.replace("\n", "")
                        self.comment.append(line)

    """
    发送请求获得情感分析
    """
    def post(self):
        #发送缓存列表，存满100个就发
        comCache = []
        numOf = 20
        for i in range(len(self.comment)):
            if(i%numOf==0 and i!=0):
                if(len(comCache)>numOf):
                    print("超出范围，缩小范围后post")
                    comCache = comCache[:numOf]
                #满numOf个了，该发送了
                print(comCache)
                data = json.dumps(comCache)
                resp = requests.post(self.sentimentUrl, headers=self.headers, data=data.encode("utf-8"))
                #接下来该拆分字符串了
                text = resp.text.replace("[", " ").replace("]", " ")
                text = text.strip()
                text = text.split(", ")
                print(text)
                #写入相应文件
                path = self.anaFilePath + "/" + "%s情感分析数据.txt"%self.goodName
                with open(path, "a") as f:
                    for k in range(len(text)):
                        if(k%2==0 and k!=0):
                            f.write("\n")
                        f.write(text[k] + ",")
                comCache = []
                comCache.append(self.comment[i])
                time.sleep(5)
            else:
                comCache.append(self.comment[i])
        #如果缓存里还有数据则再发送一次
        if(len(comCache)!=0):
            data = json.dumps(comCache)
            resp = requests.post(self.sentimentUrl, headers=self.headers, data=data.encode("utf-8"))
            #接下来该拆分字符串了
            text = resp.text.replace("[", " ").replace("]", " ")
            text = text.strip()
            text = text.split(", ")
            print(text)
            #写入相应文件
            path = self.anaFilePath + "/" + "%s情感分析数据.txt"%self.goodName
            with open(path, "a") as f:
                for k in range(len(text)):
                    if(k%2==0 and k!=0):
                        f.write("\n")
                    if(text[k]!='{"status":429,"message":"count limit exceeded"}'):
                        f.write(text[k] + ",")
            time.sleep(2)

    """
    根据获得的情感倾向数据得到平均情感倾向，并且写入到根目录的satisfaction.txt
    """
    def getSaticfaction(self):
        like = 0
        dislike = 0
        count = 0
        path = self.anaFilePath + "/" + "%s情感分析数据.txt"%self.goodName
        with open("satisfaction.txt", "a", encoding="utf-8") as file:
            with open(path, "r") as f:
                lines = f.readlines()
                for line in lines:
                    data = line.split(",")
                    for i in range(len(data)):
                        data[i] = data[i].strip()
                        if(data[i]!=""):
                            if(i%2==0):  #正面情绪值
                                count += 1
                                like += float(data[i])
                            else:
                                dislike += float(data[i])
            print("like=", like)
            print("count=",count)
            like = like/count
            dislike = dislike/count
            file.write("%s"%self.goodName+","+str(like)+","+str(dislike)+"\n")



    """
    用于生成价格和差评的柱状图
    """
    def getBarImage(self):
        #先获得平均价格的柱状图
        barMeanPrice = Bar("爬取的各品牌手机的平均价格")
        x=[]
        y=[]
        with open("priceInfo.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                info = line.split(",")
                x.append(info[0])
                print(info[0])
                y.append(float(info[1]))
                print(float(info[1]))
        kwargs=dict(
            name="柱形图",
            x_axis = x,
            y_axis = y
        )
        barMeanPrice.add(**kwargs)
        path = self.anaPath + "/平均价格.html"
        barMeanPrice.render(path)
        #接着是差评率
        barBadComment = Bar("各个品牌手机平均差评率（放大10w倍）")
        x=[]
        y=[]
        with open("BadComment.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                info = line.split(",")
                x.append(info[0])
                print(info[0])
                y.append(float(info[1])*100000)
                print(float(info[1])*100000)
        kwargs=dict(
            name="柱形图",
            x_axis = x,
            y_axis = y
        )
        barBadComment.add(**kwargs)
        path = self.anaPath + "/平均差评率.html"
        barBadComment.render(path)

    """
    用于生成用户满意度柱状图
    """
    def getSatic(self):
        barSatic = Bar("用户满意度（以100为基准）")
        x=[]
        y=[]
        with open("satisfaction.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                info = line.split(",")
                x.append(info[0])
                print(info[0])
                y.append(float(info[1])*100)
                print(float(info[1])*100)
        kwargs=dict(
            name="柱形图",
            x_axis = x,
            y_axis = y
        )
        barSatic.add(**kwargs)
        path = self.anaPath + "/用户满意度.html"
        barSatic.render(path)


    """
    用于根据词频生成词云
    """
    def getCloudWrod(self):
        wc = WordCloud(
            max_font_size=200,
            font_path=self.fontPath,
            width=1400,
            height=800,
            background_color="white",
            margin=2,
            max_words=500,
        )
        path = self.filePath + "/%s词频.json"%self.goodName
        dict = {}
        with open(path, "r", encoding="utf-8") as f:
            dict = json.load(f)
        wc.generate_from_frequencies(dict)
        #显示
        plt.figure()
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")
        savePath="anaImage/%s评论词云.jpg"%self.goodName
        plt.savefig(savePath, dpi=200)
        plt.ion()
        time.sleep(5)
        plt.close()

    """
    开始方法
    @:param goodNum 要调用评论的商品数
    """
    def run(self, goodNum=2):
        self.getcommentInfo(goodNum=goodNum)
        self.post()

if __name__=="__main__":
    ana = Analysis("小米")
    ana.run()
