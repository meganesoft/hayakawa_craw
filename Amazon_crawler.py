import requests # urlを読み込むためrequestsをインポート
from bs4 import BeautifulSoup # htmlを読み込むためBeautifulSoupをインポート
import pandas as pd
import os.path
from urllib.request import urlopen
import re

pages = set()
#def csv_joiner(*File,**Filetype):
#   def decorator(f):
       
#   df = pd.read_csv('book.csv')
    #画像のタイトルや概要テキストをCSVに保存する処理を書く
    #def decorator(f):
        
        

def write_data(URL):
    images = [] # 画像リストの配列
    csv_data = pd.read_csv("data/book.csv")
    soup = BeautifulSoup(requests.get(URL).content,'lxml') # bsでURL内を解析
    
    #print(soup.find(id="M_itemImg").findAll("img"))
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
        print(target.split('/')[-1])
        with open('img/' + target.split('/')[-1], 'wb') as f: # imgフォルダに格納
            f.write(re.content) # .contentにて画像データとして書き込む
    
    #CSVにテキストを書き込む
    for link in soup.find(id="M_itemDetail").findAll("p"):
        print("kokomade")
        print(link.getText())
        csv_data["text"] = str(link.getText())

    csv_data.to_csv("data/book.csv",encoding="utf-8")
    print("ok") # 確認

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
		csv_data.to_csv("data/book.csv")

#未実装
def write_text(URL):
    soup = BeautifulSoup(requests.get(URL).content,'lxml') # bsでURL内を解析
    print(soup.find(id="M_itemDetail").findAll("p"))
    for link in soup.find(id="M_itemImg").findAll("p"): # pタグを取得しlinkに格納
        print(link.getText())
        
def enum_links(html,base):
	soup = BeautifulSoup(html)
	links = soup.select("a[href]")
	next_link = set()
	
	for a in links:
		href = a.attrs['href']
		url = urljoin(base,href)
		next_link.append(url)
	return next_link

#def analize_html(url,root_url):	

def main():
    url = "http://www.hayakawa-online.co.jp/shopdetail/000000013936/genre_001002/page1/order/"
    create_csv()
    write_data(url)

if __name__ == '__main__':
    main()
    

   
