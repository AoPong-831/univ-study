from flask import Flask,render_template, request, redirect, Response, make_response
import googlemaps
import cv2
import datetime
import numpy as np
import easyocr

app = Flask(__name__)

GoogleApiKey = 'AIzaSyAhw39tHBs0l5t2gro0I8tmMI93JZk5OfU'
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
        #POSTにより受け取った画像を読み込む
        #---よくわからないc&p zone(htmlから画像を読み込み、pathを返す)
        stream = request.files["img"].stream
        img_array = np.asarray(bytearray(stream.read()),dtype=np.uint8)
        img = cv2.imdecode(img_array,1)#画像データ(配列)
        #---よくわからないc&p zone 終わり
        #現在時刻を名前として「imgs/」に保存する
        dt_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        img_path = img_dir + dt_now + ".jpg"
        cv2.imwrite(img_path, img)#画像保存を行う関数(ファイル名,多次元配列(numpy,ndarray))

        #画像処理(easyocr)
        reader = easyocr.Reader(["ja","en"])
        result = reader.readtext(img_path,detail=0)

        #geocoding
        data = Geocoding(result[0])#data = Geocoding(name)
    return render_template("index.html", img_path = img_path,name=data[0],lat=data[1],lng=data[2],API=GoogleApiKey)

if __name__ == "__main__":
    app.run(debug=True)