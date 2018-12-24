"""
这个文件相当于main函数
"""
import getCommnetInfo
import JDCommentSpider
import analysis


def main(goodsName=[]):
    #先爬取评论数据，并且提取数据，再获取情感分析数据
    for i in range(5, len(goodsName)):
        spider = JDCommentSpider.CommentSpider(goodsName[i])
        spider.getSku(60)
        spider.getCommentRun(10, 500)
        comm = getCommnetInfo.getCommentInfo(goodsName[i])
        comm.run()
        ana = analysis.Analysis(goodsName[i])
        ana.run(2)
        ana.getCloudWrod()
    #然后把平均价格和平均差评画出来
    ana = analysis.Analysis("")
    ana.getBarImage()
    ana.getSaticfaction()
    ana.getSatic()




if __name__ == "__main__":
    goodsName=["小米手机", "华为", "oppo", "锤子", "苹果手机", "魅族"]
    main(goodsName=goodsName)

