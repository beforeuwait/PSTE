# PSTE第二版

## 根据最高院网页改版，顺带迭代了一版该接口

### 改动

1. 不再请求百度的被执行人接口

2. 简化了 被执行人和失信被执行人 代码，便于维护

3. 验证码部分，增加了验证部分，每次ocr后都要对改结果进行验证

4. 不再对请求结果予以保存

5. 不再保存CaptchaId,每次都用鲜活的


## 启动

    1. 先启动redis
    > redis-server
    
    2. 启动验证码模块
    nohup python3 CaptchaHandler.py &
    
    3. 启动web服务
    nohup python3 PSTEWebServer.py
    

## 说明

- 该接口不做任何参数验证，由调用接口前端去完成(偷懒ing)

- 务必上代理，虽说还是可能被反向解析出

- 带cookie测试过程会出现js加载cookie 的部分，目前没有影响，不过也是个隐患