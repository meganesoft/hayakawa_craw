import requests # urlを読み込むためrequestsをインポート
from bs4 import BeautifulSoup # htmlを読み込むためBeautifulSoupをインポート
import pandas as pd
import os.path
#def write_csv(func):
   # df = pd.read_csv('book.csv')
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
    
    for target in images: # imagesからtargetに入れる
        re = requests.get(target)
        with open('img/' + target.split('/')[-1], 'wb') as f: # imgフォルダに格納
            f.write(re.content) # .contentにて画像データとして書き込む
    
    for link in soup.find(id="M_itemDetail").findAll("p"):
        print("kokomade")
        print(link.getText())
        csv_data["text"] = str(link.getText())

    print(csv_data["text"])
    csv_data.to_csv("data/book.csv",encoding="shift_jis")
    print("ok") # 確認

#dataディレクトリにcsvファイルが作成されていない時にファイルを作成する
def create_csv():
    if os.path.isfile("data/book.csv"):
        pass
    else:
        csv_data = pd.DataFrame([["1","1","1"]],columns=["url","image","text"])
        csv_data.to_csv("data/book.csv")

def write_text(URL):
    soup = BeautifulSoup(requests.get(URL).content,'lxml') # bsでURL内を解析
    print(soup.find(id="M_itemDetail").findAll("p"))
    for link in soup.find(id="M_itemImg").findAll("p"): # pタグを取得しlinkに格納
        print(link.getText())
        
def crawl_web(seed):
    tocrawl = [seed]
    crawled = list()
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
            union(tocrawl, get_all_links(get_page(page)))
            crawled.append(page)
    return crawled

def main():
    url = "http://www.hayakawa-online.co.jp/shopdetail/000000013936/genre_001002/page1/order/"
    create_csv()
    write_data(url)

if __name__ == '__main__':
    main()
    

   