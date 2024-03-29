import json
from flask import Flask, request
import requests
import urllib3
import logging

urllib3.disable_warnings()
requests.adapters.DEFAULT_RETRIES = 3
s = requests.Session()
s.keep_alive = False
s.verify = False
urllib3.disable_warnings()
app = Flask(__name__)

logger = logging.getLogger()
fh = logging.FileHandler('chatglm-main.log', encoding='utf-8', mode='a')
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.setLevel(logging.DEBUG)

headers_ask = {'Content-Type': 'application/json'}

# 全局的会话存储
chat_holder = {}

# 全局的配置文件存储路径
config_path = "chatglm.ini"


@app.route("/")
def hi():
    return "<p>hi!</p>"


# 加载配置文件
def load_config():
    global chat_holder
    with open(config_path) as f:  # 默认模式为‘r’，只读模式
        contents = f.read()  # 读取文件全部内容
        logging.warning(contents)  # 打印文件内容
        logging.warning('------------')

        # convert string to  object
        chat_holder = json.loads(contents)  # 将字符串转换为字典
        logging.warning(chat_holder)  # 打印字典


# outing request
@app.route("/webhook/event", methods=['POST'])
def event():
    global chat_holder, headers_ask
    json_data = json.loads(request.data)
    logging.warning(json_data)
    asker = json_data['senderNick']
    conversation_id = json_data['conversationId']
    content = json_data['text']['content']
    if content == " clear":  # clear
        chat_holder[conversation_id]['history'] = []
        send_msg(conversation_id, asker, "对话清理成功")
    elif content.startswith(' bind:'):  # bind:token
        token = content.split(":", 1)[1]
        chat_holder[conversation_id] = {
            "history": [],
            "dingToken": token
        }
        with open(config_path, 'w') as f:  # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
            f.write(json.dumps(chat_holder, indent=2))
        send_msg(conversation_id, asker, "conversation_id:" + conversation_id + "\r已绑定token:" + token)
    elif conversation_id not in chat_holder.keys():  # 未初始化
        send_msg(conversation_id, asker, "conversation_id:" + conversation_id + ",会话未初始化")
    else:  # chat with chat-glm
        json_message = {
            "history": chat_holder[conversation_id]['history'],
            "prompt": content,
            "max_length": 20480
        }
        logging.warning("send message to gpt")
        logging.warning(json_message)

        answer = ""
        try:
            chatgpt_response = requests.post('http://192.168.50.30:8000', headers=headers_ask, json=json_message,
                                             proxies={})
            logging.warning("chatgpt_response:")
            logging.warning(chatgpt_response.json())
            answer = chatgpt_response.json()['response']
            chat_holder[conversation_id]['history'] = chatgpt_response.json()['history']

            logging.warning("----" * 20)
            logging.warning(content)
            logging.warning("----" * 20)
            logging.warning(answer)
            logging.warning("----" * 20)
        except Exception as ex:
            answer += "哎呀，崩溃啦。。。呜呜呜，请联系我的主人吧！\r\n" + str(ex)
            logging.warning("An exception occurred", ex)

        send_msg(conversation_id, asker, "" + answer)

        if len(chat_holder[conversation_id]['history']) > 50:
            chat_holder[conversation_id]['history'] = []

    return 'conversation:done'


def send_msg(conversation_id, asker, msg):
    global chat_holder
    logging.warning("----" * 20)
    logging.warning("send msg to " + conversation_id + ", msg:\r\n" + msg)
    logging.warning("----" * 20)

    headers_ding = {'Content-Type': 'application/json'}
    json_bot_msg = {
        "msgtype": "text",
        "text": {
            "content": asker + " 你好!\r\n" + msg + "\r\n第" + str(len(chat_holder[conversation_id]['history'])) + "轮conversation"
        }
    }
    url = 'https://oapi.dingtalk.com/robot/send?access_token=' + chat_holder[conversation_id]['dingToken']

    response = requests.post(url, headers=headers_ding, json=json_bot_msg)
    logging.warning(response.text)


if __name__ == '__main__':
    load_config()

    logging.warning("program loading")
    app.run(host='0.0.0.0', port=18888, debug=True)
    logging.warning("program exit()")
