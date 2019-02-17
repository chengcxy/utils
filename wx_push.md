## 微信公众号推送消息

## 开发流程
### 1.公众平台测试号 申请测试号的地址 微信扫描登录 获取 appID appsecret 用于获取access_token
> 地址：https://mp.weixin.qq.com/debug/cgi-bin/sandboxinfo?action=showinfo&t=sandbox/index

### 2.添加测试模板 获取模板id为微信接口必带参数
```
{{first.DATA}}
订单商品：{{product.DATA}}
订单编号：{{order_id.DATA}}
支付金额：{{pay_money.DATA}}
支付时间：{{order_time.DATA}}
{{remark.DATA}}
```

### 3.获取access_token
```
https请求方式: GET
接口地址:https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=你的appID&secret=你的appsecret

正常情况下，微信会返回下述JSON数据包给公众号：
{"access_token":"ACCESS_TOKEN","expires_in":7200}
```

### 4.携带token 调用发送模板消息
```
开发文档:https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1433751277
http请求方式: POST
接口地址:https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=ACCESS_TOKEN
```

参数说明

|参数|是否必填|说明
|:-----|:-----|:-----|
|touser|	是|	接收者openid
|template_id|	是|	模板ID
|data	|是	|模板数据
|color	|否	|模板内容字体颜色，不填默认为黑色

POST数据(json)示例如下：
```python
 {
    "touser":"OPENID",
    "template_id":"ngqIpbwh8bUfcSsECmogfXcV14J0tQlEpBO27izEYtY",
    "data": {
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
}
```
在调用模板消息接口后，会返回JSON数据包。正常时的返回JSON数据包示例：
```
{
  "errcode":0,
  "errmsg":"ok",
  "msgid":200228332
}
```





