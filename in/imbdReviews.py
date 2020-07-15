import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import time

#Ask the user for the movie they would like to watch.
movie = input("What movie or tv shows do you want to watch? : ")

# Set the web browser to chrome.
driver = webdriver.Chrome()

# Uses Get Method to go to google.
driver.get("https://www.google.com/")

#Enter the keyword for finding the movie.
driver.find_element_by_name("q").send_keys(movie + " imbd")
time.sleep(1)

#Clicks the google search button 
driver.find_element_by_name("btnK").send_keys(Keys.ENTER)
time.sleep(1)

#Click the first URL shown, given a search page.
driver.implicitly_wait(1)
driver.find_element_by_class_name("r").click()
driver.implicitly_wait(1)

#Go to the user reviews page

driver.find_elements_by_xpath("/html/body/div[2]/div/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/a[3]")

#Use B.S to scrap the IMBD review page
ans = driver.current_url
page = requests.get(ans)
soup = BeautifulSoup(page.content, "html.parser")
all = soup.find(id="main")

#Scrap imbd Review
parent = soup.find(class_="parent")
name = soup.find(itemprop = "name")
url = soup.find(itemprop = 'url')
film_title = soup.get_text()

# Get the title of the review
title_rev = all.select(".title")
title = [t.get_text().replace("\n", "") for t in title_rev]

#Get the review itself
review_rev = all.select(".content .text")
review = [r.get_text() for r in review_rev]

#Turn it into a dataframe
table_review = pd.DataFrame({
    "Title" : title,
    "Review" : review
})

#Actual Review Analysis Time :p
analyser = SentimentIntensityAnalyzer()
sentiment1 = []
sentiment2 = []

for rev in review:
    score1 = analyser.polarity_scores(rev)
    com_score = score1.get('Compound')
    if com_score >= 0.05:
        sentiment1.append('Positive')
    elif com_score > -0.05 and com_score < 0.05:
        sentiment1.append('Neutral')
    elif com_score <= -0.05:
        sentiment1.append('Negative')
table_review['Sentiment Vader'] = sentiment1

#TextBlob
for rev in review:
    score2 = TextBlob(rev).sentiment.polarity
    if score2 >= 0:
        sentiment2.append('Positive')
    else:
        sentiment2.append('Negative')
#Print spammage :/ 
print(f"The movie title is {film_title}")
print("")
print("According to vadersentiemnt, you should :")
if sentiment1.count('Positive') > sentiment1.count('Negative'):
    print('WATCH IT!')
else:
    print("DON'T WATCH IT...")
print('Positive : ', sentiment1.count('Positive'))
print('Negative : ', sentiment1.count('Negative'))
print("")
print("According to TextBlob, you should :")
if sentiment2.count('Positive') > sentiment2.count('Negative'):
    print('WATCH IT!')
else:
    print("DON'T WATCH IT...")
print('Positive : ', sentiment2.count('Positive'))
print('Negative : ', sentiment2.count('Negative'))

#Close the browser
driver.close()