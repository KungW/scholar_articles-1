# scholar_articles

##`History`
### 2016-4开始GoogleScholar方向工作
> 接手前articles表中有314037条数据，最大id为314060
 截止到2016-9-11，大约52w，单机日增量3k-9k，电磁学的学者从谷歌上检索完成，大部分条目已存，只爬谷歌最近的增量

### 2016-9-25起启动杂志社方向爬虫
> 截止到2016-10-1，大约200w，单机日增量30w-50w
 publisher进度:
 IEEE（80家journal，文章总量30w，进度[80/80]） 
 Springer（700家journal，文章总量400w-600w，进度[94/700]）
 Elsevier（1200家journal，文章总量700w-1000w，进度[76/1200]）
 
### 2016-10-22杂志社方向学术信息采集完成
> article 1700万， scholar 3000万，a-s,a-a,s-s关系表，数量均亿级别
 
##`JournalTask`

###数据关系为：
- `publisher->journal->volume->article`
- `出版社->期刊->卷->文章`

- 一个出版社一个解析器

###解析器包括三层：

- 数据库中保存的journal site_source解析至journal主页
（少部分直接保存的就是journal主页，大部分需要一些转换）

- journal主页解析得到所有volume_link

- 针对每个volume_link页写解析器，得到该页所有article
（注意多页的问题，但大部分情况是一页，一个杂志一卷，可能就是一年半载，不会有多少文章，至多几十篇）

> 以上三步是全过程，
     前两部都写在`JournalTask文件夹`的某某spider里
     注意继承`JournalSpider`基类
     第三部写在`journal_parser文件夹`的某某parser里
     注意继承`JournalArticle`基类

# 挖掘工作的两个方向和重点： 
##杂志社方向

>	根据[SJR](http://www.scimagojr.com/journalrank.php)提供的journal rank
	索引各个领域排名靠前的杂志社.对于每个杂志社或出版社做解析器，
	爬取所有论文结果以及相关的作者及各种数据关系（技术上包括单机多线程，多机器混合调度等）
	映射为数据库中的各个表。
	数据关系层次为：Area——Journal——Article——Scholar

##`Google Schloar`

* title
* year
* citations_count
* link
* bibtex
* resource_type
* resource_link
* summary(abstract)
* google_id


###条目初步创建

#### ArticleSpider.py
包含:
- 获取搜索结果urls的`ScholarSearch`类
- 爬虫主控制器`ArticleSpider`类

工作原理：
> spider从db中检索出scholar姓名
 交予`ScholarSearch`得到url，访问后得到源码交给`HtmlParser`模型

#### parse_html.py
包含：
- 解析搜索结果页面的`HtmlParser`类，
- 逻辑上的`Article`类，包括属性的获取，数据库保存

工作原理：
> paser解析出文章元素列表`secs`
 分别生成`Article`对象获得所有文章属性，存入数据库

###异步获取细节
#### pdf_download.py
> 仅包含一个`pdf_downloader`类
 从远程db中检索出**存在且未下载**的pdf_url条目，存于本地
 可脱离于主程序，在宿机器上运行

####**journal_pdf_url_generate.py
>  某些pdf_url谷歌无法拿到，需要版权
 针对每一学校购置版权的杂志社，写好parser，由db中的title，去搜索页检索，得到pdf_url，反馈给db

#### bibtex.py
包含:
- 爬虫控制器`BibtexSpider`类
- 逻辑上的`Bibtex`类，包括属性的获取，数据库保存

工作原理：
- 从db中检索出未填充好bibtex的article条目
- 根据google_id,规则匹配url，进入中间页，寻找bibtex页面的url
- 进入bibtex页面，获取完毕

##`PDF Download`
下载模块可多机器分布下载，读写公共数据库。
对于以上两个方向集成出的article条目，做统一处理，拿到pdf_url后放入进程池即可。为保证大范围内的下载工作正常且有序
：
- 添加上方提及的Manager WebServer角色

- 发挥集群带宽优势，确保不重复，不遗漏下载

- 对异常pdf url的过滤：

    -	自身指向性异常的

    -	下载获取后异常的

    -	文件大小上判断
    -	文件源码上判断
   
- 大部分失败样本特征为：

	文件尺寸较小
	文件源码包含html
	是下载权限未获取的情况（元数据采集时已一定程度上做过滤）

-   对于下载后的维护：
	数据库新建 pdf 表
	存入下载后的 pdf文件 各大属性，有效管理，最大程度减小数据丢失时的代价
	建立多份拷贝，一是为安全备份，二是为web展示以及数据分析时的高效调用

##`引用关系生成`
引用关系数据对文章价值，学者价值的评判相当重要
> 1）【初始化遍历】的单元设计（为获取19XX－现今的既有数据）
    建立引用关系表（google id——google id）
	抓取所有引用该文章的文章条目
	模糊匹配title或其他信息，看杂志社方向爬取到的论文，主库中是否已经包含
	未包含则追加至主库article表【递归树生成了新的节点】
	包含仅更新google id即可
	主库Postgresql： 存入引用关系表
	分库MongoDB： 由于引用文章的出版年份已知，可生成既有年份的时间轴json引用数据
	初期完全依赖Google Scholar，若试验下来速率不行，则按出版社为单位重新嵌入架构
    时间轴数据可得到被引用的年份分布，被引用趋势图，利于数据分析，与同领域论文纵向比较，按某种评价算法判定论文价值（后期影响对学者评判）
    总体算是一个递归任务，基本可以走到google scholar的任意路径以及全网的论文条目

> 2） 初始化完成后的【回溯工作】（为不断获取今时最新的数据）
    为节省回溯成本，挑出算法判断价值最高（如趋势图所判断出的，近几年被引用次数增速最快）的部分数据进行数据回溯
	得到最新的被引用次数，以及引用关系增量。
3）	初始化任务和回溯任务是对于一个文章item而言的，两个模块可同时工作，只需保证回溯的范围在已初始化的文章之中即可。

# 数据库方面： 
-	论文挖掘的两个方向的article条目特征：
	google scholar： 有google_id，但无journal_id
	各大杂志社： 有journal_id，但无google_id
-	article表的条目必有google_id和journal_id之一。
-	article scholar表与SJR提供的area——category——journal集成架构为关系型数据 
-	在数据库中先将SJR的关系型领域数据存到几张新表中（包括area，category，journal，journal_categoty,journal_area及publisher）
-   MongoDB中存取的动态时间轴数据，引用关系等。



# 目录结构及运行方法介绍

##`GoogleScholarTask`
 ###ArticleSpider:
> 由Scholar Name出发的挖掘对搜索结果页直接出现的所有article信息的直接捕获
    
 ###bibtex:
> 对二级页面的bibtex异步爬取
	Dynamic Data Update
	从静态网页上更新article条目

##`JournalTask`：
![](https://github.com/lyn716/pics_temp_area/blob/master/%E5%9B%BE%E7%89%87%201.png?raw=true)		

> `ExistedSpider`模块，专门放已经写好的爬虫配置和依赖， 
    由主控制器`MajorTaskManager`根据db中检索得到的杂志社url匹配关键词，启动相关爬虫并分配到线程中去。 

![](https://github.com/lyn716/pics_temp_area/blob/master/%E5%9B%BE%E7%89%87%202.png?raw=true)

> 譬如，启动爬取人工智能领域 

![](https://github.com/lyn716/pics_temp_area/blob/master/%E5%9B%BE%E7%89%87%203.png?raw=true)

![](https://github.com/lyn716/pics_temp_area/blob/master/%E5%9B%BE%E7%89%87%204.png?raw=true)


> 爬取到新文章提示 ：

![](https://github.com/lyn716/pics_temp_area/blob/master/%E5%9B%BE%E7%89%87%205.png?raw=true)
