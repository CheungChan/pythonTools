from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

IP = '10.2.52.29'
KILL = False
MYSQL_ADDR = 'mysql+pymysql://test:123456@10.4.82.150:3306/kylin_new?charset=utf8'
ECHO = True
BaseModel = declarative_base()
engine = create_engine(MYSQL_ADDR, echo=ECHO)
DBsession = sessionmaker(bind=engine)
session = DBsession()
processes = session.execute('show processlist').fetchall()
ids = [s[0] for s in processes if IP in s[2] and s[7] != 'show processlist']
for i in ids:
    s = 'kill ' + str(i) + ';'
    print(s)
    if KILL:
        session.execute(s)
print("执行完毕")
