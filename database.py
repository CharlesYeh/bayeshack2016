import MySQLdb
import os


db = MySQLdb.connect(
    user='dbherokuu',
    passwd=os.environ['MYSQL_PASSWORD'],
    host=os.environ['MYSQL_HOST'],
    db='dbherokuu')


def get_cursor():
    return db.cursor()
