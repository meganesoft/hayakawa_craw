import requests # urlを読み込むためrequestsをインポート
from bs4 import BeautifulSoup # htmlを読み込むためBeautifulSoupをインポート
import pandas as pd
import os.path
from urllib.request import urlopen
from urllib.parse import urljoin
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

#def csv_joiner(*File,**Filetype):
#   def decorator(f):
       
#   df = pd.read_csv('book.csv')
    #画像のタイトルや概要テキストをCSVに保存する処理を書く
    #def decorator(f):
        
        

def write_data(html):
    print("書き込むよ")
    images = [] # 画像リストの配列
    csv_data = pd.read_csv("data/book.csv")
    try:
        #soup = BeautifulSoup(requests.get(html.current_url).content,'lxml') # bsでURL内を解析
        soup = BeautifulSoup(html.page_source,'lxml') 
        print(soup.title.string)
        for link in soup.find(id="M_itemImg").findAll("img"): # imgタグを取得しlinkに格納
            if link.get("src").endswith(".jpg"): # imgタグ内の.jpgであるsrcタグを取得
                images.append(link.get("src")) # imagesリストに格納
            elif link.get("src").endswith(".png"): # imgタグ内の.pngであるsrcタグを取得
                images.append(link.get("src")) # imagesリストに格納
        
        ############################
        #画像名,URLを保存する処理を書く
        ############################
        for target in images: # imagesからtargetに入れる
            re = requests.get(target)
            #正規表現でURLから画像名だけを抽出してCSVに書き込み
            csv_data["url"] = html.current_url
            csv_data["image"] = target.split('/')[-1]
            csv_data.drop_duplicates(['url'],keep='first')
            csv_data.drop_duplicates(['image'],keep='first')

            #画像があるときだけURLを書き込む
            with open('img/' + target.split('/')[-1], 'wb') as f: # imgフォルダに格納
                f.write(re.content) # .contentにて画像データとして書き込む
        
        #CSVにテキストを書き込む
        for link in soup.find(id="M_itemDetail").findAll("p"):
            #print(link.getText())
            csv_data["text"] = str(link.getText())
            csv_data.drop_duplicates(['text'],keep='first')

        
        csv_data.to_csv("data/book.csv",encoding="utf-8",index=False,mode="a")
        print("成功したよ\n") # 確認
    except AttributeError:
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
    
def enum_links (base_html,pages):
    print(type(base_html))
    #一度解析したurlを読み込まないようにする
    if base_html in pages: return
    options = webdriver.chrome.options.Options()
    options.add_argument("--headless")#これを消せばブラウザ画面が出る
    
    driver = webdriver.Chrome(chrome_options=options)

    driver.get(base_html)
    try:
        len_driver = driver.find_element_by_xpath('//*[@id="M_ctg1_3"]/span/a').click()
        soup = BeautifulSoup(len_driver.page_source,'lxml')
        print("クリックしたよ")
    except:
        soup = BeautifulSoup(driver.page_source,'lxml')

    links = soup.findAll('a')
    #returnがおかしいと思われ
    for a in links:
        if a.attrs['href'] is not None:
            href = a.attrs['href']
            print(href)
            url = urljoin(base_html,href)
            pages.append(url)
            print(url)
            return enum_links(url,pages) 
        else: return pages
    else:
        return pages

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
        driver.execute_script("showMakeShopChildCategory")
        print("実行後のドライバー返した")
        return driver
    except:
        print("driver返した")
        return driver

def main():
    #url = 'http://www.hayakawa-online.co.jp/shopbrand/genre_001001/'
    #url = "http://www.hayakawa-online.co.jp/shopdetail/000000013936/genre_001002/page1/order/"
    url = "http://www.hayakawa-online.co.jp/"
    pages = []
    create_csv()
    write_data(analyze_html(url))
    link = enum_links(url,pages)
    print(link)
    for next_link in link:
        print("取得したURLだよ！")
        print(next_link)
        write_data(analyze_html(next_link))
        drop_csv()
        sleep(0.001)

if __name__ == '__main__':
    main()
