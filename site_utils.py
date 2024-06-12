from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup 
import requests
import time
import re




def get_web_elements(driver):
    """Locate all instances of <a> tags indicating an article title.
    :Inputs: a selenium Web Driver
    """ 
    
    return WebDriverWait(driver, 2).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, 'a.post-title-link')
        )
    )




def scroll_page(driver, page_height,  scroll_page_cmd):
    """Navigate an infinite scroll page and retrieve html elements
    incrementally.

    :param driver: A Selenium Web Driver
    :param page_height: JS Selenium input as {return document.body.scrollHeight}
    :param scroll_page_cmd:JS Selenium input as {window.scrollTo(0, document.body.scrollHeight);}
    """

    driver.execute_script(scroll_page_cmd)
    time.sleep(2)

    last_height = page_height
    new_height = driver.execute_script(page_height)
    
    if new_height == last_height:
        return None 
    last_height = new_height

    return get_web_elements(driver)




def scrape_data(link, lst):
    """Iterates through a webpage, looking for <strong> and <em> tags,
    then finds the next <br> tag, to locate the text sibling. A check
    is performed to ensure that text is indeed found as a {str}.
    Creates an array of dicts.

    :param link: Web Page URL.
    :param lst: Provide an empty array to append results to.
    """

    http_req = requests.get(f'{link}')
    soup = BeautifulSoup(http_req.content, 'html.parser')
    title = soup.find('h3') 
    questions = soup.find_all(['strong', 'em'])
    
    for question in questions:

        try:
            # This is to strip the tags for questions...
            # Because I could not figure out how to do it otherwise...
            remove_question_tags = re.compile('<.*?>')
            question_text = re.sub(remove_question_tags, "", question.text) 
            
            
            next_br = question.find_next('br')
            answer = next_br.next_sibling

            # Make sure that the following sibling is actually text...
            # Then create dicts stored in our list for later...
            if isinstance(answer, str):
                
                lst.append({
                    "title" : title,
                    "question" : question_text,
                    "answer" : answer
                })
        
        except Exception as e:
            print(f"error is {e}")
            continue

