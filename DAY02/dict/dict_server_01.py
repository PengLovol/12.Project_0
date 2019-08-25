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
            sys.exit(0)
        else:
            c.close()
            continue


if __name__=='__main__':
    main()