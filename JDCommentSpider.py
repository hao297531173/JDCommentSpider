"""
这个文件用于在京东商品详情页面上爬取商品信息和用户评论
"""
#coding:utf-8
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import os
import json

"""
CommentSpider 提供的接口
getSku 根据关键字获取在京东上搜索的商品sku信息，并且写入txt
getCommentRun 根据输入数据获取number个商品信息，每个商品commentNum个评论
getCommentAssign 根据给定的goodSku信息获取商品评论，获取commentNum个评论
"""

class CommentSpider:
    """
    这个类包含了从搜索商品的sku到爬取信息的全部方法
    """
    """
    构造函数
    初始化浏览器对象
    @:param goodsName 想要搜索的商品名称 如 小米
    """
    def __init__(self, goodsName):
        self.goodsName = goodsName
        self.browser = webdriver.Chrome()
        self.filePath = "%sdata_sku"%(self.goodsName)
        exist = os.path.exists((self.filePath))
        if not exist:
            os.makedirs(self.filePath)
        #用于储存商品信息的字典
        self.dict = {}
        #商品页的基础url
        self.itemUrl = "https://item.jd.com/"

    """
    析构函数
    关闭浏览器对象
    """
    def __del__(self):
        try:
            self.browser.quit()
        except:
            print("已经成功退出浏览器...")

    """
    等待模块加载函数，供 getSku和getNextPage方法调用
    """
    def getWait(self):
        #所有class是gl-item的元素
        locator = (By.CLASS_NAME, "gl-item")
         #执行滑动到底部的js代码
        try:
            js = "var q=document.documentElement.scrollTop=100000"
            self.browser.execute_script(js)
            time.sleep(5)
        except:
            print("执行滑动js语句失败...")
        #执行等待元素加载的js语句
        try:
            #timeout时间是20， 每隔0.5秒就检查一次
            ele = WebDriverWait(self.browser, 20, 0.5).until(EC.presence_of_all_elements_located(locator))
        except:
            print("等待加载模块运行失败...")

    """
    getNextPage 获取下一页面的data-sku信息，供getSku方法调用
    @:param nextUrl 下一个页面的url
    @:param number 还需要爬取的商品数量
    @:return 1 爬取结束
    @:return 2 还需要再爬取下一个页面信息
    """
    def getNextPage(self, nextUrl, number):
        #geturl
        self.browser.get(nextUrl)
        #调用等待函数
        self.getWait()
        #获取页面的html代码
        html = self.browser.page_source
        #进行bs解析
        soup = BeautifulSoup(html, "html.parser")
        #接下来就开始爬取data-sku数据
        ul = soup.find("ul", {"class": "gl-warp"})
        liAll = ul.find_all("li", {"class": "gl-item"})
        for li in liAll:
            #读取data-sku
            dataSku = li["data-sku"] + ".html"
            self.writeSku(context=dataSku)
            number -= 1
            if(number == 0):
                return 1
        return 2

    """
    写文件，供getSku和getNextPage方法调用
    @:param context 待写入的数据
    """
    def writeSku(self, context):
        print("写操作")
        path = self.filePath + ("/data-sku%s.txt"%(self.goodsName))
        try:
            with open(path, "a") as file:
                file.write(context + "\n")
        except:
            print("写入文件执行失败...")
    """
    在search主页面上获取商品的sku数据
    @:param number 想要搜索的商品的数量
    """
    def getSku(self, number=60):
        baseUrl = "https://search.jd.com/Search?keyword=%s&enc=utf-8"%(self.goodsName)
        #检查是否有指定存放的文件夹
        exist = os.path.exists(self.filePath)
        if not exist:
            os.makedirs(self.filePath)
        #geturl
        self.browser.get(baseUrl)
        #调用等待函数
        self.getWait()
        #获取页面的html代码
        html = self.browser.page_source
        #进行bs解析
        soup = BeautifulSoup(html, "html.parser")
        #接下来就开始爬取data-sku数据
        ul = soup.find("ul", {"class": "gl-warp"})
        liAll = ul.find_all("li", {"class": "gl-item"})
        for li in liAll:
            print(li)
            #读取data-sku
            dataSku = li["data-sku"] + ".html"
            #写入文件
            self.writeSku(context=dataSku)
            number -= 1
            if(number == 0):
                return
        #执行到这里还没有退出就是需要翻页了
        pageNum = 3
        url = baseUrl + "&page="
        baseUrl = url + str(pageNum)
        while True:
            single = self.getNextPage(nextUrl=baseUrl, number=number)
            if(single == 1):
                return
            pageNum += 2
            baseUrl = url + str(pageNum)
    """
    getWaitItem 用于等待操作，供getComment调用
    """
    def getWaitItem(self):
        #所有class是gl-item的元素
        locator = (By.CLASS_NAME, "comment-con")
         #执行滑动到底部的js代码
        try:
            js = "var q=document.documentElement.scrollTop=100000"
            self.browser.execute_script(js)
            time.sleep(5)
        except:
            print("执行滑动js语句失败...")
        #执行等待元素加载的js语句
        try:
            #timeout时间是20， 每隔0.5秒就检查一次
            ele = WebDriverWait(self.browser, 20, 0.5).until(EC.presence_of_all_elements_located(locator))
        except:
            print("等待加载模块运行失败...")

    """
    写入json文档操作，供getComment调用
    @:param fileName 写入的json文档名称
    """
    def writeJson(self, fileName):
        fileName = self.filePath + "/" + fileName + ".json"
        print(fileName)
        with open(fileName, "w", encoding="utf-8") as f:
            #不加 ensure_ascii=False 会乱码
            json.dump(obj = self.dict, fp = f, ensure_ascii=False, indent=4)

    """
    getComment 用于实际操作获取评论，供getCommentRun调用
    @:param commentNum 获取评论条数
    @:param goodSku 商品的sku数据
    """
    def getComment(self,goodSku, commentNum):
        #组装url
        self.dict = {}
        url = self.itemUrl + goodSku
        self.browser.get(url)
        #等待动态加载
        self.getWaitItem()
        html = self.browser.page_source
        soup = BeautifulSoup(html, "html.parser")
        """获取商品名字"""
        name = soup.find("title").string
        #如果有括号就按照括号进行分割，否则按照空格分割，
        if(name[0] == "【"):
            name = name.split("【")[1].split("】")[0]
        else:
            nameSection = name.split(" ")
            name = ""
            for i in range(4):
                name = name+nameSection[i]
        #子字典
        subDict = {}
        #获取价格
        try:
            price = soup.find("span", {"class": "price"}).string
            subDict["price"] = price
        except:
            print("价格获取失败...")
            return
        #获取评论标签
        try:
            divTag = soup.find("div", {"class": "tag-list"})
            spans = divTag.find_all("span")
            tags = []
            for span in spans:
                tags.append(span.string)
            subDict["tags"] = tags
        except:
            #获取标签失败基本就能说明是预售产品，直接跳过
            print("评论获取失败，可能是预售产品，直接跳过...")
            return
        #获取评论数据，好评中评和差评
        ul = soup.find("ul", {"class": "filter-list"})
        liAll = ul.find_all("li", {"data-tab": "trigger"})
        #评论数据字典
        commData = {}
        for li in liAll:
            a = li.find("a")
            #获取a中的字符，要过滤掉img标签
            comStr = a.next.strip()
            em = a.find("em")
            comNum = em.string
            #去掉括号
            comNum = comNum.split("(")[1].split(")")[0]
            #写入字典
            commData[comStr] = comNum
        #写入子字典
        subDict["comm_data"] = commData
        ###获取商品详细评论###
        divAll = soup.find_all("div", {"class": "comment-item"})
        comment = {}
        #记录用户编号
        numOfUser = 1
        #记录评论信息的列表
        for div in divAll:
            #每一条评论都要用一个新的列表
            com = []
            userName = "user-"+str(numOfUser)
            numOfUser += 1
            #获取详细信息
            p = div.find("p", {"class": "comment-con"})
            com.append(p.string)
            #调试用，打印评论
            print(p.string)
            message = div.find("div", {"class": "order-info"})
            mes = message.find_all("span")
            for mess in mes:
                com.append(mess.string)
                time.sleep(0.2)
            #最后拉入字典中，每增加一条记录都执行插入操作
            comment[userName] = com
            subDict["comment"] = comment
            commentNum -= 1
            if(commentNum==0):
                #写入字典
                self.dict[name] = subDict
                fileName = name + "comment"
                self.writeJson(fileName=fileName)
                return
        ###翻页###
        while True:
            time.sleep(2)
            #先寻找下一页操作是否存在，如果存在就翻页，否则就退出
            nextPager = soup.find("a", {"class": "ui-pager-next"})
            try:
                print(nextPager)
                commentNum -= 10
                print(commentNum)
            except:
                print("没有下一页按钮了，下一个...")
                return
            #使用js进行翻页操作
            try:
                js = "var q=document.getElementsByClassName('ui-pager-next')[0].click()"
                self.browser.execute_script(js)
                print("翻页成功...")
            except:
                print("翻页操作失败...")
                return
            #重新获取网页原码
            html = self.browser.page_source
            soup = BeautifulSoup(html, "html.parser")
            #检查是否暂无评价，如果是的话就退出
            ac = soup.find("div", {"class": "ac"})
            if(ac.string == "「暂无评价」"):
                return
            divAll = soup.find_all("div", {"class": "comment-item"})
            for div in divAll:
                #每一条评论都要用一个新的列表
                com = []
                userName = "user-"+str(numOfUser)
                numOfUser += 1
                #获取详细信息
                p = div.find("p", {"class": "comment-con"})
                com.append(p.string)
                #调试用，打印评论
                print(p.string)
                message = div.find("div", {"class": "order-info"})
                mes = message.find_all("span")
                for mess in mes:
                    com.append(mess.string)
                #最后拉入字典中，每增加一条记录都执行插入操作
                comment[userName] = com
                subDict["comment"] = comment
                commentNum -= 1
                print(commentNum)
                if(commentNum<0):
                    #写入字典
                    self.dict[name] = subDict
                    fileName = name + "comment"
                    self.writeJson(fileName=fileName)
                    return

    """
    getCommentRun 获取JD商品信息和评论
    @:number 获取商品的数量 0-120
    @:commentNum 获取评论的数量
    """
    def getCommentRun(self, number, commentNum):
        #先获取商品sku
        path = self.filePath + "/data-sku%s.txt"%self.goodsName
        with open(path, "r") as file:
            lines = file.readlines()
            for line in lines:
                self.getComment(goodSku=line, commentNum=commentNum)
                number -= 1
                if(number == 0):
                    self.browser.close()
                    return

    """
    getCommentAssign 指定商品的sku获取商品信息
    @:param commentNum 获取的商品评论数
    @:param goodSku 商品sku信息
    """
    def getCommentAssign(self, goodSku, commentNum):
        self.getComment(goodSku=goodSku, commentNum=commentNum)
        self.browser.close()

    """
    这是进行各种测试的方法
    """
    def test(self):
        self.browser.get("https://item.jd.com/6737464.html#comment")
        html = self.browser.page_source
        soup = BeautifulSoup(html, "html.parser")
        a = soup.find("div", {"class": "jfaeinv"})
        try:
            print(a + "成功啦...")
        except:
            print("成功了...")
            return
        b = soup.find("div", {"class": "comment-more"})
        print(type(b))

"""
遇到的问题：当进入预售页面的时候会无限翻页操作
"""

if __name__=="__main__":
    spider = CommentSpider("小米")
    spider.getSku(120)
    spider.getCommentRun(10, 200)
    #goodSku = "7437564.html"
    #spider.getCommentAssign(goodSku=goodSku, commentNum=1000)
    #spider.test()


