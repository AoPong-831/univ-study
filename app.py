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

app = Flask(__name__)

GoogleApiKey = 'AIzaSyANuDUtyjaATaB2wXaJzo4MQI7XXu9Rbxg'
gmaps = googlemaps.Client(key=GoogleApiKey)

def Geocoding(name):
    try:
        result = gmaps.geocode(name)
        lat = result[0]["geometry"]["location"]["lat"]#緯度
        lng = result[0]["geometry"]["location"]["lng"]#軽度
        data = [name,lat,lng]
    except:
        data = ["error",34,135]
    return data

@app.route('/',methods=["GET","POST"])
def index():
    img_dir = "static/imgs/"#画像が入ってるファイルのpath(後で使う)

    #便宜上
    data = ["none",34,135]

    if request.method == "GET": img_path = None
    elif request.method == "POST":
        #imgsの中身を一旦空にする(imgsを消して、再度作成)
        shutil.rmtree('static/imgs')
        os.mkdir('static/imgs')

        #POSTにより受け取った画像を読み込む
        #---よくわからないc&p zone(htmlから画像を読み込み、pathを返す)
        stream = request.files["img"].stream
        img_array = np.asarray(bytearray(stream.read()),dtype=np.uint8)
        img = cv2.imdecode(img_array,1)#画像データ(配列)
        #---よくわからないc&p zone 終わり

        #***現在時刻を名前として「imgs/」に保存する
        dt_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        img_path = img_dir + dt_now + ".jpg"
        cv2.imwrite(img_path, img)#画像保存を行う関数(ファイル名,多次元配列(numpy,ndarray))
        #***

        #画像処理(easyocr)
        reader = easyocr.Reader(["ja","en"])
        result = reader.readtext(img_path,detail=0)#文字に直す？
        #画像処理結果を表示
        print("-"*30)
        for i in result:
            print("["+ i +"]")
        print("-"*30)
            

        #geocoding
        try:
            data = Geocoding(result[0])#data = Geocoding(name)
        except:#Geocording で何かしらのエラーが起こった時。
            data = ['none', 0, 0]

    #保存した画像ファイルのpath, geocordingデータをHTMLに渡す
    return render_template("index.html", img_path = img_path,name=data[0],lat=data[1],lng=data[2],API=GoogleApiKey)


@app.route('/yolov5', methods=['GET'])
def yolov5():
    #detectの中身を一旦空にする(1.detectを消して、再度作成)(2.imgsと同様の動作)
    shutil.rmtree('yolov5/runs/detect')#1
    os.mkdir('yolov5/runs/detect')#2

    #yolov5
    files = os.listdir("static/imgs")#指定pathの中身をlistで取得。(該当画像)
    cmd = "python yolov5/detect.py --source static/imgs/"+files[0]+" --weights yolov5/best.pt"#cmdを書く(detect.pyを動かすため)
    subprocess.call(cmd.split())#cmd実行

    return index()


if __name__ == "__main__":
    app.run(debug=True, port=8888)