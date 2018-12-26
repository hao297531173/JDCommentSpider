# JDCommentSpider
这个项目使用python+selenium做JD商品爬虫<br>
PS:所有的数据都是JD网站获取，仅供学习交流使用<br>
### 使用的依赖库<br>
python 3.6<br>
selenium python自动化测试框架<br>
bs4 BeautifulSoup html元素提取器<br>
jieba jieba分词器<br>
wordcloud 词云<br>
matlibplot 2D绘图库<br>
pyecharts 图表库<br>
以及nlp在线分析网站 [boson](https://bosonnlp.com)<br>
### 文件夹解析<br>
anaImage---存放所有的图表<br>
"%sdata_sku"%goodName---存放所有的数据，包括评论，词频和sku号<br>
"%sanalysis"%goodName---存放情感分析数据<br>
### 根目录文件解析<br>
badComment.txt---记录各个品牌的差评率<br>
priceInfo.txt---记录各个品牌的均价<br>
satisfaction.txt---记录用户对于各个品牌的满意程度<br>
以上文件的数据都是以二元组的形式 goodName,data 给出<br>
### 主要分析的数据<br>
所有的图表都放在 [anaImage](https://github.com/hao297531173/JDCommentSpider/tree/master/anaImage)文件夹中<br>
这个项目我没有将所有的信息都爬取下来，实际上只要是页面上有的基本都可以爬取的到<br>
并且通过这些信息可以做更多的数据分析，这里我只是分析了评论关键词词频<br>
(词频是用json文件存放的,存放在"%sdata_sku"%goodName文件夹中
比如嗦 [魅族词频.json](https://github.com/hao297531173/JDCommentSpider/blob/master/%E9%AD%85%E6%97%8Fdata_sku/%E9%AD%85%E6%97%8F%E8%AF%8D%E9%A2%91.json)
<br>
![Image text](https://github.com/hao297531173/JDCommentSpider/blob/master/anaImage/%E9%AD%85%E6%97%8F%E8%AF%84%E8%AE%BA%E8%AF%8D%E4%BA%91.jpg?raw=true)
平均价格<br>
![Image text](https://github.com/hao297531173/JDCommentSpider/blob/master/anaImage/%E7%88%AC%E5%8F%96%E7%9A%84%E5%90%84%E5%93%81%E7%89%8C%E6%89%8B%E6%9C%BA%E7%9A%84%E5%B9%B3%E5%9D%87%E4%BB%B7%E6%A0%BC.png?raw=true)
<br>差评率
![Image text](https://github.com/hao297531173/JDCommentSpider/blob/master/anaImage/%E5%90%84%E4%B8%AA%E5%93%81%E7%89%8C%E6%89%8B%E6%9C%BA%E5%B9%B3%E5%9D%87%E5%B7%AE%E8%AF%84%E7%8E%87%EF%BC%88%E6%94%BE%E5%A4%A710w%E5%80%8D%EF%BC%89.png?raw=true)
<br>
并且通过boson的在线情感分析器分析用户对于产品的满意程度<br>
![Image text](https://github.com/hao297531173/JDCommentSpider/blob/master/anaImage/%E7%94%A8%E6%88%B7%E6%BB%A1%E6%84%8F%E5%BA%A6%EF%BC%88%E4%BB%A5100%E4%B8%BA%E5%9F%BA%E5%87%86%EF%BC%89.png?raw=true)
<br>
### PS:由于网络不好加上穷，买不起boson的分析次数，只能使用免费的次数，所以满意程度的分析数据量较小，只是做一个示范，不是真实的满意程度。
### 下面说一下各个脚本的作用<br>
所有可运行的脚本都在根目录<br>
boot.py---总的调用脚本，相当于mian函数<br>
JDCommentSpider.py---爬虫主文件，用于根据关键词获取商品信息和评论等数据<br>
getCommentInfo.py---主要用于提取评论信息，并且计算词频（计算的文件都在"%sdata_sku"%goodName文件夹中）<br>
analysis.py---所有的分析操作都在这个脚本中<br>
### 主要API说明<br>
#### [JDCommentSpider.py](https://github.com/hao297531173/JDCommentSpider/blob/master/JDCommentSpider.py)<br>

getSku 根据关键字获取在京东上搜索的商品sku信息，并且写入txt<br>
getCommentRun 根据输入数据获取number个商品信息，每个商品commentNum个评论<br>
getCommentAssign 根据给定的goodSku信息获取商品评论，获取commentNum个评论<br>

#### [getCommentInfo.py](https://github.com/hao297531173/JDCommentSpider/blob/master/getCommnetInfo.py)<br>

实例化类的时候需要传入 goodName 作为商品名称标识，一次找到需要处理的数据<br>
run()开始方法，不用传入参数<br>

#### [analysis.py](https://github.com/hao297531173/JDCommentSpider/blob/master/analysis.py)<br>
run(goodNum=2)开始根据评论信息分析情感倾向（需要先到boson注册账号获取X-Token秘钥，文件中给出的秘钥请换成自己的）,goodNum是你需要分析的商品数量<br>
[boson开发者文档](https://bosonnlp.com/dev/center)<br>
getSatisfaction()用于计算平均情感倾向，请在run()后面调用<br>
getSatic()获取情感分析倾向数据并作图，依据是根目录下的satisfaction.txt文件，所以请把所有待求商品的数据计算完再调用这个方法<br>
getBarImage()同上，也是最后调用，用于做出平均价格和差评率的柱状图<br>

#### [boot.py](https://github.com/hao297531173/JDCommentSpider/blob/master/boot.py)<br>
main(goodsName=[])请将你要查询的商品关键词写入一个列表中当做参数传递，然后直接运行就行了<br>

### 我想说的一些话<br>
这个项目就是一个示例，有很多地方可以优化，比如代码结构不够清晰，爬取资源过少，分析数据过少等等。<br>

### 代码使用方法<br>
只需要clone根目录几个py文件，然后运行boot.py ,goodsName列表就是关键词列表。<br>
如果想要进行其他数据的分析，可以根据需要修改代码。
