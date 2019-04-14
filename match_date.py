import time


class Matchdate(object):
    """
    Match = Matchdate()
    import json
    print json.dumps(Match.to_match('2014-01-11','2014-08-22'))
    """

    def __init__(self, db_prefix=None):
        self.db_prefix = db_prefix
        if db_prefix is None:
            self.db_prefix = ''

    def getMonthDays(self, year, month):
        day = 31
        while day:
            try:
                time.strptime('%s-%s-%d' % (year, month, day), '%Y-%m-%d')
                return day
            except:
                day -= 1

    def fit_date_format(self, year, month):
        month = int(month) if str(month)[0] != 0 else int(str(month)[1::])
        if month < 10:
            str_db = self.db_prefix + "%s0%s" % (year, month)
        else:
            str_db = self.db_prefix + "%s%s" % (year, month)

        return str_db

    def get_str_month(self, month):
        month = int(month) if str(month)[0] != 0 else int(str(month)[1::])
        if month < 10:
            return '0' + str(month)
        return str(month)

    def get_start_end(self, year, month, start=None, end=None):
        _start = "%s-%s-01" % (year, self.get_str_month(month))
        _end = "%s-%s-%s" % (year, self.get_str_month(month), self.getMonthDays(year, month))
        if start:
            _start = start
        if end:
            _end = end
        return [_start, _end]

    def get_year_per_months(self, years):
        l = [[year, month] for month in range(1,13) for year in years]
        return l

    def join_year(self,l):
        ms = list(map(lambda x:str(x[0])+'0'+str(x[1]) if x[1]<10 else str(x[0])+str(x[1]),l))
        return ms

    def to_match(self, start, end):
        if int(start.replace('-','')) > int(end.replace('-','')):
            info = '开始日期:{}大于结束日期:{}'.format(start,end)
            raise Exception(info)
        _start = int(''.join(start.split('-')[:2]))
        _end = int(''.join(end.split('-')[:2]))
        dc = {}
        _start_year, _end_year = start.split('-')[0], end.split('-')[0]
        _start_month, _end_month = start.split('-')[1], end.split('-')[1]
        _start_year_months = list(map(str,range(_start, int(_start_year + '13'))))
        _end_year_months = list(map(str,range(int(_end_year + '01'), _end + 1)))
        count_year = int(_end_year) - int(_start_year)
        months = []
        if count_year:
            months = _start_year_months + _end_year_months
            if count_year >1:
                years = list(range(int(_start_year)+1,int(_end_year)))
                l = self.get_year_per_months(years)
                ms = self.join_year(l)
                months += ms
        else:
            months = [i for i in _start_year_months if i in _end_year_months]
        months = sorted(months)
        for d in months:
            year,month = d[:4],d[4::]
            dc[self.fit_date_format(year, month)] = self.get_start_end(year, month)
        if dc:
            dc[self.fit_date_format(_start_year,_start_month)][0] = start
            dc[self.fit_date_format(_end_year, _end_month)][-1] = end
        return dc



if __name__ == '__main__':
    match = Matchdate(db_prefix='buzz_v1_')
    str_db = match.fit_date_format(year='2019', month=11)
    print(str_db)
    dc = match.to_match('2013-04-11', '2017-04-11')
    for k,v in dc.items():
        print(k,v)
    g = words(10,common=True)
    print(g)