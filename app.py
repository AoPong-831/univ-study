from flask import Flask,render_template, request, redirect, Response, make_response
import googlemaps
import cv2
import datetime
import numpy as np

app = Flask(__name__)

GoogleApiKey = 'AIzaSyANuDUtyjaATaB2wXaJzo4MQI7XXu9Rbxg'
gmaps = googlemaps.Client(key=GoogleApiKey)

def Geocoding(name):
    result = gmaps.geocode(name)
    lat = result[0]["geometry"]["location"]["lat"]#緯度
    lng = result[0]["geometry"]["location"]["lng"]#軽度
    return [name,lat,lng]

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
        img = cv2.imdecode(img_array,1)
        #---よくわからないc&p zone 終わり

        #画像処理(番外編:お遊び)
        img = (img * -1) + 255
        img = np.clip(img, 0, 255).astype(np.uint8)

        #現在時刻を名前として「imgs/」に保存する
        dt_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        img_path = img_dir + dt_now + ".jpg"
        cv2.imwrite(img_path, img)#画像保存を行う関数(ファイル名,多次元配列(numpy,ndarray))

        data = Geocoding("清水寺")#data = Geocoding(name)
    return render_template("index.html", img_path = img_path,name=data[0],lat=data[1],lng=data[2])
        
        #return render_template("index.html",name=data[0],lat=data[1],lng=data[2])
    #else:
        #return render_template("index.html",name="none",lat=34,lng=135)#とりあえずエラー時の初期値

if __name__ == "__main__":
    app.run(debug=True)