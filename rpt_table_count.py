
import pymysql ,os ,json ,time ,hashlib




class RptTable(object):

    def __init__(self, mode='test'):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file = os.path.join(base_dir, 'config.json')
        self.mode = mode
        with open(file) as fr:
            self.config = json.load(fr)[self.mode]
        self.conn = pymysql.connect(**self.config)
        self.cursor = self.conn.cursor()

    def get_table_dim(self):
        query = 'select table_name,table_comment,table_type from dim_table'
        return self.get_data(query)

    def save(self ,values ,table):
        for value in values:
            fields = list(value.keys())
            _fields  = ','.join(fields)
            _str = ','.join(['%s' for i in fields])
            base_sql = 'insert into {table}({_fields}) values({_str})'
            sql = base_sql.format(table=table ,_fields=_fields ,_str=_str)
            data = [value[i] for i in fields]
            self.cursor.execute(sql ,data)
            self.conn.commit()

    def get_data(self ,sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_md5(self ,value):
        md5 = hashlib.md5()
        _str = ''.join(value)
        md5.update(_str.encode())
        return md5.hexdigest()

    def count_dim(self):
        sql = 'select db,table_name,column_name,column_comment from spider.dim_column'
        datas = self.get_data(sql)
        values = []
        base_sql = 'select count(1) as total_count,sum(if({column_name} is not null,1,0)) as not_null_count,sum(if({column_name} is null,1,0)) as null_count from {db}.{table_name}'
        for db ,table_name ,column_name, column_comment in datas:
            sql = base_sql.format(column_name=column_name ,table_name=table_name ,db=db)
            print(sql)
            total_count ,not_null_count ,null_count = self.get_data(sql)[0]
            item = {}
            item['db'] = db
            item['table_name'] = table_name
            item['column_name'] =column_name
            item['column_comment'] = column_comment
            item['total_count'] = total_count
            item['not_null_count'] = not_null_count
            item['not_null_rate'] = str(
                round(not_null_count / total_count * 100, 2)) + '%' if total_count and not_null_count else '0.00%'
            item['null_rate'] = str(
                round(null_count / total_count * 100, 2)) + '%' if total_count and null_count else '0.00%'
            item['null_count'] = null_count
            item['create_date'] = time.strftime("%Y-%m-%d", time.localtime())
            item['create_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            values.append(item)
        if values:
            self.save(values, table='rpt_dim_count')

    def count_table(self):
        base_sql = 'select count(1) from spider.{table_name}'
        datas = self.get_table_dim()
        values = []
        for table_name, table_comment, table_type in datas:
            sql = base_sql.format(table_name=table_name)
            print(sql)
            item = {}
            item['table_name'] = table_name
            item['table_comment'] = table_comment
            item['table_type'] = table_type
            count = self.get_data(sql)[0]
            item['count'] = count
            create_date = time.strftime("%Y-%m-%d", time.localtime())
            item['create_date'] = create_date
            item['create_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            values.append(item)
        if values:
            self.save(values, table='rpt_table_count')

    def run(self):
        self.count_table()
        self.count_dim()


if __name__ == '__main__':
    r = RptTable()
    r.run()



