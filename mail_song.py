#!/usr/bin/env python
#coding:utf8

import psycopg2
import sys
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import logging
reload(sys)
sys.setdefaultencoding('utf-8')

my_sender='xxxxx@139.com'
my_pass = 'xxxxx'
my_user=['xxxxx@xxx.xxx','xxxxx@xxx.xxx']

def query():
    '''
    ###https://github.com/chinese-poetry/chinese-poetry/blob/master/ci/ci.db
    '''
    con = psycopg2.connect("dbname=ci user=ci")
    cur = con.cursor()
    cur.execute("select rhythmic, author, content from ci order by random() limit 1;")
    res = cur.fetchone()
    print res[0], res[1], res[2]
    
    cur.close()
    con.close()

    text = open('./ci.text', 'w')
    text.write(res[0])
    text.write('\n')
    text.write(res[1])
    text.write('\n')
    text.write(res[2])
    text.close()

    ret=True
    try:
        
        msg=MIMEText(res[2].strip(),'plain','utf-8')
        msg['From']=formataddr(["诗情画意",my_sender])
        msg['To']=",".join(my_user)
        msg['Subject']="%s：%s" % (res[0].strip(), res[1].strip())
        server=smtplib.SMTP_SSL("smtp.139.com", 465)
        server.login(my_sender, my_pass)
        server.sendmail(my_sender,my_user,msg.as_string())
        server.quit()
    except Exception, err:
        ret=False
        print 1,err
    return ret

def job_function():
    ret=query()
    if ret:
        print("邮件发送成功")
    else:
        print("邮件发送失败")

#logging.basicConfig()
#sched = BlockingScheduler()
#sched.add_job(job_function, 'interval', hours=12, start_date='2018-09-21 09:30:00', end_date='2020-09-20 09:30:00')
##sched.add_job(job_function, 'date', run_date='2018-09-21 09:51:00')
#sched.start()
if __name__=='__main__':
    job_function()
