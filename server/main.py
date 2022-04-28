from operator import imod
from flask import Flask, redirect, request, send_file, render_template
import Algorithms
import numpy as np
import matplotlib as plt
import io
import sys

from flask_cors import CORS, cross_origin


app = Flask(__name__)
isUpload = False
isUpload2 = False
fileSourceName = ''
fileSourceName2 = ''

cors = CORS(app, supports_credentials=True)


# error codes
# 666:success
# -1:error
# -2:no image uploaded


@app.route('/')
def index():
    return {'log': 'Hello World!'}


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    print(request.form)
    if request.method == 'POST':
        print(request.files)
        f = request.files['the_file']

        try:
            fileExt = f.filename.split('.')[1]
            filepath = './data/' + 'source.' + fileExt
            f.save(filepath)

            global isUpload
            global fileSourceName
            isUpload = True
            fileSourceName = 'source.' + fileExt

            return redirect('http://127.0.0.1:5500/')

        except:
            return redirect('http://127.0.0.1:5500/')

    else:
        return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form action="" method=post enctype=multipart/form-data>
        <p><input type=file name=the_file>
        <input type=submit value=Upload>
        </form>
        '''


def return_img_stream(img_local_path):
    """
    工具函数:
    获取本地图片流
    :param img_local_path:文件单张图片的本地绝对路径
    :return: 图片流
    """
    import base64
    img_stream = ''
    img_local_path = './data/source.jpg'
    with open(img_local_path, 'r') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream)
    return img_stream

# 读取服务器本地图片


def getImage(filePath):
    import base64
    with open(filePath, 'rb') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream)
    return img_stream


def ImageReturn(filePath):
    f = getImage(filePath)
    # byte to JSON
    f = str(f, encoding='utf-8')
    f = f.replace('b\'', '').replace('\'', '')
    return f


@app.route('/source', methods=['POST', 'GET'])
def returnSource():
    import io
    if request.method == 'POST':

        fileJSON = ImageReturn('./data/' + fileSourceName)
        # res = app.make_response(data)
        # res.headers["Content-Type"] = "image/png"
        return {'msg': '666', 'file': fileJSON}
    else:
        return {'msg': '-1', 'file': 'No image uploaded'}


@app.route('/CannyDetect', methods=['POST', 'GET'])
def CannyDetect():
    if isUpload:
        req = Algorithms.CannyProcess(fileSourceName)
        fileJSON = ImageReturn(req['src'])
        if req['msg'] == '666':
            return {'msg': '666', 'file': fileJSON}
        else:
            return {'msg': '-1'}
    else:
        print('no image uploaded')
        return {'msg': '-2'}


@app.route('/HarrisDetect', methods=['POST', 'GET'])
def CornerDetect():
    if isUpload:
        req = Algorithms.HarrisProcess(fileSourceName)
        fileJSON = ImageReturn(req['src'])
        if req['msg'] == '666':
            return {'msg': '666', 'file': fileJSON}
        else:
            return {'msg': '-1'}
    else:
        return {'msg': '-2'}


@app.route('/SubPixDetect', methods=['POST', 'GET'])
def CornerDetect2():
    if isUpload:
        req = Algorithms.SubPixProcess(fileSourceName)
        fileJSON = ImageReturn(req['src'])
        if req['msg'] == '666':
            return {'msg': '666', 'file': fileJSON}
        else:
            return {'msg': '-1'}
    else:
        return {'msg': '-2'}


@app.route('/FaceDetect', methods=['POST', 'GET'])
def FaceDetectProcess():
    if isUpload:
        req = Algorithms.FaceDetect(fileSourceName)
        fileJSON = ImageReturn(req['src'])
        if req['msg'] == '666':
            return {'msg': '666', 'file': fileJSON}
        else:
            return {'msg': '-1'}
    else:
        return {'msg': '-2'}


@app.route('/uploadTarget', methods=['POST', 'GET'])
def upload2():
    print(request.form)
    if request.method == 'POST':
        print(request.files)
        f = request.files['the_file']

        try:

            fileExt = f.filename.split('.')[1]
            filepath = './data/' + 'target.' + fileExt
            f.save(filepath)

            global isUpload2
            global fileSourceName2
            isUpload2 = True
            fileSourceName2 = 'target.' + fileExt

            return redirect('http://127.0.0.1:5500/')
            # return {'msg': '12'}
        except:
            return redirect('http://127.0.0.1:5500/')

    else:
        return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form action="" method=post enctype=multipart/form-data>
        <p><input type=file name=the_file>
        <input type=submit value=Upload>
        </form>
        '''


@app.route('/ImageSimilarity', methods=['POST', 'GET'])
def ImageSimilarityProcess():
    if (isUpload and isUpload2):
        req = Algorithms.ImageSimilarity(fileSourceName, fileSourceName2)
        fileJSON = ImageReturn(req['src'])
        if req['msg'] == '666':
            res = '{:.2%}'.format(req['result'])
            return {'msg': '666', 'result': res, 'file': fileJSON}
        else:
            return {'msg': '-1'}
    else:
        return {'msg': '-2'}


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5050, debug=True)
