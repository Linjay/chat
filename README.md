# chat


## 添加群自定义机器人

钉钉机器人的outing设置为：


```
http://linjay.asuscomm.com:18888/webhook/event
```


## 绑定机器人
添加机器人后

@机器人

```
@robot bind:${token}
```

<img width="679" alt="image" src="https://user-images.githubusercontent.com/4114248/233837892-48d1923c-31e2-4a6d-8849-7f3432bc73db.png">

绑定后的结果写入```chatglm.ini```

## 启动
```
chmod +x start.sh
./start.sh
```

## 日志
```
tail -300f chatglm.log
```

## 其他指令

### 清理对话

```
@robot clear
```

<img width="567" alt="image" src="https://user-images.githubusercontent.com/4114248/233837900-3ce48790-9a1f-4942-95a9-1583a4d24e74.png">
