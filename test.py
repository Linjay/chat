import json

chat_holder = {}

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


    print('2------------')
    str = json.dumps(chat_holder)
    print(str)
