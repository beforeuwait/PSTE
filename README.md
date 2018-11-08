# 最高院失信被执行人查询api使用说明

## 日志

- 2018-09-29:

完成验证码模块的开发,验证码图片不做保存处理，直接在线ocr

- 2018-10-25：

拖了蛮久来进行收尾

这期间在重新做一版ocr

用的挺老的svm方法

重新部署上线，spider方面的代码没有改动

- 2018-10-29

迭代验证码部分，在线上服务器会遇到下载验证码过慢的问题

之前队列里只放1个ocr的思路就行不通了

new idea：在2mins内，队列保持10个ocr结果，同时调用端也保持FIFO的原则

- 2018-11-05

**接口在周末不能用，经检查发现，网站服务器性能差，打不开，验证码加载慢** 

## 注意:

代理部分，本人使用的阿布云(已屏蔽)

**需手动去配置**
> 目标:
    
搭建一个server，提供在线的查询，通过输入的人的名字和身份证号

返回:

1. 被执行人查询结果
2. 失信被执行人查询结果
3. 百度api返回被执行人查询结果

## 模块

- 验证码模块
	- 实时获取最新验证码并ocr
- http-server
	- 提供api服务
- spider
	- 失信被执行数据抓取
	- 被执行人数据抓取
	- 百度api的被执行人数据抓取


## 如何使用
部署地址:

		http:118.123.201.169:23080/pste2

1. 首先启动验证码识别模块
	
		每次去下载2个最新的验证码
		在线实时图片识别
		然后丢入队列里
		
		终端:
			先启动 redis
			python3 CaptchaHandler.py
	
2. 启动一个http-server 作为api
		
		终端:
			python3 PSTEWebServer.py
		监听端口自定义

3. 该api的调用

		
		请求(以本地为例):
		http://localhost:xxxx/pste2
		
		方法: POST
		参数: {
				'pname': 'xxx',
				'cardNum': 'xxxxxxxxxxxx'
				}
				
		接口返回参数格式:{
		        "api_status_code": 200,
		        "api_msg": [],
		        "api_status": "success",
		        "data": {
		            'zhixing': {
		                'info': [],
		                'status': 200
		            },
		            'shixin': {
		                'info': [],
		                'status': 200
		            },
		            'baidu': {
		                'info': [],
		                'status': 200
		            }
		       	}
		    }