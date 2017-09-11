# ChinanewsScraper
ChinanewsScraper is a Scrapy crawler/spider for scrapping www.chinanews.com
, which includes 'wh','mil','gj','yl','ty','jk','sh','hr','fortune','cj','it','ny','ga','estate','auto','tw' sixteen branchs.  

## Overview （项目概述）  
本项目建立在scrapy框架基础上，编写code.py程序用于抓取**中国新闻网**（www.chinanews.com ）上多个类别的**新闻语料**（12-17年），包括文化，军事，国际，娱乐，体育，健康，社会，华人，金融，财经，it，能源，港澳，房产，汽车，台湾这16版块的**新闻类型**

## Requirements （项目环境） 
详细配置请参考https://github.com/adrianyoung/SCRAPY_BASIC  

## Configuration （文件设置）  
#### 只需在项目中的 `settings.py` 进行设置 
#### 1.NEWS TYPE SETTINGS  
填写需要抓取的**新闻类型(NEWS TYPE)**，包括文化，军事，国际，娱乐，体育，健康，社会，华人，金融，财经，it，能源，港澳，房产，汽车，台湾这16个版块  

    TYPE_LIST  =  # ['wh','mil','gj','yl','ty','jk','sh','hr','fortune','cj','it','ny','ga','estate','auto','tw']  
    
#### 2.SPIDERS DATE SETTINGS  
填写需要抓取新闻的**日期范围（DATE RANGE）**（格式:'20120601'），由于网页结构变动原因，本程序仅适用于抓取'20120601'至今的新闻网页    

    BEGIN_DATE =  # '20120601'  
    END_DATE   =  # '20170728'  
      
  
更多详细配置请参考https://github.com/adrianyoung/SCRAPY_BASIC
## Usage （运行测试）  

#### 1.运行命令:  
     
    $ scrapy crawl news  
    
#### 2.数据格式：
  
详细可参照项目中的`items.py`，其中JSON格式主要包括**新闻类型**，**日期**，**标题**，**正文**  

    news_type = scrapy.Field()
    news_date = scrapy.Field()
    news_title = scrapy.Field()
    news_text = scrapy.Field()

#### 3.数据结果：  
从mongodb导出得JSON格式数据存放在百度云盘，包含12-17年各类型的新闻  
**具体链接**: https://pan.baidu.com/s/1kV7R1jT **密码**: fwqx

 


> 关于我，欢迎联系  
  微信：[yd0301]() 邮箱：yd0301@outlook.com

