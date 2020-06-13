import time
import sys
import os
from urllib.request import urlopen

try_import("from googletrans import Translator", "googletrans")
try_import("from apscheduler.schedulers.background import BackgroundScheduler", "apscheduler")
try_import("from selenium import webdriver;from selenium.webdriver.common.keys import Keys; from selenium.common.exceptions import TimeoutException", "selenium")
try_import("from webdriver_manager.chrome import ChromeDriverManager", "webdriver-manager")
try_import("from googletrans import Translator", "googletrans")  
try_import("from bs4 import BeautifulSoup", "beautifulsoup4")
    
def try_import(instruction, package_name):
    try:
        exec(instruction)
    except ModuleNotFoundError:
        !pip install --upgrade pip
        !pip install $package_name
                 
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko")
browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
browser.set_window_size(1024, 768)
        
keyword = input("Insert keyword: ")

url_dict = {}
url_dict['google'] = f"https://www.google.com/search?q={keyword}&tbm=isch"
url_dict['youtube'] = f"https://www.youtube.com/results?search_query={keyword}"
url_dict['yahoo_japan'] = f"https://search.yahoo.co.jp/image/search;_ylt=A2RCMZH6NuNezlMAoQyU3uV7?p={keyword}&aq=-1&oq=&ei=UTF-8"
url_dict['daum'] = f"https://search.daum.net/search?w=img&&q={keyword}"
url_dict['naver'] = f"https://search.naver.com/search.naver?where=image&query={keyword}"

translator = Translator()
chinese = translator.translate(keyword, dest='zh-cn').text
url_dict['bidu'] = f"http://image.baidu.com/i?tn=baiduimage&word={chinese}"

file = open("src_list.txt", "a")
file.close()
file = open("src_list.txt", "r")
src_list = [src_name.strip() for src_name in file.readlines()]
for web_site, url in url_dict.items():
    try:
        browser.get(url)
    except TimeoutException:
        print(f"TimeoutException has been thrown: {web_site}")
        continue
    time.sleep(1)
    element = browser.find_element_by_tag_name("body")
    for i in range(30):
        element.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.3)
    source = browser.page_source
    bs_object = BeautifulSoup(source,"html.parser")
    img_data = bs_object.find_all("img")
    animation = ""
    for i, ele in enumerate(img_data):
        animation = f"{web_site} crawling : {i+1}/{len(img_data)}"
        print(animation, end="\r")
        try:
            with open("src_list.txt", "a") as file:
                if ele.attrs['src'] not in src_list:
                    file.write(ele.attrs['src']+"\n")
                    src_list.append(ele.attrs['src'])
                    t = urlopen(ele.attrs['src']).read()
                else:
                    continue
        except:
            continue
        if not os.path.isdir(f"./{web_site}"):
            os.mkdir(f"./{web_site}")
        filename = f"./{web_site}/{web_site}_{i}.jpg"
        with open(filename, "wb") as f:
            f.write(t)
    print()
browser.close()
