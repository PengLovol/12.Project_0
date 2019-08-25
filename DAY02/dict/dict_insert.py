import pymysql 
import re  

f = open('dict.txt')
db = pymysql.connect\
('localhost','root','120913','dict')

cursor = db.cursor()    #创建游标对象

for line in f:
    l = re.split(r'\s+',line)
    word = l[0]              #单词
    interpret = ' '.join(l[1:]) #解释，用空格符将单词解释连接起来
    
    sql = "insert into words (word,interpret) \
    values('%s','%s')"%(word,interpret)

    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
f.close()

