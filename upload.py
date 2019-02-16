import os
import sqlite3
import binascii
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session
from werkzeug import secure_filename
from datetime import datetime
from PIL import Image
from io import BytesIO
import histogram
import firebasepy

app = Flask(__name__)

UPLOAD_FOLDER = './path/to/upload_dir'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.urandom(24)

# test: rootにアクセスするとhelloworldを返す
@app.route('/')
def hello():
	return 'Hello world!'

'''
        send()... byte列に変換された画像とfirebaseに登録するための固有のIDを受け取る
                  ↓
                  先頭にIDがあるのでスライスで分割する
                  ↓
                  リクエストがPOSTの場合でbyte列に変換された画像があるなら、サーバ上に画像データに直して保存する
                  ↓
                  保存した画像をヒストグラムの配列に変換し、一番似ているゴリラの画像パスと類似度を受け取る
                  ↓
                  それをfirebase上に登録し、成功したらその旨のメッセージを返す

'''

@app.route('/send', methods=['GET', 'POST'])
def send():
    length = len(str(binascii.hexlify(request.data), 'utf-8'))
    u_id = bytes.fromhex(str(binascii.hexlify(request.data),'utf-8')[length-32:length]).decode('utf-8')
    cv_dict = {}
    if request.method == 'POST':
        img_file = request.data[:length-32]
        if img_file:
            filename = 'Android_picture'+datetime.now().strftime("%Y%m%d%H%M%S")+'.jpg'
            android_pic = Image.open(BytesIO(img_file))
            img_url = './uploads/' + filename
            android_pic.save(img_url)
            pic_hist = histogram.parse_ndarray(img_url)
            cv_dict = histogram.search_similar(pic_hist,img_url)
            result = str(max(cv_dict,key=cv_dict.get)) + ',' + str(max(cv_dict.values()))
            firebasepy.update_value(u_id,result)
            return 'Success!!'
        else:
            return 'Failed...!'
    else:
        return 'oops'

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0',port=8000)
