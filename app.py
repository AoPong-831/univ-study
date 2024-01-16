from flask import Flask,render_template, request, redirect, Response, make_response
import googlemaps
import cv2
import datetime
import numpy as np
import easyocr
from yolov5 import detect
import subprocess
import os
import shutil
import time
import torch
import csv
import re


def EasyOcr(img_path):
    reader = easyocr.Reader(["ja","en"])#認識言語設定
    result = reader.readtext(img_path,detail=0)#文字読み込み
    
    #画像処理結果を表示、綺麗にして出荷
    print("-"*30)
    #resultから、いらない文字を消すためのリスト
    DELETE_CHARACTER = ["\\d","[.|\[|\]]"]#[\d]数字消す,". [ ]"消す,
    newResult = []
    for i in result:
        #resultから、いらない文字消す
        for j in DELETE_CHARACTER:
            i = re.sub(j,"", i)
        print("["+ i +"]")
        if i:#適切な文字があればリストに保管
            newResult.append(i)
    print("-"*30)

    print(newResult)
    return newResult

def Geocoding(name):
    try:
        result = gmaps.geocode(name)
        lat = result[0]["geometry"]["location"]["lat"]#緯度
        lng = result[0]["geometry"]["location"]["lng"]#軽度
        data = [name,lat,lng]
    except:
        data = ["error",34,135]
    return data





app = Flask(__name__)

GoogleApiKey = 'AIzaSyANuDUtyjaATaB2wXaJzo4MQI7XXu9Rbxg'
gmaps = googlemaps.Client(key=GoogleApiKey)

@app.route('/',methods=["GET","POST"])
def index():
    img_dir = "static/imgs/"#画像が入ってるファイルのpath(後で使う)

    #便宜上
    data = ["none",34,135]

    if request.method == "GET": img_path = None
    elif request.method == "POST":
        #imgsの中身を一旦空にする(1.imgsを消して、2.再度作成)
        shutil.rmtree('static/imgs')#1
        os.mkdir('static/imgs')#2

        #POSTにより受け取った画像を読み込む
        #---よくわからないc&p zone(htmlから画像を読み込み、pathを返す)
        stream = request.files["img"].stream
        img_array = np.asarray(bytearray(stream.read()),dtype=np.uint8)
        img = cv2.imdecode(img_array,1)#画像データ(配列)
        #---よくわからないc&p zone 終わり

        img_path = img_dir + "pic.jpg"#画像の名前設定(原則 pic.jpg)
        cv2.imwrite(img_path, img)#画像保存を行う関数(ファイル名,多次元配列(numpy,ndarray))
        #***

    #保存した画像ファイルのpathをHTMLに渡す
    return render_template("index.html", img_path = img_path,placeName=None,lat=None,lng=None,API=GoogleApiKey)





@app.route('/yolov5', methods=['GET'])
def yolov5():
    #detectの中身を一旦空にする(1.detectを消して、2.再度作成)(indexの最初、static/imgsと同様の動作)
    try:#2を実行後、yoloがエラーを吐いて止まった時用。
        shutil.rmtree('runs/detect')#1
    except:
        pass
    os.mkdir('runs/detect')#2

    #画像切り取り==========
    model = torch.hub.load("yolov5", "best", source='local')#(実行ファイル, 重み付け, ...)の順に書く。
    # 検出できる物体を表示する(80種類)
    print(model.names)#いつか使う?ために残してる。
 
    results = model("static/imgs/pic.jpg")  # 画像パスを設定し、物体検出を行う
    objects = results.pandas().xyxy[0]  # 検出結果を取得してobjectに格納
    # objectに格納したデータ
    # => バウンディングBOX左上のx座標とy座標、信頼度、クラスラベル、物体名

    # 物体検出結果を出力するためのcsvファイルを作成
    with open('detection_Result.csv', 'w') as f:
        print("ID,種類,x座標,y座標,幅,高さ", file=f) # print()の第2引数で出力先を指定可能
 
        for i in range(len(objects)):
            name = objects.name[i]
            xmin = objects.xmin[i]
            ymin = objects.ymin[i]
            width = objects.xmax[i] - objects.xmin[i]
            height = objects.ymax[i] - objects.ymin[i]
            # print(f"{i}, 種類:{name}, 座標x:{xmin}, 座標y:{ymin}, 幅:{width}, 高さ:{height}")
            # csvファイルにバウンディングBOX情報を出力
            print(f"{i},{name},{xmin},{ymin},{width},{height}", file=f)

    results.crop()  # 検出した物体の切り取り
    #==========画像切り取り終わり


    img_path = "runs/detect/exp/crops/license/pic.jpg"#ここいずれ複数検索に対応させる。(以下)
    #files = os.listdir(img_path)#file内のファイル名をlistで列挙

    #画像処理(easyocr)
    result = EasyOcr(img_path)

    #geocoding
    try:
        data = Geocoding(result[0])#data = Geocoding(name)
    except:#Geocording で何かしらのエラーが起こった時。
        data = ['none', 0, 0]

    #保存した画像ファイルのpath, geocordingデータをHTMLに渡す
    return render_template("index.html", img_path = img_path,placeName=data[0],lat=data[1],lng=data[2],API=GoogleApiKey)    
    


if __name__ == "__main__":
    app.run(debug=True, port=8888)