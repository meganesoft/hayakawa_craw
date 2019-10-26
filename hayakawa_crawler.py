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
from tqdm import tqdm

genre_pages = set()
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
            csv_data["title"] = soup.title.string
            csv_data.drop_duplicates(['url'],keep='first')
            csv_data.drop_duplicates(['image'],keep='first')
            csv_data.drop_duplicates(['title'],keep='first')

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
    except:
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
		csv_data = pd.DataFrame(index=[],columns=["url","image","text","title"])
		csv_data.to_csv("data/book.csv",index=False)

#未実装
def write_text(URL):
    soup = BeautifulSoup(requests.get(URL).content,'lxml') # bsでURL内を解析
    for link in soup.find(id="M_itemImg").findAll("p"): # pタグを取得しlinkに格納
        print(link.getText())

#重複する行の削除
def drop_csv():
    drop_csv = pd.read_csv("data/book.csv")
    settled_csv = drop_csv.drop_duplicates(['url'],keep='first')
    settled_csv.to_csv('data/book.csv',index=False)
    
#巡回するリンクのリストを作る
def genre_links(first_url,driver):
    print("ジャンルごとのURLを集めている")
    #サイトのページを取得
    driver.get(first_url)

    try:
        driver.find_element_by_xpath('//*[@id="M_ctg1_5745"]/span/a').click()
        #レンダリングを待つ
        sleep(5)
        click_html = driver.page_source
    except:
        print("clickできてないよ")
        driver.close()

    try:
        soup = BeautifulSoup(click_html,'lxml')
    except:
        print("soupがとれない")
        return


    for a_tag in soup.find_all(href=re.compile("/shopbrand/genre*")):
        print(a_tag)
        if 'href' in a_tag.attrs:
            if('shopdetail' in a_tag.attrs['href'] or 'shopbrand' in a_tag.attrs['href']):
                href = a_tag.attrs['href']
                genre_Page = urljoin('http://www.hayakawa-online.co.jp/',href)
                if genre_Page not in genre_pages:
                    genre_pages.add(genre_Page)


#ジャンルごとの書籍の詳細のURLを集める
def enum_links (genre_url):
    print("作業中")

    try:
        soup = BeautifulSoup(requests.get(genre_url).content,'lxml')
    except:
        print("soupがとれない")
        return

    
    for a in soup.findAll(href=re.compile("^/shopdetail/.*/order/$")):
        #hrefがあるか確かめる
        if'href' in a.attrs:
           #一度解析したリンクに飛んでないか確かめる
            if('shopdetail' in a.attrs['href'] or 'shopbrand' in a.attrs['href']):
                href = a.attrs['href']
                newPage = urljoin('http://www.hayakawa-online.co.jp/',href)
                if newPage not in pages:
                    pages.add(newPage)
                    print(len(pages))
                    enum_links(newPage) 
            else:
                print("失敗")
                return

def main():
    url = "http://www.hayakawa-online.co.jp/"
    options = webdriver.chrome.options.Options()
    options.add_argument("--headless")#これを消せばブラウザ画面が出る

    driver = webdriver.Chrome(chrome_options=options)

    create_csv()
    genre_links(url,driver)
    print(genre_pages)

    for url in genre_pages:
        enum_links(url)
    for link in tqdm(pages):
        print("取得したURL")
        write_data(link)
        sleep(0.001)
    drop_csv()
    print("完了！！！！！")

if __name__ == '__main__':
    main()
