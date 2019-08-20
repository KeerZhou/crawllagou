from sqlalchemy import create_engine, Integer, Float, String
from sqlalchemy.orm import  sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
import pymysql

#创建数据库连接
engine = create_engine("mysql+pymysql://root:root@127.0.0.1:3306/lagou?charset=utf8")
#操作数据库
Session = sessionmaker(bind=engine)
#声明一个基类
Base = declarative_base()

class Lagoutables(Base):
    #表名称
    __tablename__ = 'lagou_java1'
    #id,设置为主键和自动增长
    id = Column(Integer,primary_key=True,autoincrement=True)
    #职位id
    positionID = Column(Integer,nullable=True)
    # 经度
    longitude = Column(Float, nullable=True)
    # 纬度
    latitude = Column(Float, nullable=True)
    # 职位名称
    positionName = Column(String(length=50), nullable=False)
    # 工作年限
    workYear = Column(String(length=20), nullable=False)
    # 学历
    education = Column(String(length=20), nullable=False)
    # 职位性质
    jobNature = Column(String(length=20), nullable=True)
    # 公司类型
    financeStage = Column(String(length=30), nullable=True)
    # 公司规模
    companySize = Column(String(length=30), nullable=True)
    # 业务方向
    industryField = Column(String(length=30), nullable=True)
    # 所在城市
    city = Column(String(length=10), nullable=False)
    # 职位标签
    positionAdvantage = Column(String(length=200), nullable=True)
    # 公司简称
    companyShortName = Column(String(length=50), nullable=True)
    # 公司全称
    companyFullName = Column(String(length=200), nullable=True)
    # 工资
    salary = Column(String(length=20), nullable=False)
    # 抓取日期
    crawl_date = Column(String(length=20), nullable=False)

if __name__ == '__main__':
    #创建数据表
    Lagoutables.metadata.create_all(engine)