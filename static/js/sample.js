var map;
var marker;
var center = {
    lat: lat, // 緯度
    lng: lng // 経度
};
var resultText = document.getElementById("resultText");// index.html id=resultTextの部分を以下の文字列に変換する
resultText.innerHTML = "[デバッグ用]" + placeName + ":" + lat + ":" + lng;//一応結果表示(デバック用)

function initMap() {
    map = new google.maps.Map(document.getElementById('sample'), { // #sampleに地図を埋め込む
        center: center, // 地図の中心を指定
        zoom: 19 // 地図のズームを指定
    });

    marker = new google.maps.Marker({ // マーカーの追加
        position: center, // マーカーを立てる位置を指定
        map: map // マーカーを立てる地図を指定
    });
}