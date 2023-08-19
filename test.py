import time
from selenium import webdriver

options = webdriver.ChromeOptions()
# デバッグログを表示させないoption
#options.add_experimental_option('excludeSwitches', ['enable-logging'])
# ヘッドレスモードを有効にする（次の行をコメントアウトすると画面が表示される）。
# options.add_argument('--headless')
# ChromeのWebDriverオブジェクトを作成する。
driver = webdriver.Chrome(executable_path=r"C:\chromedriver_win32\chromedriver.exe", options=options)
# Googlemapのトップ画面を開く。
driver.get('https://www.google.co.jp/maps/')
# HTML内で検索ボックス(name='q')を指定する
search = driver.find_element_by_name('q')
# 検索ワードを送信する
search.send_keys('浅草橋')
# 検索を実行
driver.find_element_by_id("searchbox-searchbutton").click()
# 5秒間待機
time.sleep(5)

def ranking(driver):
    # ループ番号、ページ番号を定義
    i = 1
    # 最大何ページまで分析するかを定義
    i_max = 1
    # タイトルを格納する空リストを用意
    title_list = []
    # 緯度を格納する空リストを用意
    ido_list = []     # タイトルを格納する空リストを用意
    # 経度を格納する空リストを用意
    keido_list = []      # URLを格納する空リストを用意
    # 現在のページが指定した最大分析ページを超えるまでループする
    while i <= i_max:
        # タイトルをclass="section-result"に入っている
        class_group = driver.find_elements_by_css_selector('.section-result')
        # タイトルを抽出しリストに追加するforループ
        for elemnum in range(len(class_group)):
            # URLの遷移によるエラー対策のため再度タイトルを抽出する
            class_group = driver.find_elements_by_css_selector('.section-result')
            # class_groupのelemnum番目の要素を取得
            elem = class_group[elemnum]
            # タイトル(class="section-result-title")
            title_list.append(elem.find_element_by_css_selector('.section-result-title').text)
            # 次へのボタンをクリック(class="section-result-content")
            elem.find_element_by_class_name('section-result-content').click()
            # 3秒間待機
            time.sleep(3)
            # クリック先のURLの取得
            txt = driver.current_url
            # 取得したURLの文字列の中から"!3d"の位置を見つける
            pos = txt.find('!3d')
            # "!3d"の位置から!3dを除いた後ろの文字列を取得する
            txt2 = driver.current_url[pos+3:]
            # さらに"!4d"で文字列を分割
            txt3 = txt2.split('!4d')
            # 分割した文字列の前側が緯度
            ido_list.append(txt3[0])
            # 分割した文字列の後側が緯度
            keido_list.append(txt3[1])
            # "結果一覧に戻る"ボタンをクリック(class="section-back-to-list-button.blue-link.noprint")
            driver.find_element_by_css_selector('.section-back-to-list-button.blue-link.noprint').click()
            # 3秒間待機
            time.sleep(3)
 
        # 次ページボタンがあると試す
        try:
            # 次ページをクリック
            driver.find_element_by_id('n7lv7yjyC35__section-pagination-button-next').click()
            # iを更新
            i = i + 1
            # 5秒間待機
            time.sleep(5)
        # 次ページボタンがない場合は終了する
        except:
            i = i_max + 1
 
    # タイトルとリンクのリストを戻り値に指定
    return title_list, ido_list, keido_list
 
# ranking関数を実行してタイトルとURLリストを取得する
title, ido, keido= ranking(driver)
 
 
# タイトルリストをテキストに保存
with open('title.txt', mode='w', encoding='utf-8') as f:
    f.write("\n".join(title))
# 緯度リストをテキストに保存
with open('ido.txt', mode='w', encoding='utf-8') as f:
    f.write("\n".join(ido))
# 経度リストをテキストに保存
with open('keido.txt', mode='w', encoding='utf-8') as f:
    f.write("\n".join(keido))
# ブラウザを閉じる
driver.quit()