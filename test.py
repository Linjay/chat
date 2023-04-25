# 创建一个flash app 程序

# 导入Flask类
import flask

# 创建一个Flask类的实例
app = flask.Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/hello', methods=['GET'])
def hello():
    name = "aaa"
    #  获取请求参数
    name = flask.request.args.get('name')
    return 'Hello!' + name

# 对一个字符串列表进行首字母排序
def sort_list(string_list):
    return sorted(string_list)

if __name__ == '__main__':
    app.run("0.0.0.0", 5000)