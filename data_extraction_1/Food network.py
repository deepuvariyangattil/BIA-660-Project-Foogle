
# coding: utf-8

# In[91]:


from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import time
import re


# In[65]:


# food network
def open_driver():
    global driver
    
    from selenium import webdriver

    #PROXY = "88.157.149.250:8080" # IP:PORT or HOST:PORT

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("headless")
    #chrome_options.add_argument('--proxy-server=%s' % PROXY)

    driver = webdriver.Chrome(executable_path='C:/Users/malik/Downloads/chromedriver_win32/chromedriver.exe', options = chrome_options)
    url = 'https://www.foodnetwork.com/topics/easy'
    driver.get(url)
    
open_driver()

# In[69]:


#Food network

def extract_urls():
    global urls
    urls = []
    num = input('how many pages should I crawl? (1 page -> 18 recipes) = ')
    num = int(num)
    for i in range (num):
        print('\nstarting page {}'.format(i+1))
        
        LINK_PAUSE_TIME = 3

        url_bf = driver.current_url
        r = requests.get(url_bf,headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(r.text, 'lxml')
    
        for info in soup.findAll("section", attrs={'class': 'o-RecipeResult o-ResultCard' }):
            for inf in info.findAll('h3', attrs={'class':'m-MediaBlock__a-Headline'}):
                for link in inf.findAll('a'):
                    urls.append('https:' + (link.get('href')))                                                                   
        
        # Navigate to next page
        n = soup.find("a", attrs={'class': 'o-Pagination__a-Button o-Pagination__a-NextButton' })
        next_link = 'https:' + n.get('href')        
        
        driver.get(next_link)
        
        # Wait to load page
        time.sleep(LINK_PAUSE_TIME)
        
extract_urls()

print('number of recipes: {}'.format(len(urls)))


# In[70]:


len(urls)


# In[71]:


#removing duplicates in urls if any
def Remove(duplicate): 
    final_list = [] 
    for num in duplicate: 
        if num not in final_list: 
            final_list.append(num) 
    return final_list

urls = Remove(urls)
len(urls)


# In[102]:


#Food Network

def data_extract():
    global df
    df = pd.DataFrame()
    df['Title'] = []
    df['Recipie'] = []
    df['Url'] = []
    url_err = []
    
    i = 1
    
    print('about to examine {} urls'.format(len(urls)))
    for ur_l in urls[1204:]:
        print('\nstarting url {}'.format(i))
        i+=1
        resp = []
        recipies = []
        titles = []
        options = webdriver.ChromeOptions()
        options.add_argument('headless')        
        options.add_argument("window-size=1400,600")
        prefs = {'profile.managed_default_content_settings.images':2}
        options.add_experimental_option("prefs", prefs)
        
        from fake_useragent import UserAgent
        ua = UserAgent()
        user_agent = ua.random
        
        options.add_argument(f'user-agent={user_agent}')
        
        r = requests.get(ur_l,headers={'User-Agent': 'Mozilla/5.0'})
        driver = webdriver.Chrome(chrome_options=options)
        driver.get(ur_l)
        
        soup = BeautifulSoup(r.content,'html.parser')
        soup_clean = soup.get_text().replace('\n','')        
        
        try:
            title = driver.find_element_by_class_name('o-AssetTitle__a-HeadlineText')
            titles.append(title.text)
            
            print('title.text: {}'.format(title.text))                  
            
            ingredients = re.findall(r'"recipeIngredient": \[(.*?)\],',soup_clean)[0].split('",')
            ingredients = [x.strip() for x in ingredients]
            ingredients = [x.strip('"') for x in ingredients]
            
            recipies.append(','.join(str(e) for e in ingredients))

            df = df.append({'Title':titles , 'Recipie':recipies, 'Url':ur_l} , ignore_index=True)
            driver.close()
            time.sleep(3)
        except TimeoutException:
            print('This url timed out: ', ur_l)
            url_err.append(ur_l)
            driver.close()
            time.sleep(20)
        except NoSuchElementException:
            print('cannot process this url: ', ur_l)     
        except:
            print('Unknown Error: ', ur_l)

        
data_extract()


# In[103]:


df['Recipie'] = df['Recipie'].str.get(0)
df['Title'] = df['Title'].str.get(0)
df = df[df.Recipie != '']
df


# In[104]:


df.to_csv('Food Network.csv', mode='a', header=False,index=False)

