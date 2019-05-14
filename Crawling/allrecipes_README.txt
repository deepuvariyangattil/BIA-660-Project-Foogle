@author - Vishal 
Github - vishalp7
email - vishal.pgs@gmail.com
*********************All Recipes**********************
"all_recipes.py" this file contains the crawling code and scraping code for "all recipes" website
i have used primarily beautifulsoup and selenium for making it work.

I have designed the code in such a way that the user can give the topic name(for list of available topic names you can see the code where its commented) and the crawler will start extracting URLs of the recipes
and later it will visit each of the extracted URLs to fetch title and ingredients for that recipe. After the successful running of code, you will have the data ready in a CSV file. I have written comments in the code for better understanding.
you can track the process (i have added print statements for the notifications)