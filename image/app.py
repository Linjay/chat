from flask import Flask, request, jsonify, send_from_directory, render_template
import os

app = Flask(__name__)

# 配置图片目录
image_dir = r'D:\programs\sd-webui-aki\output-bak'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_images', methods=['GET'])
def get_images():
    start = int(request.args.get('start', 0))
    num = int(request.args.get('num', 20))
    images = os.listdir(image_dir)
    images = images[start:start + num]
    has_more = len(images) == num
    return jsonify({'images': images, 'hasMore': has_more})


@app.route('/image/<path:image_name>')
def image(image_name):
    return send_from_directory(image_dir, image_name)


if __name__ == '__main__':
    app.run("0.0.0.0", port=5001, debug=True)
