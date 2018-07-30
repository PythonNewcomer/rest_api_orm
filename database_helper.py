from psycopg2 import connect
from json import dumps


class DatabaseHelper(object):

    def __init__(self, host, dbname, user, password):
        try:
            self.conn = connect(dbname=dbname, user=user, host=host, password=password)
        except:
            print("Connection failed!")

    def execute_script(self, script):
        cur = self.conn.cursor()
        cur.execute(script)
        self.conn.commit()

    def execute_select(self, script):
        cur = self.conn.cursor()
        cur.execute(script)
        rows = cur.fetchall()
        return rows

    def transform_dataset_into_json(self, result):
        list = []
        for row in result:
            dic = {}
            dic['id'] = row[0]
            dic['country'] = row[1]
            dic['continent'] = row[2]
            list.append(dic)
        return dumps(list)

    def transform_row_into_json(self, result):
        dic = {}
        try:
            row = result[0] # result returns list even if it consists of one tuple only
            dic['id'] = row[0]
            dic['country'] = row[1]
            dic['continent'] = row[2]
        except IndexError:
            dic['message'] = "Country Not Found"
        return dumps(dic)

    def close_connection(self):
        self.conn.close()
