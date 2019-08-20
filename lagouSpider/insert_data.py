from collections import Counter

from sqlalchemy import func

from lagouSpider.creat_lagou_tables import Lagoutables
from lagouSpider.creat_lagou_tables import Session
import time


class CrawlLagouData(object):
    def __init__(self):
        #实例化
        self.mysql_session = Session()
        self.date = time.strftime("%Y-%m-%d",time.localtime())

    #数据的存储方法
    def insert_item(self,item):
        #今天
        date = time.strftime("%Y-%m-%d",time.localtime())
        #数据结构
        data = Lagoutables(
            #职位ID
            positionID = item['positionId'],
            # 经度
            longitude=item['longitude'],
            # 纬度
            latitude=item['latitude'],
            # 职位名称
            positionName=item['positionName'],
            # 工作年限
            workYear=item['workYear'],
            # 学历
            education=item['education'],
            # 职位性质
            jobNature=item['jobNature'],
            # 公司类型
            financeStage=item['financeStage'],
            # 公司规模
            companySize=item['companySize'],
            # 业务方向
            industryField=item['industryField'],
            # 所在城市
            city=item['city'],
            # 职位标签
            positionAdvantage=item['positionAdvantage'],
            # 公司简称
            companyShortName=item['companyShortName'],
            # 公司全称
            companyFullName=item['companyFullName'],
            # 工资
            salary=item['salary'],
            # 抓取日期
            crawl_date=date
        )

        #在存储数据之前查询表里是否有这条岗位信息
        query_result = self.mysql_session.query(Lagoutables).filter(Lagoutables.crawl_date==date,
                                                                    Lagoutables.positionID == item['positionId']).first()

        if query_result:
            print('该岗位信息已存在%s:%s:%s' % (item['positionId'], item['city'], item['positionName']))
        else:
            #插入数据
            self.mysql_session.add(data)
            #提交数据
            self.mysql_session.commit()
            print('新增岗位信息%s' % item['positionId'])

lagou_mysql = CrawlLagouData()
#lagou_mysql.query_industryfield_result()
