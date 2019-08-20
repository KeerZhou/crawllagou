#coding=gbk
import json
import multiprocessing
import re
import time
import requests
from lagouSpider.insert_data import lagou_mysql


class CrawlLaGou(object):
    def __init__(self):
        # 使用session保存cookies信息
        self.lagou_session = requests.session()
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
        }
        self.city_list = ""

    #获取城市
    def crawl_city(self):
        #使用正则表达式获取HTML代码中的城市名称
        city_search = re.compile(r'www\.lagou\.com\/.*\/">(.*?)</a>')
        #网页URL
        city_url = "https://www.lagou.com/jobs/allCity.html"
        city_result = self.crawl_request(method="GET", url=city_url)
        self.city_list = city_search.findall(city_result)
        self.lagou_session.cookies.clear()

    #获取职位信息
    def crawl_city_job(self,city):
        #职位列表数据包的url
        first_request_url = "https://www.lagou.com/jobs/list_python?city=%s&cl=false&fromSearch=true&labelWords=&suginput="%city
        first_response = self.crawl_request(method="GET", url=first_request_url)
        #使用正则表达式获取职位列表的页数
        total_page_search = re.compile(r'class="span\stotalNum">(\d+)</span>')
        try:
            total_page = total_page_search.search(first_response).group(1)
        except:
            # 如果没有职位信息，直接return
            return
        else:
            for i in range(1, int(total_page) + 1):
                #data信息中的字段
                data = {
                    "pn":i,
                    "kd":"python"
                }
                #存放职位信息的url
                page_url = "https://www.lagou.com/jobs/positionAjax.json?city=%s&needAddtionalResult=false" % city
                #添加对应的Referer
                referer_url = "https://www.lagou.com/jobs/list_python?city=%s&cl=false&fromSearch=true&labelWords=&suginput="% city
                self.header['Referer'] = referer_url.encode()
                response = self.crawl_request(method="POST",url=page_url,data=data,info=city)
                lagou_data = json.loads(response)
                #通过json解析得到的职位信息存放的列表
                job_list = lagou_data['content']['positionResult']['result']
                for job in job_list:
                    print(job)
                    lagou_mysql.insert_item(job)


    #返回结果
    def crawl_request(self,method,url,data=None,info=None):
        while True:
            if method == "GET":
                response = self.lagou_session.get(url=url,headers=self.header)
            elif method == "POST":
                response = self.lagou_session.post(url=url, headers=self.header, data=data)
            response.encoding = "utf8"
            #解决操作太频繁问题
            if '频繁' in response.text:
                print(response.text)
                self.lagou_session.cookies.clear()
                first_request_url = "https://www.lagou.com/jobs/list_python?city=%s&cl=false&fromSearch=true&labelWords=&suginput=" % info
                self.crawl_request(method="GET", url=first_request_url)
                time.sleep(10)
                continue
            return response.text

if __name__ == '__main__':
    lagou = CrawlLaGou()
    lagou.crawl_city()
    #print(lagou.city_list)
    #city = "深圳"
    #lagou.crawl_city_job(city)
    for city in lagou.city_list:
         lagou.crawl_city_job(city)
    #     break