import urllib.request
import json
import csv

# 发送HTTP请求并获取响应
url = "https://raw.githubusercontent.com/PlexPt/awesome-chatgpt-prompts-zh/main/prompts-zh.json"
response = urllib.request.urlopen(url)
data = json.loads(response.read().decode())

# 写入CSV文件
with open('data.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['act', 'prompt'])
    writer.writeheader()
    for item in data:
        writer.writerow(item)
