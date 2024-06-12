from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import pandas as pd
import sys
sys.path.append('/home/eyelady/projects/python_projects/thrasher_site/')
from site_utils import scroll_page, scrape_data # UDF Imports


#####################
#  Core Variables   #
#####################

thrasher_site = 'https://www.thrashermagazine.com/articles-and-interviews/'
driver = webdriver.Firefox()
driver.get(thrasher_site)
actions = ActionChains(driver)


# Resusable Vars
scroll_page_cmd = "window.scrollTo(0, document.body.scrollHeight/ 5);"
page_height = "return document.body.scrollHeight"
item_target_count = 20
counter = 0


# The script will loop through articles...
# Creating dicts of questions and answers...
# Then append each dict in this list...
articles_data = []


# This keeps track of what we have seen in the loop...
# After each click that link will be added to this set..
clicked_links = set()



#####################
#   Extract Logic   #
#####################

# Limit this by the target count, otherwise it will run infinitely...
# Each Iteration of this loop will increment to that point...
while counter < item_target_count: 
    
    elements = scroll_page(driver=driver, page_height=page_height, scroll_page_cmd=scroll_page_cmd)    

    try:
        for element in elements:
            try:

                # Look for each clickable title link
                link = element.get_attribute('href')
                
                # clicked_links is to help with redundancy between iterations...
                # This was not a problem, just for incase the redirect does something weird...
                if link not in clicked_links:
                    clicked_links.add(link)
                    driver.get(f'{link}')
                    
                    scrape_data(link=f'{link}', lst=articles_data)
                    driver.back()    
                    counter+=1    
                    print(counter)
                    
                    if counter >= item_target_count:
                        break
            # Not really sure why I two try/excepts work...
            # But it works and I was running into insurmountable stale elements...
            except (StaleElementReferenceException, NoSuchElementException):
                    continue  

    except TimeoutException:
            continue
            


#####################
# Data Prep for ORM #
#####################
df = pd.DataFrame(articles_data)
df.to_csv('./data/data.csv')
driver.close()
