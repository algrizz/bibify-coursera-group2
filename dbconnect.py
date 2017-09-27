import pymysql
def dbconnect():
    connection = pymysql.connect(host='localhost', user='root', passwd='coursera', db='COURSERA', charset='utf8')
    return connection

