# 服务器端已知问题

## 1. `AI绘画`少数情况下返回结果为空

少数情况下，nv服务器返回以下内容：

```
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>500 Internal Server Error</title>
<h1>Internal Server Error</h1>
<p>The server encountered an internal error and was unable to complete your request.  Either the server is overloaded or there is an error in the application.</p>
```

推测应该是远端服务器内部错误

临时解决方案：尝试重新生成结果



## 2. 多数API仅支持单用户访问

# 运行所需的额外要求

## 程序

bash, curl, v2ray

## 代理
http_proxy='127.0.0.1:8889'
https_proxy='127.0.0.1:8889'
