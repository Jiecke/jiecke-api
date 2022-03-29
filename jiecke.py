import flask
from PIL import Image
from template import Template
from flask import request, jsonify, make_response
import time
import os
import yaml


with open('./config.yml','rb') as f:
    config = yaml.safe_load(f)
    photo_dir = config['photo_path']

server = flask.Flask(__name__)

def responseUtil(code, msg) :
    return jsonify(
        {
            "code": "-1", 
            "msg" : msg
        }
    )

@server.route('/ping', methods=['get'])
def ping():
    return jsonify({"code": "1", "msg": "success", "data": "pong"})


# 转换图片格式
def transImg(img_path):
    strs = img_path.rsplit(".", 1)
    if(len(strs) > 1 and (strs[1] == "png" or strs[1] == "PNG")):
        return img_path
    output_img_path = strs[0] + ".png"
    print(output_img_path)
    im = Image.open(img_path)
    try:
        im.save(output_img_path)
        return output_img_path
    except:
        return ""


# 保存图片
def saveImage(upload_image):
    upload_path = os.path.join(photo_dir, str(int(time.time())))
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
    file_path = os.path.join(upload_path, upload_image.filename)
    upload_image.save(file_path)
    # 图片格式转换
    file_path = transImg(file_path)
    return file_path


@server.route('/', methods=['post'])
def convert():
    # 获取参数
    machine_type = request.form.get('type')
    upload_image = request.files.get('image')
    if upload_image is None:
        return responseUtil(-1, "图片上传失败，请重新上传!")

    # 存储图片，返回path
    file_path = saveImage(upload_image)
    if file_path == "":
        return responseUtil(-1, "图片不合法")

    # 图片套壳
    t = Template(machine_type, file_path)
    res_img_path = t.synthetic()

    # 返回图片
    image_data = open(res_img_path, "rb").read()
    response = make_response(image_data)
    response.headers['Content-Type'] = 'image/png'
    return response

if __name__ == '__main__':
    server.run(host='0.0.0.0', port=8080, debug=True)