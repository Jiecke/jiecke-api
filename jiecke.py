import flask
from template import Template
from flask import request, jsonify, make_response
import time
import os
import yaml


with open('./config.yml','rb') as f:
    config = yaml.safe_load(f)
    photo_dir = config['photo_path']

server = flask.Flask(__name__)

@server.route('/ping', methods=['get'])
def ping():
    return jsonify({"code": "1", "msg": "success", "data": "pong"})


@server.route('/', methods=['post'])
def convert():
    upload_image = request.files.get('image')
    type = request.form.get('type')
    print(type)
    if upload_image is None:
        return jsonify({"code": "-1", "msg" : "图片上传失败，请重新上传!", "data" : ""})

    upload_path = os.path.join(photo_dir, str(int(time.time())))
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
    file_path = os.path.join(upload_path, upload_image.filename)
    upload_image.save(file_path)
    t = Template(type, file_path)
    res_img_path = t.synthetic()
    image_data = open(res_img_path, "rb").read()
    response = make_response(image_data)
    response.headers['Content-Type'] = 'image/png'
    return response

if __name__ == '__main__':
    server.run(host='0.0.0.0', port=8080, debug=True)