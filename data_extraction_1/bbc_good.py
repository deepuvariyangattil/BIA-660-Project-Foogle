#importing Required Packages
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import time
from fake_useragent import UserAgent
import re

def open_driver():
    global driver

    from selenium import webdriver


    chrome_options = webdriver.ChromeOptions()

    driver = webdriver.Chrome(executable_path='C:/webdrivers/chromedriver.exe', options = chrome_options)
    global url
    url = 'https://www.bbcgoodfood.com/'
    driver.get(url)
open_driver()#opening a web driver

r = requests.get(url,headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(r.text, 'lxml')
print(r.status_code)

#extracting reciepes tab urls from BBCgoodfood
urls = []
for i in soup.findAll('li',attrs={'class':'expanded link-level-1 item-2 left-nav-info is-active'}):
    for ur_l in i.findAll('li',attrs={'class':['first leaf link-level-3 no-sub-level','leaf link-level-3 no-sub-level']}):
        for link in ur_l.findAll('a'):
            urls.append(link.get('href'))
print("extracting recipe tab urls completed")

#Formating acquired URLS
url_test = 'http://www.bbcgoodfood.com%s'
url_s=[]
url_c = []
for i in urls:
    if re.match('https://www.bbcgoodfood.com',i):
        print(i)
        url_c.append(i)
    else:
        url = url_test %i
        url_s.append(url)
urls=url_s+url_c
print("formating urls completed")

#acquiring the urls of all pages in each category
page_links = []
current = driver.current_url
time.sleep(5)
r = requests.get(current,headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(r.text, 'lxml')
for url in urls:
    driver.get(url)
    time.sleep(5)
    current = driver.current_url
    r = requests.get(current,headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(r.text, 'lxml')
    for pager in soup.findAll('li',attrs={'class':'pager-item'}):
        for link in pager.findAll('a'):
            page_links.append(link.get('href'))
            print(link.get('href'))
print("acquiring page link urls completed")

url_test = 'http://www.bbcgoodfood.com%s'

#Formating the page links
for i in page_links:
        url = url_test %i
        urls.append(url)
        print(url)
print("formating page link urls completed")

#acquruing titles and its urls from urls[]
titles = []
links = []
for i in urls:
    options = webdriver.ChromeOptions()
    options.add_argument("window-size=1400,600")
    prefs = {'profile.managed_default_content_settings.images':2}
    options.add_experimental_option("prefs", prefs)
    from fake_useragent import UserAgent
    ua = UserAgent()
    user_agent = ua.random
    print(user_agent)
    options.add_argument(f'user-agent={user_agent}')
    r = requests.get(i,headers={'User-Agent': 'Mozilla/5.0'})
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(i)
    soup = BeautifulSoup(r.text, 'lxml')
    try:
        for link in soup.findAll('h3',attrs={'class','teaser-item__title'}):
            for info in link.findAll('a'):
                titles.append(info.text)
                print(info.text)
                links.append(info.get('href'))
        driver.close()
        time.sleep(5)
    except:
        print('unknown error ', i)
print("extraction of titles and recipe urls complete...!")

print("checking and removing duplicates.....")
def Remove(duplicate):
    final_list = []
    for num in duplicate:
        if num not in final_list:
            final_list.append(num)
        else:
            print(num)
    return final_list
#removing duplicate titles if any
final_titles = Remove(titles)
len(final_titles)
print("finished..!!")

#creating a pandas Dataframe and inserting aquired titles and thier corresponding urls
df = pd.DataFrame()
df['Title'] = titles
df['Urls'] = links
df = df.drop_duplicates(subset='Title')
len(df)

#preprocesing urls in pandas DataFrame
url_test = 'http://www.bbcgoodfood.com%s'
df_urls = []
for i in df['Urls']:
    url = url_test %i
    df_urls.append(url)
    print(url)

df['Urls'] = df_urls
print("sample of DataFrame")
df.head()

#extracting recipes from each url and inserting them in to the pandas DataFrame
print("extracting ingredients from recipe urls")
x=0
final_resp = []
for i in df['Urls']:
    recipes = []
    options = webdriver.ChromeOptions()
    options.add_argument("window-size=1400,600")
    prefs = {'profile.managed_default_content_settings.images':2}
    options.add_experimental_option("prefs", prefs)
    from fake_useragent import UserAgent
    ua = UserAgent()
    user_agent = ua.random
    print(user_agent)
    options.add_argument(f'user-agent={user_agent}')
    #options.add_argument("--headless")
    r = requests.get(i,headers={'User-Agent': 'Mozilla/5.0'})
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(i)
    soup = BeautifulSoup(r.text, 'lxml')
    try:
        for resp in soup.findAll('li',attrs={'class':'ingredients-list__item'}):
            recipes.append(resp.get('content'))
            print(resp.get('content'))
        final_resp.append(recipes)
        driver.quit()
        time.sleep(10)
    except TimeoutException:
        print(i)
        final_resp.append('')
        time.sleep(20)
        driver.quit()
    except:
        print('unknown error')
        final_resp.append('error')
        time.sleep(10)
        driver.quit()
print("finished...!!!")

df['Recipe'] = final_resp
final_df = df[['Title', 'Recipe','Urls']]
final_df.to_csv('BBCgood_data.csv', mode='a', header=True,index=False)
print("sample of final_df")
final_df.head()
print("Dataframe is saved")
