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

pages = set()
#def csv_joiner(*File,**Filetype):
#   def decorator(f):
       
#   df = pd.read_csv('book.csv')
    #画像のタイトルや概要テキストをCSVに保存する処理を書く
    #def decorator(f):
        
        

def write_data(html):
    #driver = webdriver.PhantomJS()
    #drver.get(URL)
    
    images = [] # 画像リストの配列
    csv_data = pd.read_csv("data/book.csv")
    try:
        soup = BeautifulSoup(requests.get(html).content,'lxml') # bsでURL内を解析
        #soup = BeautifulSoup(driver.page_source,'lxml') 

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
            csv_data["url"] = URL
            csv_data["image"] = target.split('/')[-1]
            csv_data.drop_duplicates(['url'],keep='first')
            csv_data.drop_duplicates(['image'],keep='first')

            #画像があるときだけURLを書き込む
            with open('img/' + target.split('/')[-1], 'wb') as f: # imgフォルダに格納
                f.write(re.content) # .contentにて画像データとして書き込む
        
        #CSVにテキストを書き込む
        for link in soup.find(id="M_itemDetail").findAll("p"):
            print("kokomade")
            print(link.getText())
            csv_data["text"] = str(link.getText())
            csv_data.drop_duplicates(['text'],keep='first')

        
        csv_data.to_csv("data/book.csv",encoding="utf-8",index=False,mode="a")
        print("ok") # 確認
    except AttributeError:
        pass
    except:
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
    print(soup.find(id="M_itemDetail").findAll("p"))
    for link in soup.find(id="M_itemImg").findAll("p"): # pタグを取得しlinkに格納
        print(link.getText())
        
def drop_csv():
    drop_csv = pd.read_csv("data/book.csv")
    settled_csv = drop_csv.drop_duplicates(['url'],keep='first')
    settled_csv.to_csv('data/book.csv',index=False)
    
def enum_links(html,base):
    soup = BeautifulSoup(requests.get(html).content,'lxml')
    #soup = BeautifulSoup(html)
    links = soup.select("a[href]")
    next_link = set()
	
    for a in links:
        href = a.attrs['href']
        url = urljoin(base,href)
        next_link.add(url)
    return next_link

def analize_html(url):	
    options = webdriver.chrome.options.Options()
    options.add_argument("--headless")#これを消せばブラウザ画面が出る
    
    driver = webdriver.Chrome(chrome_options=options)

    driver.get(url)
    #これを実装する
    driver.find_element_by_xpath(//div[contains(@M_ctgl
    
    return driver.page_source

def main():
    #url = "http://www.hayakawa-online.co.jp/shopdetail/000000013936/genre_001002/page1/order/"
    url = "http://www.hayakawa-online.co.jp/"
    create_csv()
    link = enum_links(url,url)
    for next_link in link:
        print(next_link)
        write_data(analize_html(next_link))
        drop_csv()

if __name__ == '__main__':
    main()
