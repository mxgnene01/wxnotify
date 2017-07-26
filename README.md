# 验证码服务启动方法

wxnotify-server --logging_config=/Users/Daling/mxg/git/qa/wxnotify/etc/beta/logging.conf --config_file=/Users/Daling/mxg/git/qa/wxnotify/etc/beta/wxnotify.conf

## 部署分支

int

# 验证码生成服务使用方法

## 生成验证码

API调用：/api/v1/captcha/image
返回值：
 - token: 用于验证用户输入的 token
 - redirect_uri: 验证码图片地址

范例：
```
$ http POST http://127.0.0.1:8000/api/v1/captcha/image
HTTP/1.1 200 OK
Content-Length: 173
Content-Type: application/json; charset=UTF-8
Date: Tue, 19 Jul 2016 10:25:13 GMT
Server: TornadoServer/4.4

{
    "redirect_uri": "http://127.0.0.1:8000/api/v1/captcha/image/4743a13e5fa5ad9fe97e62c8020a949d8be9eb38.png",
    "status": 0,
    "token": "4743a13e5fa5ad9fe97e62c8020a949d8be9eb38"
}

```

## 验证用户输入

API调用: /api/v1/captcha/image/[token]/[code]

其中：

- [token] 为生成验证码接口返回的 token
- [code] 为用户输入的 code

返回值:

当HTTP CODE为200时：
- validate 为 1 表示验证成功，validate 为 0 表示验证失败

当HTTP CODE为404时：
查询的 TOKEN 过期或者不存在

范例:
```
http GET http://127.0.0.1:8000/api/v1/captcha/image/4743a13e5fa5ad9fe97e62c8020a949d8be9eb38/1234
HTTP/1.1 200 OK
Content-Length: 28
Content-Type: application/json; charset=UTF-8
Date: Tue, 19 Jul 2016 10:26:26 GMT
Etag: "d3699d6b8511f42b9c752b05aa6539bbf26adaf7"
Server: TornadoServer/4.4

{
    "status": 0,
    "validate": 0
}
```


## 其他

验证码过期时间默认为 60s


# 短信验证码

## 获取验证码

API调用: http://127.0.0.1:8000/api/v1/captcha/text/[mobile]

其中:
mobile 为客户手机号

返回值：
 - token: 用于验证用户输入的 token

例如：
```
http POST http://127.0.0.1:8000/api/v1/captcha/text/13800138000

HTTP/1.1 200 OK
Content-Length: 159
Content-Type: application/json; charset=UTF-8
Date: Tue, 19 Jul 2016 12:45:33 GMT
Server: TornadoServer/4.4

{
    "status": 0,
    "token": "c3a93b382ca04e1aa8eabd5bf5611595"
}
```

达令家 短信
```
http POST "http://captcha.beta.daling.com/api/v1/captcha/text/18988888888" 'caller=dalingjia'

HTTP/1.1 200 OK
Connection: keep-alive
Content-Length: 58
Content-Type: application/json; charset=UTF-8
Date: Wed, 19 Jul 2017 08:43:16 GMT
Server: Tengine/2.1.0

{
    "status": 0,
    "token": "9168ff12b6ac4685bdbf19395bd90fbb"
}
```


## 校验验证码
API调用: /api/v1/captcha/text/[token]/[code]
其中：

- [token] 为生成验证码接口返回的 token
- [code] 为用户输入的 code

返回值:

当HTTP CODE为200时：
- validate 为 1 表示验证成功，validate 为 0 表示验证失败

e.g.,
```
http GET http://127.0.0.1:8000/api/v1/captcha/text/4743a13e5fa5ad9fe97e62c8020a949d8be9eb38/123456
HTTP/1.1 200 OK
Content-Length: 28
Content-Type: application/json; charset=UTF-8
Date: Tue, 19 Jul 2016 10:26:26 GMT
Etag: "d3699d6b8511f42b9c752b05aa6539bbf26adaf7"
Server: TornadoServer/4.4

{
    "status": 0,
    "validate": 1
}
```
