import pymysql
import datetime

from pydantic import BaseModel

class UserAccess(BaseModel):
    id: str
    username: str
    sitename: str

class Register(BaseModel):
    id: str
    username: str
    email: str
    password: str

class Job(BaseModel):
    id: str
    title: str
    description: str
    minsalary: str
    maxsalary: str

class Employee(BaseModel):
    id: str
    name: str
    birth: str
    position: str
    salary: str

class Access(BaseModel):
    id: str
    username: str
    sitename: str
    accesstime: datetime.datetime

class Database(object):

    def __init__(self, user, password, host, database):

        self.user = user
        self.password = password
        self.host = host
        self.database = database

        self.conn = pymysql.connect(user='root', passwd='test-kamal', host='34.69.151.13', database='test', autocommit=True, cursorclass=pymysql.cursors.DictCursor)
        self.conn.autocommit = True
        self.cur = self.conn.cursor()

    def insert(self, insert_model, table_name):
        insert_model = insert_model.dict()
        columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in insert_model.keys())
        values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in insert_model.values())
        sql = "INSERT INTO %s ( %s ) VALUES ( %s );" % (table_name, columns, values)

        # print(sql)

        try:
            self.cur.execute(sql)
            return True

        except Exception as e:
            print(f"Error during executing pymysql : {e}")
            return False

    def query(self, sql):

        print(sql)

        try:
            self.cur.execute(sql)
            get_data = self.cur.fetchall()
            # print(get_data)

            if get_data:
                # print(f"there is a data")
                return {
                    "data": get_data,
                    "status": True
                }
            else:
                # print("There is no data")
                return {
                    "data": [],
                    "status": False
                }

        except Exception as e:
            print(f"Error during executing pymysql : {e}")
            return False