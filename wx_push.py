import requests, json

__author__ = 'chengxinyao'


class PushWxMsg(object):
    def __init__(self, appID, appsecret, template_id):
        self.appID, self.appsecret = appID, appsecret
        self.get_token_api = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'.format(
            self.appID, self.appsecret)
        self.access_token = self.get_access_token()
        self.template_id = template_id
        self.msg_data = {
            "first": {
                "value": "恭喜你购买成功！",
                "color": "#173177"
            },
            "product": {
                "value": "巧克力",
                "color": "#173177"
            },
            'order_id': {
                "value": "100001",
                "color": "#173177"

            },
            "pay_money": {
                "value": "39.8元",
                "color": "#173177"
            },
            "order_time": {
                "value": "2014年9月22日",
                "color": "#173177"
            },
            "remark": {
                "value": "欢迎再次购买！",
                "color": "#173177"
            }
        }

    def get_access_token(self):
        '''
        :return: 微信接口返回的合法token
        '''
        access_token = requests.get(self.get_token_api).json()['access_token']
        return access_token

    def get_openids(self):  # 获取用户列表
        '''
        :return: 获取公众号关注列表
        '''
        url = 'https://api.weixin.qq.com/cgi-bin/user/get?access_token=%s&next_openid=' % str(self.access_token)
        openids = requests.get(url).json()['data']['openid']
        return openids

    def push_msg(self, template_id, openids, msg_data):
        template = """\
共推送成功{}次:
openids:\n
{}
"""
        success = 0
        for openid in openids:
            post = {
                "touser": openid,
                "template_id": template_id,
                "data": msg_data
            }
            url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}'.format(self.access_token)
            result = requests.post(url, data=json.dumps(post)).json()
            success += 1
        ids = [str(i + 1) + '用户:' + id for i, id in enumerate(openids)]
        result = template.format(success, '\n'.join(ids))

        return result

    def run(self):
        openids = self.get_openids()
        result = self.push_msg(self.template_id, openids, self.msg_data)
        return result


if __name__ == '__main__':
    appID, appsecret = '你的appID', '你的appsecret'
    template_id = '你的template_id'
    p = PushWxMsg(appID, appsecret, template_id)
    result = p.run()
    print(result)

