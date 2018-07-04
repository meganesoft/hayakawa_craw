import requests # urlを読み込むためrequestsをインポート
from bs4 import BeautifulSoup # htmlを読み込むためBeautifulSoupをインポート
print("kokomade")
def write_image(URL):
    images = [] # 画像リストの配列

    soup = BeautifulSoup(requests.get(URL).content,'lxml') # bsでURL内を解析
    print("kokomade")
    #print(soup.find(id="M_itemImg").findAll("img"))
    print(soup.find(id="M_itemDetail").findAll("p"))
    for link in soup.find(id="M_itemImg").findAll("img"): # imgタグを取得しlinkに格納
        if link.get("src").endswith(".jpg"): # imgタグ内の.jpgであるsrcタグを取得
            images.append(link.get("src")) # imagesリストに格納
        elif link.get("src").endswith(".png"): # imgタグ内の.pngであるsrcタグを取得
            images.append(link.get("src")) # imagesリストに格納
    
    for target in images: # imagesからtargetに入れる
        re = requests.get(target)
        with open('img/' + target.split('/')[-1], 'wb') as f: # imgフォルダに格納
            f.write(re.content) # .contentにて画像データとして書き込む
 
    print("ok") # 確認

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
    write_image(url)

if __name__ == '__main__':
    main()
    

   