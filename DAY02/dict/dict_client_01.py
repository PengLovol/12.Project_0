#!/usr/bin/python3
#coding=utf-8

from socket import *
import sys
import getpass
#建立连接和完成并发关系
#创建网络连接
def main():
    if len(sys.argv)<3:
        print("argv is error")
        return

    HOST=sys.argv[1]
    PORT=int(sys.argv[2])
    s=socket()
    try:
        s.connect((HOST,PORT))
    except Exception as e:
        print(e)
        return


    while True:
        print('''
        ==================Welcome===============
        ----1.注册　　2.登录   3.退出-----
        ''')
        cmd=input("输入选项>>")


if __name__=='__main__':
    main()