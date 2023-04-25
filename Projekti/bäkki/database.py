import mysql.connector


class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
                 host="mysql.metropolia.fi",
                 port= 3306,
                 database="lucasla",
                 user="lucasla",
                 password="1234",
                 autocommit=True
                 )
    def get_conn(self):
        return self.conn