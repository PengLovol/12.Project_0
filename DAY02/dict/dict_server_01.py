'''
name :  Tedu
date :  2018-10-1
email:  xxx
modules: pymongo
This is a dict project for AID
'''
#建立连接和完成并发关系
from socket import *
import os
import time
import signal
import pymysql
import sys

#定义需要的全局变量
DICT_TEXT='./dict.txt'
HOST='0.0.0.0'
PORT=8000
ADDR=(HOST,PORT)

#流程控制
def main():
    #创建数据连接
    db=pymysql.connect('localhost','root','120913','dict')

    #创建套接字
    s=socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(ADDR)
    s.listen(5)

    #忽略子进程退出，防止僵尸进程,子进程结束时, 父进程会收到这个信号.
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)

    while True:
        try:
            c,addr=s.accept()
            print('Connect from',addr)
        except KeyboardInterrupt:              #ctrl c　客户端异常退出
            s.close()
            sys.exit('服务器退出')
        except Exception as e:
            print(e)
            continue

        #创建子进程
        pid=os.fork()
        if pid==0:
            s.close()
            print('子进程准备处理请求')
            do_child(c,db)
        else:
            c.close()
            continue

def do_child(c,db):
    #循环接收客户端请求
    while True:
        data=c.recv(128).decode()
        print(c.getpeername(),':',data)
        if (not data) or data[0]=='E':  #退出
            c.close()
            sys.exit(0)
        elif data[0]=='R':
             do_register(c,db,data)
        elif data[0]=='L':
            do_login(c,db,data)
        elif data[0]=='Q':
            do_query(c,db,data)
        elif data[0]=='H':
            do_hist(c,db,data)

def do_login(c,db,data):
    print("登录操作")
    l=data.split(' ')
    name=l[1]
    passwd=l[2]
    cursor=db.cursor() #创建数据库游标对象

    sql="select * from user where name='%s' and passwd='%s'"%(name,passwd)
    cursor.execute(sql)
    r=cursor.fetchone()

    if r==None:
        c.send(b'FALL')

    else:
        print("%s登录成功"%name)
        c.send(b'OK')

def do_query(c,db,data): #查询单词同时将历史记录插入到数据库中
    print("查询操作")
    l=data.split(' ')
    name=l[1]
    word=l[2]
    cursor=db.cursor()

    def insert_history():
        tm=time.ctime()

        sql="insert into  hist (name,word,time) values('%s','%s','%s')"%(name,word,tm)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()


    #文本查询
    try:
        f=open(DICT_TEXT)
    except:
        c.send(b'FALL')
        f.close()
        return
    for line in f:
        tmp=line.split(' ')[0] #每行按空格切割，得到每行的首单词
        print(tmp)
        if tmp>word:
            c.send(b'FALL')
            return
        elif tmp==word:
            c.send(b'OK')
            time.sleep(0.1)
            c.send(line.encode())
            f.close()
            insert_history()
            return
    c.send(b'FALL')
    f.close()

def do_hist(c,db,data):
    print("历史记录")
    l=data.split(' ')
    name=l[1]
    cursor=db.cursor()

    sql = "select * from hist where name='%s'" % name
    cursor.execute(sql)
    r=cursor.fetchall()
    if not r:
        c.send(b'FALL')
        return
    else:
        c.send(b'OK')

    for i in r:
        time.sleep(0.1)
        msg = "%s    %s    %s"%(i[1],i[2],i[3])
        c.send(msg.encode())
    time.sleep(0.1)
    c.send(b'##')



def do_register(c,db,data):
    print("注册操作")
    l=data.split(' ')
    name=l[1]
    passwd=l[2]
    cursor=db.cursor() #创建数据库游标对象

    sql="select * from user where name='%s'"%name
    cursor.execute(sql)
    r=cursor.fetchone()

    if r!=None:
        c.send(b'EXISTS')
        return

    #用户不存在插入用户

    sql = "insert into user (name,passwd) values ('%s','%s')" % (name, passwd)
    try:
        cursor.execute(sql)   # 执行sql语句
        db.commit()           # 提交到数据库执行
        c.send(b'OK')
    except:
        db.rollback()
        c.send(b'FAIL')
    else:
        print("%s注册成功"%name)




if __name__=='__main__':
    main()