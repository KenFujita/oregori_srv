"""hist matching."""

import cv2
import os
import io
import numpy as np

# ゴリラの画像があるフォルダ名
IMG_DIR = os.path.abspath(os.path.dirname(__file__))
IMG_SIZE = (180, 180)
res_list = {}

def post_imageData(data):
    # BytesIOで読み込んでOpenCVで扱える型にする
    f = data.stream.read()
    bin_data = io.BytesIO(f)
    file_bytes = np.asarray(bytearray(bin_data.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    post_img = cv2.resize(img,IMG_SIZE)
    post_hist = cv2.calcHist([post_img], [0], None, [256], [0, 256])
    return post_hist

def parse_ndarray(file_name):
    target_img_path = IMG_DIR + file_name.lstrip(".")
    print(target_img_path)
    target_img = cv2.imread(target_img_path)
    target_img = cv2.resize(target_img, IMG_SIZE)
    target_hist = cv2.calcHist([target_img], [0], None, [256], [0, 256])
    return target_hist

def search_similar(target,file_name):
    files = os.listdir(IMG_DIR+'/Dogs/')
    for file in files:
        if file == '.DS_Store' or file == file_name:
            continue

        comparing_img_path = IMG_DIR + '/Dogs/' + file
        comparing_img = cv2.imread(comparing_img_path)
        if comparing_img is None:
            continue

        comparing_img = cv2.resize(comparing_img, IMG_SIZE)
        comparing_hist = cv2.calcHist([comparing_img], [0], None, [256], [0, 256])

        ret = cv2.compareHist(target, comparing_hist, 0)
        res_list[file]=ret
    return res_list

if __name__ == '__main__':
    TARGET_FILE = '05.png'
    result = parse_ndarray(TARGET_FILE)
    res_li = search_similar(result,TARGET_FILE)
    print('{}が最も似ているゴリラのimgname: {} 類似度: {}'.format(TARGET_FILE,max(res_li,key=res_li.get),max(res_li.values())))
