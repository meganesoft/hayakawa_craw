import requests # urlを読み込むためrequestsをインポート
from bs4 import BeautifulSoup # htmlを読み込むためBeautifulSoupをインポート
import pandas as pd
import os.path
from urllib.request import urlopen
from urllib.parse import urljoin
from urllib.parse import urlparse
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

pages = set()

def write_data(html):
    print("書き込むよ")
    images = [] # 画像リストの配列
    csv_data = pd.read_csv("data/book.csv")
    try:
        soup = BeautifulSoup(requests.get(html).content,'lxml') # bsでURL内を解析
        #soup = BeautifulSoup(html.page_source.encode('utf-8'),'lxml') 
        print('取得したタイトル')
        print(soup.title.string)
        for link in soup.find(id="M_itemImg").findAll("img"): # imgタグを取得しlinkに格納
            if link.get("src").endswith(".jpg"): # imgタグ内の.jpgであるsrcタグを取得
                images.append(link.get("src")) # imagesリストに格納
            elif link.get("src").endswith(".png"): # imgタグ内の.pngであるsrcタグを取得
                images.append(link.get("src")) # imagesリストに格納
        print(images)
        
        ############################
        #画像名,URLを保存する処理を書く
        ############################
        for target in images: # imagesからtargetに入れる
            re = requests.get(target)
            #正規表現でURLから画像名だけを抽出してCSVに書き込み
            csv_data["url"] = html
            csv_data["image"] = target.split('/')[-1]
            csv_data.drop_duplicates(['url'],keep='first')
            csv_data.drop_duplicates(['image'],keep='first')

            #画像があるときだけURLを書き込む
            with open('img/' + target.split('/')[-1], 'wb') as f: # imgフォルダに格納
                f.write(re.content) # .contentにて画像データとして書き込む
        
        #CSVにテキストを書き込む
        for link in soup.find(id="M_itemDetail").findAll("p"):
            print(link.getText())
            csv_data["text"] = str(link.getText())
            csv_data.drop_duplicates(['text'],keep='first')

        
        csv_data.to_csv("data/book.csv",encoding="utf-8",index=False,mode="a")
        print("成功したよ\n") # 確認
    except AttributeError:
        import traceback
        traceback.print_exc()
        print("AttributeError")
        pass
    except NameError:
        print("失敗した\n")
        pass
        
#dataディレクトリを作成しdataディレクトリにcsvファイルが作成されていない時にファイルを作成する
def create_csv():
	#フォルダ確認、作成
	if os.path.isdir("data"):
		pass
	else:
		os.mkdir("data")
	if os.path.isdir("img"):
		pass
	else:
		os.mkdir("img")
	#CSVファイル確認、作成
	if os.path.isfile("data/book.csv"):
		pass
	else:
		csv_data = pd.DataFrame([["1","1","1"]],columns=["url","image","text"])
		csv_data.to_csv("data/book.csv",index=False)

#未実装
def write_text(URL):
    soup = BeautifulSoup(requests.get(URL).content,'lxml') # bsでURL内を解析
    for link in soup.find(id="M_itemImg").findAll("p"): # pタグを取得しlinkに格納
        print(link.getText())
        
def drop_csv():
    drop_csv = pd.read_csv("data/book.csv")
    settled_csv = drop_csv.drop_duplicates(['url'],keep='first')
    settled_csv.to_csv('data/book.csv',index=False)
    
#巡回するリンクのリストを作る
#seleniumには屈服した
def enum_links (base_html):
    print("作業中")
    global pages
    #base_html = urlparse(base_html).scheme+"://"+urlparse(base_html).netloc
    try:
        soup = BeautifulSoup(requests.get(base_html).content,'lxml')
    except:
        return
    '''
    options = webdriver.chrome.options.Options()
    options.add_argument("--headless")#これを消せばブラウザ画面が出る
    
    driver = webdriver.Chrome(chrome_options=options)

    try:
        driver.get(base_html)
        len_driver = driver.find_element_by_xpath('//*[@id="M_ctg1_3"]/span/a').click()
        soup = BeautifulSoup(len_driver.page_source,'lxml')
        len_driver.close()
        print("クリックしたよ")
    except:
        try:
            soup = BeautifulSoup(requests.get(base_html).content,'lxml')
        except:
            return

    driver.close()
    '''
    #links = soup.findAll('a',href=re.compile("^shopbrand/*|^shopdetail/*"))
    #returnがおかしいと思われ
    for a in soup.findAll('a',href=re.compile("^/shopbrand/*|^/shopdetail/*")):
        #hrefがあるか確かめる
        if'href' in a.attrs:
           #if a.attrs['href'] is not None:
           #一度解析したリンクに飛んでないか確かめる
            if a.attrs['href'] not in pages:
                if('shopdetail' in a.attrs['href'] or 'shopbrand' in a.attrs['href']):
                    href = a.attrs['href']
                    newPage = urljoin('http://www.hayakawa-online.co.jp/',href)
                    if newPage not in pages:
                        pages.add(newPage)
                        print(len(pages))
                        enum_links(newPage) 
    else:
        return pages

#selenium操作関数
def analyze_html(url):	
    options = webdriver.chrome.options.Options()
    options.add_argument("--headless")#これを消せばブラウザ画面が出る
    
    driver = webdriver.Chrome(chrome_options=options)
    #driverをゲットできなかったらurlを返す,ット出来たらjs実行後のdriverか実行してないdriverを返す
    try:
        driver.get(url)
    except:
        print("urlとして返すわ")
        return url
    try:
        #driver.execute_script("showMakeShopChildCategory")
        print("実行後のドライバー返した")
        return driver
    except:
        print("driver返した")
        return driver

def main():
    original_url = ['http://www.hayakawa-online.co.jp/shopbrand/genre_001001/','http://www.hayakawa-online.co.jp/shopbrand/genre_001002/','http://www.hayakawa-online.co.jp/shopbrand/genre_001003/','http://www.hayakawa-online.co.jp/shopbrand/genre_001004/','http://www.hayakawa-online.co.jp/shopbrand/genre_001004/','http://www.hayakawa-online.co.jp/shopbrand/genre_001006/','http://www.hayakawa-online.co.jp/shopbrand/genre_001007/','http://www.hayakawa-online.co.jp/shopbrand/genre_001008/','http://www.hayakawa-online.co.jp/shopbrand/genre_002008/','http://www.hayakawa-online.co.jp/shopbrand/genre_001009/','http://www.hayakawa-online.co.jp/shopbrand/genre_001010/','http://www.hayakawa-online.co.jp/shopbrand/genre_001011/','http://www.hayakawa-online.co.jp/shopbrand/genre_001012/','http://www.hayakawa-online.co.jp/shopbrand/genre_001013/','http://www.hayakawa-online.co.jp/shopbrand/genre_001014/','http://www.hayakawa-online.co.jp/shopbrand/genre_001015/','http://www.hayakawa-online.co.jp/shopbrand/genre_001016/']
    #original_url = "http://www.hayakawa-online.co.jp/shopdetail/000000013936/genre_001002/"
    #url = "http://www.hayakawa-online.co.jp/"
    create_csv()
    #write_data(analyze_html(url))
    for url in original_url:
        link = enum_links(url)
        for next_link in link:
            print("取得したURLだよ！")
            print(next_link)
            write_data(next_link)
            drop_csv()
            sleep(0.0001)

if __name__ == '__main__':
    main()
