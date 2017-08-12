# -*- coding:utf-8 -*-
import time

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, create_engine
from redis import StrictRedis
from bottle import Bottle, run

app = Bottle()
Base = declarative_base()
engine = create_engine("mysql://root:@localhost/test")
Session = sessionmaker()
Session.configure(bind=engine)
redis_client = StrictRedis(host='localhost', port=6379, db=0)
key = "concurrency_test"


class Table(Base):
    __tablename__ = 'concurrency_test'

    id = Column(Integer, primary_key=True)
    value = Column(Integer)


@app.route('/query')
def query():
    value = redis_client.get(key)
    if not value:
        # 缓存没有命中，从数据库中读取value
        first_row = Session().query(Table).filter(Table.id == 1).first()
        value = first_row.value
        print "Server query operation get value : {}".format(value)
        # 模拟比较费时间的业务逻辑
        time.sleep(1)
        # 设置缓存
        print "Server query operation time sleep over..."
        redis_client.set(key, value)

    return [str(value)]


@app.route('/update/<value:int>')
def update(value):

    session = Session()
    first_row = session.query(Table).filter(Table.id == 1).first()

    # 先更新数据库
    first_row.value = value
    session.commit()

    # 再删除缓存
    redis_client.delete(key)
    return "200"


if __name__ == '__main__':
    redis_client.delete(key)
    run(app=app, host='localhost', port=8080, debug=True, server='paste')
