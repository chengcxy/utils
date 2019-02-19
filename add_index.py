
s = """\
1.xx_fplx_bi_count
	zz_bm、fplx、kpny
2.xx_fplx_month_count
	zz_bm、kpny、fplx、kp_year
3.xx_goods_base_month_count
	zz_bm、kpny、fplx、goods_type
4.xx_goods_count
	fplx、zz_bm、kpny、goods_type、zhsl
5.xx_goods_area_count
	fplx、zz_bm、kpny、goods_type
6.xx_ghdw_top_month_count
	fplx、zz_bm、kpny
7.xx_ghdw_gis_count
	fplx、zz_bm、kpny
8.xx_ghdw_month_count
	zz_bm、kpny
9.xx_hc_detail
	zz_bm、kpny
10.xx_hc_base_month_count
	zz_bm、kpny、fplx、kp_year、fp_type
"""


if __name__ == '__main__':
    tables  = []
    indexs = []
    for i in s.split('\n'):
        if '.' in i:
            tables.append(i.split('.')[-1])
        if '、' in i:
            indexs.append(i)
    item = dict(zip(tables,indexs))
    for k,v in item.items():
        indexlist = v.replace('\t','').split('、')
        l = []
        for j in indexlist:
            sql = 'alter table {k} add index {j}({j});'.format(k=k,j=j)
            l.append(sql)
        item[k] = '\n'.join(l)
    for k, v in item.items():
        print(v)