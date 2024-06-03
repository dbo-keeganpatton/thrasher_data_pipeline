from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup 
import requests
import time


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
    # all questions are in <strong> tag or <em> tag
    # answers are in <br> tag

    questions = soup.find_all(['strong', 'em'])
    group = []
    
    
    for question in questions:

        import re 
        # This is to strip the tags for questions...
        # Because I could not figure out how to do it otherwise...
        
        remove_question_tags = re.compile('<.*?>')

        question_text = re.sub(
                remove_question_tags,
                "",
                question.text
        ) 

        print(question_text)
        next_br = question.find_next('br')
        
        answer = next_br.next_sibling
        
#        if isinstance(answer, str):
#            
#            group.append((question, answer))
#
#        
#    
#    print(group)
    break
    driver.back()
    counter += 1
     




        
           


