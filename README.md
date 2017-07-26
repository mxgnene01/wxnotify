# 微信报警

## 说明

接入微信服务号发送报警使用

### 安装

```shell
make install
```

### 启动

```shell
wxnotify-server --logging_config=/Users/Daling/mxg/git/qa/wxnotify/etc/beta/logging.conf --config_file=/Users/Daling/mxg/git/qa/wxnotify/etc/beta/wxnotify.conf
```

## 服务号后台配置

在微信管理后台基本配置处修改 `服务器地址(URL)` 为外网能访问的的域名地址：http://domain/api/wechat/msg

## 绑定

- 关注的微信服务号
- 绑定：输入 bind:手机号
- 解绑： unbind

## 发送报警

```shell
http "http://domain/api/push/byusername?user_names=18988888881,18988888888&title=达令监控报警&machine=yadmin3&moniterkey=监控项&state=服务状态&output=监控输出&remark=注释&url=www.baidu.com"
```

### 参数说明

- user_names: 支持多手机号发送相同的报警，用逗号分隔
- title：报警的标题，不传默认为 '公司监控报警通知'
- machine： 报警机器
- moniterkey： 监控项，如：api/home/hotsale time > 10
- state: 服务状态 ，如 ERROR，WARN，INFO
- output：监控输出
- remark：注释
- url: 点击消息跳转的链接

### 返回

只要多个手机号中有一个发送成功即返回成功

```json
{
    "code": 0,
    "original": {
        "errcode": 0,
        "errmsg": "ok",
        "msgid": 412392410
    }
}
```

发送失败

```json
{
    "code": 5003,
    "reason": "push notify hash error"
}
```