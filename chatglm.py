import json
from flask import Flask,request
import requests
import urllib3
import time

urllib3.disable_warnings()
requests.adapters.DEFAULT_RETRIES = 3
s = requests.Session()
s.keep_alive = False
s.verify = False
urllib3.disable_warnings()
app = Flask(__name__)

chatgpt_conversation=[]

@app.route("/")
def hi():
    return "<p>hi!</p>"

@app.route("/webhook/event",methods=['POST'])
def event():
    global chatgpt_conversation
    proxies={'http':'http://192.168.50.4:7890','https':'https://192.168.50.4:7890'}
    headers={'Content-Type': 'application/json','Authorization': 'Bearer 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'}
    json_data=json.loads(request.data)
    print(json_data)
    chatgpt_conversation.append({"role": "user", "content": json_data['text']['content']})
    json_message={
    "model": "gpt-3.5-turbo",
    "messages": chatgpt_conversation}
    print("send message to gpt")
    print(json_message)
    chatgpt_response=requests.post('https://api.openai.com/v1/chat/completions',headers=headers,json=json_message,proxies={})
    print("chatgpt_response:")
    print(chatgpt_response)
    chatgpt_conversation.append(chatgpt_response.json()['choices'][0]['message'])
    answer=chatgpt_response.json()['choices'][0]['message']['content']
    print("----"*20)
    print(answer)
    print("----"*20)
    headers2={'Content-Type':'application/json'}
    json_sendmessages={"msgtype": "text","text": {"content":answer+'\r\nconversation:'+str(len(chatgpt_conversation))}}
    url='https://oapi.dingtalk.com/robot/send?access_token=6aa3cf223f652ff19d48518f9fdd7f7970def822e19a4f30557c6d05d75fbe16'
    response=requests.post(url,headers=headers2,json=json_sendmessages)
    print(response.text)
    if len(chatgpt_conversation)>16:
        chatgpt_conversation=[]
    return 'conversation这只是一个回复'
@app.route("/webhook/images",methods=['POST'])
def images():
    proxies={'http':'http://192.168.50.4:7890','https':'https://192.168.50.4:7890'}
    headers={'Content-Type': 'application/json','Authorization': 'Bearer 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'}
    json_data=json.loads(request.data)
    print(json_data['text']['content'])
    json_message={
    "prompt": json_data['text']['content'],
    "n": 1,
    "size": "1024x1024"}
    chatgpt_response=requests.post('https://api.openai.com/v1/images/generations',headers=headers,json=json_message,proxies={})
    json_data['text']['content']=chatgpt_response.json()['data'][0]['url']
    print("----"*20)
    print(chatgpt_response.json()['data'][0]['url'])
    print("----"*20)
    return json_data
if __name__ == '__main__':
    print("program loading")
    app.run(host='0.0.0.0',port=18888,debug=True)
    print("program exit()")