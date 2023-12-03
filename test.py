import torch
import csv

# PyTorch Hubから学習済みモデルをダウンロード 
model = torch.hub.load("../yolov5", "best", source='local')
# 検出できる物体を表示する(80種類)
print(model.names)  
 
results = model("car.jpg")  # 画像パスを設定し、物体検出を行う
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

results.show()  # 検出した物体の表示
results.crop()  # 検出した物体の切り取り