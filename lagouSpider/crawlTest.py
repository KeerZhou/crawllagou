#coding=gbk
import json
import multiprocessing
import re
import time
import requests
from lagouSpider.insert_data import lagou_mysql


class CrawlLaGou(object):
    def __init__(self):
        # ʹ��session����cookies��Ϣ
        self.lagou_session = requests.session()
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
        }
        self.city_list = ""

    #��ȡ����
    def crawl_city(self):
        #ʹ��������ʽ��ȡHTML�����еĳ�������
        city_search = re.compile(r'www\.lagou\.com\/.*\/">(.*?)</a>')
        #��ҳURL
        city_url = "https://www.lagou.com/jobs/allCity.html"
        city_result = self.crawl_request(method="GET", url=city_url)
        self.city_list = city_search.findall(city_result)
        self.lagou_session.cookies.clear()

    #��ȡְλ��Ϣ
    def crawl_city_job(self,city):
        #ְλ�б����ݰ���url
        first_request_url = "https://www.lagou.com/jobs/list_python?city=%s&cl=false&fromSearch=true&labelWords=&suginput="%city
        first_response = self.crawl_request(method="GET", url=first_request_url)
        #ʹ��������ʽ��ȡְλ�б��ҳ��
        total_page_search = re.compile(r'class="span\stotalNum">(\d+)</span>')
        try:
            total_page = total_page_search.search(first_response).group(1)
        except:
            # ���û��ְλ��Ϣ��ֱ��return
            return
        else:
            for i in range(1, int(total_page) + 1):
                #data��Ϣ�е��ֶ�
                data = {
                    "pn":i,
                    "kd":"python"
                }
                #���ְλ��Ϣ��url
                page_url = "https://www.lagou.com/jobs/positionAjax.json?city=%s&needAddtionalResult=false" % city
                #��Ӷ�Ӧ��Referer
                referer_url = "https://www.lagou.com/jobs/list_python?city=%s&cl=false&fromSearch=true&labelWords=&suginput="% city
                self.header['Referer'] = referer_url.encode()
                response = self.crawl_request(method="POST",url=page_url,data=data,info=city)
                lagou_data = json.loads(response)
                #ͨ��json�����õ���ְλ��Ϣ��ŵ��б�
                job_list = lagou_data['content']['positionResult']['result']
                for job in job_list:
                    print(job)
                    lagou_mysql.insert_item(job)


    #���ؽ��
    def crawl_request(self,method,url,data=None,info=None):
        while True:
            if method == "GET":
                response = self.lagou_session.get(url=url,headers=self.header)
            elif method == "POST":
                response = self.lagou_session.post(url=url, headers=self.header, data=data)
            response.encoding = "utf8"
            #�������̫Ƶ������
            if 'Ƶ��' in response.text:
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
    #city = "����"
    #lagou.crawl_city_job(city)
    for city in lagou.city_list:
         lagou.crawl_city_job(city)
    #     break