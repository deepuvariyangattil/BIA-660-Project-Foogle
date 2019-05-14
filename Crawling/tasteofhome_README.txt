@author - Vishal 
Github - vishalp7
email - vishal.pgs@gmail.com
**********************Taste of Home**********************
"taste_of_home.py" this file contains the crawling code and scraping code for "tasteofhome" website.
i have used primarily beautifulsoup and selenium for making it work.

taste of home website is pretty straight forward going to the recipe page in taste of home has page navigation till 1686 pages(you can change the page number in the code if you want to extract fewer pages).
I go to each page extracting URLs and then visit each URL to extract title and ingredients for the recipe and form a CSV file using pandas.
I have written comments in the code for better understanding.you can track the process (i have added print statements for the notifications)