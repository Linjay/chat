from transformers import AutoTokenizer, AutoModel
tokenizer = AutoTokenizer.from_pretrained("D:\programs\chatglm\chatglm-6b-model", trust_remote_code=True)
model = AutoModel.from_pretrained("D:\programs\chatglm\chatglm-6b-model", trust_remote_code=True).half().cuda()
model = model.eval()
response, history = model.chat(tokenizer, "你好", history=[])
print(response)
response, history = model.chat(tokenizer, "晚上睡不着应该怎么办", history=history)
print(response)
