from flask import Flask,render_template, request, redirect, Response, make_response
import googlemaps

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
    if request.method == "POST":
        name = request.form["entry"]#名前を受け取る

        data = Geocoding(name)
        return render_template("index.html",name=data[0],lat=data[1],lng=data[2])
    else:
        return render_template("index.html",name="none",lat=34,lng=135)#とりあえずエラー時の初期値

if __name__ == "__main__":
    app.run(debug=True)