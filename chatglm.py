import json
from flask import Flask, request
import requests
import urllib3

urllib3.disable_warnings()
requests.adapters.DEFAULT_RETRIES = 3
s = requests.Session()
s.keep_alive = False
s.verify = False
urllib3.disable_warnings()
app = Flask(__name__)

chat_holder = {
    "cid5Jo6E9HFyq9h53OKZLga0Q==": {
        "history": [],
        "dingToken": "6aa3cf223f652ff19d48518f9fdd7f7970def822e19a4f30557c6d05d75fbe16"
    },
    "cidbRFEZ6AtbzXd/9vjVZpLFw==": {
        "history": [],
        "dingToken": "0551bff6504ccab407014fc4d8a84c6e8657609f17668fce2c05e2828a903122"
    },
    "cid3woGpG5a4GbH/U88zZVH+w==": {
        "history": [],
        "dingToken": "6d796eac1cb8ee7affe06743871a2157c48251149236fa97d53cea2c95787a84"
    },
    "cid8JjMaf/ULHoPeXK/98cTaw==": {
        "history": [],
        "dingToken": "70caf994a77d482e6842a549ff941cda3b17433636923cbb9feee19a4910d8c1"
    }
}


@app.route("/")
def hi():
    return "<p>hi!</p>"


@app.route("/webhook/event", methods=['POST'])
def event():
    global chat_holder
    headers = {'Content-Type': 'application/json'}
    json_data = json.loads(request.data)
    print(json_data)
    asker = json_data['senderNick']
    conversation_id = json_data['conversationId']
    content = json_data['text']['content']
    if content == " clear":
        chat_holder[conversation_id]['history'] = []
        headers2 = {'Content-Type': 'application/json'}
        json_bot_msg = {"msgtype": "text", "text": {
            "content": asker + "你好!\r\n对话清理成功\r\nconversation:" + str(
                len(chat_holder[conversation_id]['history']))}}
        url = 'https://oapi.dingtalk.com/robot/send?access_token=' + chat_holder[conversation_id]['dingToken']
        requests.post(url, headers=headers2, json=json_bot_msg)
    if content.startswith(' bind:'):
        token = content.split(":", 1)[1]
        chat_holder[conversation_id] = {
            "history": [],
            "dingToken": token
        }
        with open("chatglm.ini", 'w') as f:  # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
            f.write(json.loads(chat_holder))
        headers2 = {'Content-Type': 'application/json'}
        json_bot_msg = {"msgtype": "text", "text": {
            "content": asker + "你好!\r\nconversation_id:" + conversation_id + "已绑定token:"+token+"\r\nconversation:" + str(
                len(chat_holder[conversation_id]['history']))}}
        url = 'https://oapi.dingtalk.com/robot/send?access_token=' + chat_holder[conversation_id]['dingToken']
        requests.post(url, headers=headers2, json=json_bot_msg)
    elif conversation_id not in chat_holder.keys():
        print("invalid conversation:" + conversation_id)
        headers2 = {'Content-Type': 'application/json'}
        json_bot_msg = {"msgtype": "text", "text": {
            "content": asker + "你好!\r\nconversation_id:"+conversation_id+",会话未初始化\r\nconversation:" + str(
                len(chat_holder[conversation_id]['history']))}}
        url = 'https://oapi.dingtalk.com/robot/send?access_token=' + chat_holder[conversation_id]['dingToken']
        requests.post(url, headers=headers2, json=json_bot_msg)
    else:
        json_message = {
            "history": chat_holder[conversation_id]['history'],
            "prompt": content,
            "max_length": 20480
        }
        print("send message to gpt")
        print(json_message)

        answer = ""
        try:
            chatgpt_response = requests.post('http://192.168.50.185:8000', headers=headers, json=json_message, proxies={})
            print("chatgpt_response:")
            print(chatgpt_response.json())
            answer = chatgpt_response.json()['response']
            chat_holder[conversation_id]['history'] = chatgpt_response.json()['history']

            print("----" * 20)
            print(answer)
            print("----" * 20)
        except:
            answer += "我好像找不到我的模型了。。。呜呜呜，请联系我的主人帮我开下机，谢谢！"
            print("An exception occurred")

        headers2 = {'Content-Type': 'application/json'}
        json_bot_msg = {"msgtype": "text", "text": {
            "content": asker + "你好!\r\n" + answer + '\r\nconversation:' + str(
                len(chat_holder[conversation_id]['history']))}}
        url = 'https://oapi.dingtalk.com/robot/send?access_token=' + chat_holder[conversation_id]['dingToken']
        response = requests.post(url, headers=headers2, json=json_bot_msg)
        print(response.text)

        if len(chat_holder[conversation_id]['history']) > 50:
            chat_holder[conversation_id]['history'] = []
    return 'conversation这只是一个回复'

if __name__ == '__main__':
    with open('chatglm.ini') as f:  # 默认模式为‘r’，只读模式
        contents = f.read()  # 读取文件全部内容
        print(contents)  # 输出时在最后会多出一行（read()函数到达文件末会返回一个空字符，显示出空字符就是一个空行）
        print('------------')

        # check data type with type() method
        print(type(contents))

        # convert string to  object
        chat_holder = json.loads(contents)

        # check new data type
        print(type(chat_holder))

    print("program loading")
    app.run(host='0.0.0.0', port=18888, debug=True)
    print("program exit()")
