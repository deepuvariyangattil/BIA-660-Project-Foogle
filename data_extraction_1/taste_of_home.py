#importing Required Packages
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from fake_useragent import UserAgent
import time
import re

def open_driver():
    global driver

    from selenium import webdriver


    chrome_options = webdriver.ChromeOptions()

    driver = webdriver.Chrome(executable_path='C:/webdrivers/chromedriver.exe', options = chrome_options)
    global url
    url = 'https://www.tasteofhome.com/recipes/'
    driver.get(url)

open_driver()#starting a chrome driver

r = requests.get(url,headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(r.text, 'lxml')

#extracting urls from each page in" Taste of Home"
urls = []
p_a = 0
for pages in range(0,1687):#total number of recipe pages in "Taste of Home" 1686
    time.sleep(5)
    current = driver.current_url
    r = requests.get(current,headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(r.text, 'lxml')
    for i in soup.findAll('li',attrs={'class':'single-recipe'}):
        for links in i.findAll('a'):
            urls.append(links.get('href'))
    print(p_a)
    p_a = p_a+1
    Page_link = driver.find_element_by_link_text('Next Page')
    Page_link.click()

len(urls)

def Remove(duplicate):
    final_list = []
    for num in duplicate:
        if num not in final_list:
            final_list.append(num)
    return final_list
#removing duplicate urls
urls = Remove(urls)
len(urls)

#extracting title and ingredients from each urls
recipes = []
defe_url = []
titles = []
ite = 0
for url in urls:
    resp=[]
    options = webdriver.ChromeOptions()
    options.add_argument("window-size=1400,600")
    prefs = {'profile.managed_default_content_settings.images':2}
    options.add_experimental_option("prefs", prefs)
    ua = UserAgent()
    user_agent = ua.random
    #print(user_agent)
    options.add_argument(f'user-agent={user_agent}')
    r = requests.get(url,headers={'User-Agent': 'Mozilla/5.0'})
    driver = webdriver.Chrome(chrome_options=options)
    try:
        driver.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        if soup.findAll('b',attrs={'class':'sIngredient'}):
            print('This has a subingredient ', url)
            resp.append('This has a subingredient')
            titles.append('IGNORE THIS')
            defe_url.append(url)
            driver.quit()
            continue
        for t in soup.findAll('h1',attrs={'class':'recipe-title'}):
            titles.append(t.text)
            print(t.text)
        for i in soup.findAll('div',attrs={'class':'recipe-ingredients'}):
            for t in i.findAll('li'):
                resp.append(t.text)
        recipes.append(resp)
        driver.quit()
        print(ite)
        ite = ite+1
        time.sleep(5)
    except NoSuchElementException:
        print('its an article ', url)
        defe_url.append(url)
        resp.append('Its an Article')
        titles.append('IGNORE THIS')
        driver.quit()
        time.sleep(5)
    except TimeoutException:
        print('took long time to load page ', url)
        defe_url.append(url)
        resp.append('Took Long Time to LOAD')
        titles.append('IGNORE THIS')
        driver.quit()
        time.sleep(10)

#inserting aquired data in pandas DataFrame
df = pd.Dataframe()
df['Title'] = titles
df['Recipie'] = recipes
df['Url'] = urls
df = df[df.Title != 'IGNORE THIS']

final_df = df[['Title', 'Recipe','Url']]

final_df.to_csv('T_O_h.csv',header=True,index=False)
