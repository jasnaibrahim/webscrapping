from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_actor_filmography(actor_name):
    try:
        # Initialize the WebDriver
    
        driver = webdriver.Chrome()
        driver.get("https://www.imdb.com")

        # Search for the actor
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        search_box.send_keys(actor_name)
        search_box.send_keys(Keys.RETURN)


        # Click on the first result in "People" section
        first_result = driver.find_element(By.CSS_SELECTOR, "li.find-name-result:nth-child(1) > div:nth-child(2) > div:nth-child(1)")
        first_result.click()

        # Scroll down to ensure the filmography section is fully loaded
        driver.execute_script("window.scrollTo(0, 800);")
        time.sleep(2)  # Additional wait for all content to load

        # Locate the "See All" button
        see_all = driver.find_element(By.CSS_SELECTOR, "button.ipc-btn--single-padding")

       # Scroll to the "See All" button
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", see_all)
        time.sleep(3)  # Add a short delay

        try:
           # Attempt to click the button using JavaScript if normal click fails
            see_all.click()
        except:
             driver.execute_script("arguments[0].click();", see_all)
        time.sleep(5)
        filmography = []
       

        try:   
            titles = driver.find_elements(By.XPATH,'//a[@class="ipc-metadata-list-summary-item__t"]')
            title = [title.text for title in titles if title.text!=""]  # Extract text from each title element

            for i in range(len(title)):
                  filmography.append(title[i]) 
        except Exception as inner_e:
            print(f"Error extracting film info: {inner_e}")
           

     
        # Print the filmography
        print(f"\nFilmography for {actor_name} (sorted in descending order):")
        for movie in filmography:
            print(f"{movie}")

    except Exception as e:
        print("An error occurred:", e)
    finally:
        driver.quit()

# Take actor name as input
actor_name = input("Enter the name of the actor: ")
get_actor_filmography(actor_name)
