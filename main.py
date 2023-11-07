import requests
import warnings
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import random

warnings.filterwarnings("ignore", category=DeprecationWarning)

# Function to select a random proxy server from the provided dictionary
def selectRandom(proxy_servers):
    return random.choice(list(proxy_servers.values()))

# Main function
def main():
    print("Copyright (c) 1998-2023")
    print("Brian Oost")
    print("All rights reserved.")
    print("https://brianoost.com/")
    
    print('')

    # Dictionary containing proxy server options
    proxy_servers = {
        1: "https://www.blockaway.net",
        2: "https://www.croxyproxy.com",
        3: "https://www.croxyproxy.rocks",
        4: "https://www.croxy.network",
        5: "https://www.croxy.org",
        6: "https://www.youtubeunblocked.live",
        7: "https://www.croxyproxy.net",
    }

    # Prompting the user to select a proxy server
    print("Please select a proxy server (1-7). 1 is recommended:")
    proxy_choice = int(input("> "))  # User selects a proxy server by entering a number
    proxy_url = proxy_servers.get(proxy_choice)  # Retrieve the URL of the selected proxy server

    twitch_username = input("Enter your channel name (e.g., Asmongold): ")  # User enters their Twitch channel name
    proxy_count = int(input("Amount of viewers to create: "))  # User specifies the number of proxy sites to open

    print("Creating virtual viewers now... Please wait.")
    
    # Set the path to the geckodriver executable (download geckodriver from Mozilla's website)
    geckodriver_path = '/usr/local/bin/geckodriver'  # Replace with the actual path to geckodriver

    firefox_options = webdriver.FirefoxOptions()
    firefox_options.add_argument("--headless")
    firefox_options.set_preference("media.volume_scale", "0.0")  # Mute audio
    firefox_options.set_preference("intl.accept_languages", "en-US")  # Set language to English
    firefox_options.set_preference("dom.webdriver.enabled", False)  # Disable webdriver detection

    firefox_service = FirefoxService(geckodriver_path)
    driver = webdriver.Firefox(service=firefox_service, options=firefox_options)

    counter = 0  # Counter variable to keep track of the number of drivers created

    # Loop to create virtual viewers using different proxy servers
    for i in range(proxy_count):
        try:
            random_proxy_url = selectRandom(proxy_servers)  # Select a random proxy server for this tab
            driver.execute_script("window.open('" + random_proxy_url + "')")
            driver.switch_to.window(driver.window_handles[-1])
            driver.get(random_proxy_url)

            text_box = driver.find_element(By.ID, 'url')
            text_box.send_keys(f'www.twitch.tv/{twitch_username}')
            text_box.send_keys(Keys.RETURN)
            
            # Wait for the element to be present before proceeding
            element_xpath = "//div[@data-a-target='player-overlay-click-handler']"
            wait = WebDriverWait(driver, 30)  # Adjust the timeout as needed
            element = wait.until(EC.presence_of_element_located((By.XPATH, element_xpath)))

            # Continue with your actions on the element
            actions = ActionChains(driver)
            actions.move_to_element(element).perform()

            time.sleep(15)  # If you need to wait after interacting with the element

            counter += 1  # Increment the counter for each driver created
            print(f"Virtual viewer {counter}/{proxy_count} spawned.")  # Print the counter and total count

        except WebDriverException as e:
            print("An error occurred while spawning a virtual viewer (Firefox driver):")
            print(e)
            break  # Exit the loop if an exception occurs

    input('All viewers have been created, press <CTRL+C> to exit this application when done streaming.\n')
    
    driver.quit()  # Close the Firefox webdriver

if __name__ == '__main__':
    main()
