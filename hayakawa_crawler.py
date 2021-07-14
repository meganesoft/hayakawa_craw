# coding*utf-8
from bs4 import BeautifulSoup, element
from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.common.keys import Keys
from tqdm import tqdm
import os
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains

def readUrlFile(filepath):
    if os.path.exists(filepath):
        with open(filepath,'r') as f:
            url_list = f.read().split("\n")
        return url_list
    else:
        print("ファイルがないから作ります")
        os.makedirs('SnapUrl',exist_ok=True)
        with open(filepath,'w') as f:
            f.write('ここにURLを書く(この文字は消す)')
        print('Done')
        driver.close()
        exit()

def readInputFile(filepath):
    if  os.path.exists(filepath):
        with open(filepath,'r') as f:
            input_list = f.read().split("\n")
        return input_list
    else:
        print("ファイルがないから作ります")
        os.makedirs('SnapUrl/input/',exist_ok=True)
        with open(filepath,'w') as f:
            f.write('ここに入力内容を書く(この文字は消す)')
        print('Done')
        exit()

#region Azure用
#Azure用
def enum_link_azure(url,driver,target):
    search =  driver.find_elements_by_class_name(target)
    #urls = [_.get_attribute('href') for _ in search
    urls = [_.text for _ in search]
    if urls == []:
        print("リンクがカラ")
    for url in urls:
        try:
            Alert(driver).accept()
        except:
            pass
        print(url)
        #driver.get(url)
        
        #print(driver.find_element_by_css_selector('.fxs-blade-title-titleText.msportalfx-tooltip-overflow').text)
        #driver.save_screenshot(driver.title + ".png")

def get_table(driver,target):
    tableElem = driver.find_elements_by_class_name(target)
    #trs = tableElem.find_elements(By.TAG_NAME, "tr")
    trs = [_.tr for _ in tableElem]
    for i in range(1,len(trs)):
        tds = trs[i].find_elements(By.TAG_NAME, "td")
        line = ""
        for j in range(0,len(tds)):
            if j < len(tds)-1:
                line += "%s\t" % (tds[j].text)
            else:
                line += "%s" % (tds[j].text)
        print(line +"\r\n")

#endregion

#region screenshot
def enum_shot(file,slowfile):
    urls = readUrlFile(file)
    slows = readUrlFile(slowfile)
    #operation_login_tk(driver,id,password)
    index = 0
    for url in urls:
        try:
            print(url)
            driver.get(url)
            WebDriverWait(driver,10).until(EC.presence_of_all_elements_located)
            if  os.path.exists('SnapShot/' + mode):
                driver.save_screenshot('SnapShot/' + mode + '/' + str(index) + '.png')
            else:
                os.makedirs('SnapShot/' + mode,exist_ok=True)
                driver.save_screenshot('SnapShot/' + mode + '/' + str(index) + '.png')
            index += 1
            print(url + ":DONE")
        except:
            index += 1
            print(url + ":Failure")
    #読み込みが遅いやつ用のスクリーンショット
    for url in slows:
        print(url)
        driver.get(url)
        sleep(5)
        if  os.path.exists('SnapShot/' + mode):
                driver.save_screenshot('SnapShot/' + mode + '/' + str(index) + '.png')
        else:
                os.makedirs('SnapShot/' + mode,exist_ok=True)
                driver.save_screenshot('SnapShot/' + mode + '/' + str(index) + '.png')
        index += 1
        print(url + ":DONE")
    driver.close()

#endregion

def enum_shot_login(file):
    operation_login_tk(driver)
    urls = readUrlFile(file)
    filepath = "SnapUrl/input/"
    index = 0 #ログイン必要じゃない分だけ足す
    for url in urls:
        print(url)
        driver.get(url)
        click_pharmacy_list_item_title(driver)
        #el = WebAnalyze.get_input_tag(url)
        filename = filepath + last_url(url)
        input_page(filename,el,driver)
        index += 1

#ページ内の指定された要素に値を入力する関数
def input_page(filepath,element_list,driver):
    if os.path.exists(filepath):
        with open(filepath,'r') as f:
            input_list = f.read().split("\n")
    for el,input in zip(element_list,input_list):
        id = driver.find_elemnt_by_id(el)
        id.send_keys(input)

def operation_login_tk(driver,id,password):
    driver.get(login_dic[mode])
    singnin_btn = driver.find_element_by_class_name('user-menu')
    singnin_btn.click()
    sleep(5)
    print(driver.current_url)
    login_id = driver.find_element_by_id('logonIdentifier')
    login_id.send_keys(id)
    login_pass = driver.find_element_by_id('password')
    #ここにパスワード入れる
    login_pass.send_keys(password)
    login_btn =  driver.find_element_by_id('next')
    login_btn.click()
    sleep(10)

def operation_logout_tk(driver):
    driver.get('https://tk-dev-v3:dev100kg@v3.okp-tdk-dev.tk/')
    sleep(5)
    hamburger_btn = driver.find_element_by_class_name('gnav-button')
    hamburger_btn.click()
    sleep(5)
    logout_btn = driver.find_element_by_css_selector('.app-button.btn.gnav-login-button-logout')
    logout_btn.click()
    sleep(10)

#薬局を選ぶ
def click_pharmacy_list_item_title(driver):
    sleep(5)
    print(driver.current_url)
    pharmacy_btn = driver.find_elements_by_class_name('pharmacy-list-item')
    ActionChains(driver).move_to_element(pharmacy_btn).click(pharmacy_btn).perform()

#日付を選ぶ
def click_day_calendar(driver):
    days_btn = driver.find_element_by_css_selector('.text-field.date-input.success')
    days_btn.send_keys("2021-07-20")

#情報入力完了ボタン
def next_form(driver):
    next_btn = driver.find_element_by_css_selector('.commit-button.btn.btn--accent.commit-button-disabled')
    next_btn.click()

#性別選択ボタン
def gender_button(driver):
    gen_btn = driver.find_element_by_class_name('radio-label')
    gen_btn.click()

#URLの最後の部分だけをファイル形式にして抽出する関数
def last_url(url):
    target = '/'
    idx = url.rfind(target)
    targetfile = url[:idx]
    idx = targetfile.rfind(target) + 1 #スラッシュが入らないようにする
    targetfile = targetfile[idx:]
    return targetfile + ".txt"

def mode_select(mode):
    filepath = "SnapUrl/" + mode + "_url_list.txt"
    slowpath = "SnapUrl/" + mode + "_url_list_slow.txt"
    return filepath,slowpath


login_dic = {"dev": "https://tk-dev-v3:dev100kg@v3.okp-tdk-dev.tk/","stg":"https://todokusuriv3:kokusanbakuga100%@tk-stg-v3.todokusuri.work/","prd":"https:///todokusuri.com/"}
print("メールアドレス:")
id = input()
print("pass:")
password = input()
print("'dev' or 'stg' or 'prd'")
mode = input()
filepath,slowfile = mode_select(mode)
driver = webdriver.Chrome()


enum_shot(filepath,slowfile)
