#!/usr/bin/env python
#coding:utf8

import MySQLdb as mdb
import sys
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import logging
reload(sys)
sys.setdefaultencoding('utf-8')

host = 'xxxxx'
user = 'xxxxx'
pawd = 'xxxxx'
dbus = 'xxxxx'
my_sender='xxxxx@139.com'
my_pass = 'xxxxx'
my_user=['xxxxx@xxx.xxx','xxxxx@xxx.xxx']

def query():
    '''
    ###https://github.com/hxgdzyuyi/tang_poetry/blob/master/tang_poetry.sql
    CREATE TABLE new_poetries as SELECT * FROM poetries WHERE id IS null;
    CREATE TABLE `new_poetries` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `name` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
        `title` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
        `content` text COLLATE utf8_unicode_ci,
        `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (`id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci
    '''
    con = mdb.connect(host, user, pawd, dbus, charset='utf8');
    cur = con.cursor()
    cur.execute("select pt.id, pt.name, pc.title, pc.content from poetries pc join poets pt on pc.poet_id = pt.id order by rand() limit 1;")
    res = cur.fetchone()
    for i in cur:
        print i[0],i[1],i[2],i[3]
    deleted_sql = "delete from poetries where id=%d;" %(i[0])
    created_sql = "insert into new_poetries(name, title, content) values ('%s', '%s', '%s');" % (i[1],i[2],i[3])
    
    cur.close()
    con.close()
    con = mdb.connect(host, user, pawd, dbus, charset='utf8');
    cur = con.cursor()
    try:
        cur.execute(deleted_sql)
        con.commit()
    except:
        con.rollback()
    cur.close()
    con.close()
    con = mdb.connect(host, user, pawd, dbus, charset='utf8');
    cur = con.cursor()
    try:
        cur.execute(created_sql)
        con.commit()
    except:
        con.rollback()
    cur.close()
    con.close()
    
    text = open('./poetry.text', 'w')
    text.write(i[1])
    text.write('\n')
    text.write(i[2])
    text.write('\n')
    text.write(i[3])
    text.close()

def pretty_(poem):
    contents = poem.split('。')
    for co in contents:
        if co != '' and len(co) > 10:
            print(co + '。')
def mail():
    ret=True
    f = open('./poetry.text', 'r')
    if not f:
        return
    result = list()
    for line in open('./poetry.text'):
        line = f.readline()
        result.append(line)
    try:
        contents = result[2].split('。')
        #msg=MIMEText(pretty_(poem=result[2]),'plain','utf-8')
        tttt = ""
        tttt += result[0].strip()+"："+result[1].strip()+"\n"
        tttt += "\n"
        for i in contents:
            if i != '' and len(i) > 10:
                tttt+=str(i)+('。')+"\n"
        msg=MIMEText(tttt,'plain','utf-8')
        msg['From']=formataddr(["诗情画意",my_sender])
        #msg['To']=formataddr(["cc",my_user])
        msg['To']=",".join(my_user)
        msg['Subject']="%s：%s" % (result[0].strip(), result[1].strip())
        #print msg['Subject']
        server=smtplib.SMTP_SSL("smtp.139.com", 465)
        server.login(my_sender, my_pass)
        #server.sendmail(my_sender,[my_user,],msg.as_string())
        server.sendmail(my_sender,my_user,msg.as_string())
        server.quit()
    except Exception:
        ret=False
    f.close()
    return ret

def job_function():
    query()
    ret=mail()
    if ret:
        print("邮件发送成功")
    else:
        print("邮件发送失败")

logging.basicConfig()
sched = BlockingScheduler()
sched.add_job(job_function, 'interval', hours=12, start_date='2018-09-21 09:30:00', end_date='2020-09-20 09:30:00')
#sched.add_job(job_function, 'date', run_date='2018-09-21 09:51:00')
sched.start()
