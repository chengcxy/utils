
__author__ = 'chengxinyao'


import asyncio
import asyncio.queues as queue
import aiohttp

"""
python3.6
asyncio aiohttp  协程异步方式 请求api接口
"""


class AsyncCheckApi(object):
    def __init__(self,urls,worker_nums):
        self.urls = urls
        self.worker_nums = worker_nums
        self.q = queue.Queue()

    async def producer(self,url):#url放进队列
        await self.q.put(url)

    async def consumer(self):#消费队列+回调异步请求
        try:
            url = await self.q.get()
            print(url)
            response = await self.request(url)
            #其他异步函数继续
            print(response)
        finally:
            self.q.task_done()

    async def request(self,url):#异步请求函数
        response = None
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    response = await resp.json()
        except Exception as e:
            print('url:{} 请求异常'.format(url,e))
        finally:
            return response


    async def worker(self):#回调消费者函数
        while not self.q.empty():
            await self.consumer()


    async def run(self):#调度函数 生产队列/消费队列
        for url in self.urls:
            await self.producer(url)
        for num in range(self.worker_nums):
            await self.worker()
        await self.q.join()



def main(urls,worker_nums):
    obj = AsyncCheckApi(urls,worker_nums)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(obj.run())


if __name__ == '__main__':
    base_url = ' http://*****/api/v1?func_name='
    func_names = ['get_com_users', 'get_activate_users', 'get_invoice_num', 'get_efficiency',
                  'get_company_economic_tops',
                  'get_industry_social_tops', 'get_user_distribution_province', 'get_user_distribution_city',
                  'get_environment_contribution', 'get_bw_cloud_contribution', 'get_compliance_inspection_num',
                  'get_tax_risk_intelligence_num', 'get_detected_tax_risks_num', 'get_tax_income_rate',
                  'get_tax_costs_amount_rate',
                  'get_tax_bear_area', 'get_tax_bear_area_tops', 'get_tax_bearing_rate', 'get_tax_night',
                  'get_ecological_com_tops',
                  'get_drift_contribution', 'get_xh_gh_sales', 'get_e_drift_heat', 'get_e_drift_source_target'
                  ]
    urls = [base_url + i for i in func_names]
    worker_nums = 10 #起多少worker消费队列里数据
    main(urls,worker_nums)
"""
输出内容
 http://*****/api/v1?func_name=get_com_users
{'data': {'get_com_users': 81000}, 'msg': '获取数据成功', 'success': True}
http://*****/api/v1?func_name=get_activate_users
{'data': {'get_activate_users': 23786}, 'msg': '获取数据成功', 'success': True}
http://*****/api/v1?func_name=get_invoice_num
{'data': {'get_invoice_num': 800000000}, 'msg': '获取数据成功', 'success': True}
:::
"""
