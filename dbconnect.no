import pymysql
def dbconnect():
    connection = pymysql.connect(host='localhost', user='root', passwd='rc.353', db='COURSERA', charset='utf8')
    return connection

