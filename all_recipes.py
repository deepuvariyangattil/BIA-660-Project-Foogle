#importing Required Packages
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import time
from fake_useragent import UserAgent

#starting a chrome driver
def open_driver():
    global driver

    from selenium import webdriver



    chrome_options = webdriver.ChromeOptions()


    driver = webdriver.Chrome(executable_path='C:/webdrivers/chromedriver.exe', options = chrome_options)
    url = 'https://www.allrecipes.com/recipes/'
    driver.get(url)

open_driver()

# CATEGORIES:
#
# Breakfast and Brunch
# Desserts
# Dinners
# Lunch
# Beef
# Beans and Legumes
# Chicken Recipes
# Chocolate
# Fruit
# Game Meats
# Grains
# Mushrooms
# Pasta
# Pork Recipes
# Potatoes
# Poultry
# Rice
# Salmon
# Seafood
# Shrimp
# Tofu and Tempeh
# Turkey
# Vegetable Recipes
# Diabetic
# Low Carb Recipes
# Dairy Free Recipes
# Gluten Free
# Healthy
# Heart-Healthy Recipes
# High Fiber Recipes
# Low Calorie
# Low Cholesterol Recipes
# Low Fat
# Weight-Loss Recipes
# 4th of July
# Baby Shower
# Birthday
# Christmas
# Christmas Cookies
# Cinco de Mayo
# Easter Recipes
# Football
# Halloween
# Hanukkah
# Mother's Day
# New Year
# Passover
# Ramadan
# St. Patrick's Day
# Thanksgiving
# Valentines Day
# More Holidays and Events
# Appetizers & Snacks
# Bread Recipes
# Cake Recipes
# Candy and Fudge
# Casserole Recipes
# Christmas Cookies
# Cocktail Recipes
# Cookie Recipes
# Mac and Cheese Recipes
# Main Dishes
# Pasta Salad Recipes
# Pasta Recipes
# Pie Recipes
# Pizza
# Sandwiches
# Sauces and Condiments
# Smoothie Recipes
# Soups, Stew, and Chili Recipes
# BBQ & Grilling
# Budget Cooking
# Clean-Eating
# Cooking for Kids
# Cooking for Two
# Gourmet
# Paleo
# Pressure Cooker
# Quick & Easy
# Slow Cooker
# Vegan
# Vegetarian
# Chinese
# Indian
# Italian
# Mexican
# Southern
# Thai
# All World Cuisine
# Allrecipes Magazine Recipes
# Food Wishes with Chef John
# Entertaining and Dinner Parties
# All Trusted Brands

def Enter_Topic():
    Topic = input('enter category ')
    print(Topic)
    Topic_link = driver.find_element_by_link_text(Topic)
    Topic_link.click()
Enter_Topic()#enter the category you are interested in scraping the data

def extract_urls():
    global urls
    urls = []
    num = input('how many iterations you want(1 iteration--->5 pages--->around 50 urls) = ')
    num = int(num)
    for i in range (0,num):
        import time
        SCROLL_PAUSE_TIME = 10

    # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            url_bf = driver.current_url
            r = requests.get(url_bf,headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(r.text, 'lxml')
            print(r.status_code)

            for info in soup.findAll("div", attrs={'class': 'fixed-recipe-card__info' }):
                for inf in info.findAll('h3', attrs={'class':'fixed-recipe-card__h3'}):
                    for link in inf.findAll('a'):
                        urls.append(link.get('href'))



            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break

            last_height = new_height
        button = driver.find_element_by_xpath('//*[@id="btnMoreResults"]') # Selector might differs
        button.location_once_scrolled_into_view
        button.click()
extract_urls() #extracting the urls of the category

len(urls)

#removing duplicates in urls if any
def Remove(duplicate):
    final_list = []
    for num in duplicate:
        if num not in final_list:
            final_list.append(num)
    return final_list

urls = Remove(urls)
len(urls)


def data_extract():
    global df
    df = pd.DataFrame()
    df['Title'] = []
    df['Recipie'] = []
    df['Url'] = []
    url_err = []

    for ur_l in urls:
        resp = []
        recipies = []
        titles = []
        options = webdriver.ChromeOptions()
        options.add_argument("window-size=1400,600")
        prefs = {'profile.managed_default_content_settings.images':2}
        options.add_experimental_option("prefs", prefs)
        ua = UserAgent()
        user_agent = ua.random
        print(user_agent)
        options.add_argument(f'user-agent={user_agent}')
        r = requests.get(ur_l,headers={'User-Agent': 'Mozilla/5.0'})
        driver = webdriver.Chrome(chrome_options=options)
        driver.get(ur_l)
        soup = BeautifulSoup(r.text, 'lxml')
        try:
            title = driver.find_element_by_xpath('//*[@id="recipe-main-content"]')
            titles.append(title.text)
            for r in soup.findAll('span',attrs={'class':'recipe-ingred_txt added'}):
                resp.append(r.text)
            recipies.append(','.join(str(e) for e in resp))
            print(title.text)
            df = df.append({'Title':titles , 'Recipie':recipies, 'Url':ur_l} , ignore_index=True)
            driver.close()
            time.sleep(10)
        except TimeoutException:
            print('This url ', ur_l)
            url_err.append(ur_l)
            driver.close()
            time.sleep(20)
        except NoSuchElementException:
            print('cannot process this url ', ur_l)
        except:
            print('Unknown Error ', ur_l)


data_extract() #extraction of title and ingredients of each url

#creating a pandas Dataframe
df['Recipie'] = df['Recipie'].str.get(0)
df['Title'] = df['Title'].str.get(0)
df = df[df.Recipie != '']
df

#only for initial use if the csv already contains data skip the following LINE
df.to_csv('AR_data.csv', mode='a', header=True,index=False)

df.to_csv('basic_data.csv', mode='a', header=False,index=False)
