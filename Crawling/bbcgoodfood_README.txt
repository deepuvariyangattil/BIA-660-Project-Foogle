@author - Vishal 
Github - vishalp7
email - vishal.pgs@gmail.com
**********************bbcgoodfood**********************
"bbc_good.py"this file contains the crawling code and scraping code for "bbcgoodfood" website
i have used primarily beautifulsoup and selenium for making it work.

in bbcgoodfood.com there is a tab called recipes where there are all subcategories I visit each of those links and extract all the URLs in those links.
after getting the URL links for the subcategories I visit each URL and check if there are any page links(navigation URLs) within them and extract those URLs too.
after acquiring the final set of urls I visit each URL and obtain title and ingredients needed of the recipe and form a CSV file using pandas.
I have written comments in the code for better understanding.you can track the process (i have added print statements for the notifications)