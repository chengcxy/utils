# coding:utf-8
import pymysql


class NoResultError(Exception):
    pass

class ObjectDict(dict):
    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError(r"'ObjectDict' object has no attribute '%s'" % attr)

    def __setattr__(self, attr, value):
        self[attr] = value


class Helper(object):
    def __init__(self, **kwargs):
        self.config = kwargs
        self.conn = pymysql.connect(**self.config)
        self.cursor = self.conn.cursor()

    def row_to_obj(self, row, cur):
        obj = ObjectDict()
        for val, desc in zip(row, cur.description):
            obj[desc[0]] = val
        return obj

    def execute(self, stmt, *args):
        self.cursor.execute(stmt, args)
        self.conn.commit()

    def query(self, stmt, *args):
        self.cursor.execute(stmt, args)
        return [self.row_to_obj(row, self.cursor) for row in self.cursor.fetchall()]

    def queryone(self, stmt, *args):
        results = self.query(stmt, *args)
        if len(results) == 0:
            raise NoResultError()
        elif len(results) > 1:
            raise ValueError("Expected 1 result, got %d" % len(results))
        return results[0]

    def any_object_exists(self,stmt, *args):
        return bool(self.query(stmt, *args))

    def close(self):
        self.cursor.close()
        self.conn.close()




if __name__ == '__main__':
    db = Helper(host='localhost',
                port=3306,
                user='root',
                password='密码',
                db='blog',
                charset='utf8' )
    sql = 'SELECT * FROM blogs'
    result = db.query(sql)
    is_exists = db.any_object_exists('select * from authors where email = %s',('458707811@qq.com'))
    print(is_exists)
    for item in result:
        print(item.title,item['title'],item.author)
    db.close()

