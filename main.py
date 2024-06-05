from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium import webdriver
from sqlalchemy import insert
from bs4 import BeautifulSoup 
import requests
import pandas as pd
import time
import re


# Selenium Automations
thrasher_site = 'https://www.thrashermagazine.com/articles-and-interviews/'
driver = webdriver.Firefox()
driver.get(thrasher_site)
actions = ActionChains(driver)


# Resusable Vars
scroll_page = "window.scrollTo(0, document.body.scrollHeight);"
page_height = "return document.body.scrollHeight"
last_height = page_height
item_target_count = 10
counter = 0


# The script will loop through articles...
# Creating dicts of questions and answers...
# Then append each dict in this list...
articles_data = []


# Thrasher Articles Site is an infinite scroll...
# Iterate through each link as the page scrolls...
# Up to the number of clicks specified by [item_target_count]...
while counter < item_target_count:
    
    ###################
    ### Automations ###
    ###################
    
    driver.execute_script(scroll_page)
    time.sleep(2)
    new_height = driver.execute_script(page_height)
   
    if new_height == last_height:
        break 
    last_height = new_height 
    
    element = driver.find_element(By.CSS_SELECTOR, 'a.post-title-link')    
    link = element.get_attribute('href')
    
    driver.get(f'{link}')
    

    ###################
    # Content Scrape  #
    ###################
    
    http_req = requests.get(f'{link}')
    soup = BeautifulSoup(http_req.content, 'html.parser')

    # div.article-text
    # div.body-text
    # all questions are in <strong> tag or <em> tag...
    # answers are set between following <br> tags...
    title = soup.find('h3') 
        

    questions = soup.find_all(['strong', 'em'])
    
    for question in questions:

        # This is to strip the tags for questions...
        # Because I could not figure out how to do it otherwise...
        remove_question_tags = re.compile('<.*?>')
        question_text = re.sub(remove_question_tags, "", question.text) 
        
        
        next_br = question.find_next('br')
        answer = next_br.next_sibling

        # Make sure that the following sibling is actually text...
        # Then create dicts stored in our list for later...
        if isinstance(answer, str):
            
            articles_data.append({
                "title" : title,
                "question" : question_text,
                "answer" : answer
            })

    




#####################
# Data Prep for ORM #
#####################
df = pd.DataFrame(articles_data)
print(df.head())
print(df.columns)
