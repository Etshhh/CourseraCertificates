# from apis import Driver

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from confidentials import email, password
import time

# Recommend reading the main function first.

def do_work():
    # Wait for the decision to be present and fetch the element
    # (the 1 sec delay is just to be safe)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='rc-LoggedInHome-CourseCards css-w3ukyh']")))
    time.sleep(1)
    cards_div = driver.find_element_by_xpath("//div[@class='rc-LoggedInHome-CourseCards css-w3ukyh']")
    cards = cards_div.find_elements_by_xpath("div")

    # Scroll a bit down so you can see them
    driver.execute_script("window.scrollTo(0, 320)")

    # Select the cards again if found there length to be zero
    while len(cards) == 0:
        cards_div = driver.find_element_by_xpath("//div[@class='rc-LoggedInHome-CourseCards css-w3ukyh']")
        cards = cards_div.find_elements_by_xpath("div")

    # Iterate over the cards (each being a certificate)
    for card in cards:
        # Click on the View Certificate button
        WebDriverWait(card, 4).until(EC.presence_of_element_located((By.LINK_TEXT, 'View Certificate'))).click()

        # Switch to the certificate's window tab
        windows = driver.window_handles
        driver.switch_to_window(windows[1])

        # Click on the download button
        download_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Download Certificate')]/..")))
        download_btn.click()

        # Click on download the pdf
        try:
            WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.LINK_TEXT, 'click here to download the PDF file.'))).click()
        except:
            WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.LINK_TEXT, 'click here to download the PDF file.'))).click()

        # Close the tab and return to the main tab
        driver.close()
        driver.switch_to_window(windows[0])

    # Find the 'next page' button
    # Click the button and return True if it is enabled
    next_btn = driver.find_element_by_xpath("//button[@aria-label='Next Page']")
    attr = next_btn.get_attribute('class')
    if (attr.find('disabled') == -1):
        next_btn.click()
        return True

    return False
    

if __name__ == '__main__':

    # Specify chrome options to disable logging messages and enable direct pdf download
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_experimental_option("prefs", {
        "download.default_directory": r"D:\DP\certs",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        "plugins.always_open_pdf_externally": True,
        })
    
    # Create driver and maximize window
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    
    # Go to the Coursera websit and click log in
    driver.get("https://www.coursera.org/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Log In"))).click()

    # Fill in the login credentials and log in.
    email_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email")))
    email_box.send_keys(email)
    
    password_box = driver.find_element_by_id('password')
    password_box.send_keys(password)
    
    login_btn = driver.find_element_by_xpath("//button[contains(text(), 'Login')]")
    login_btn.click()

    # Let the user manually pass the robot test for the code to continue
    input('Please authenticate the log in.')
    print('thanks!')
    
    # Close the pop up window, in case it opens up (maybe change the 2 seconds to a bigger number if takes longer to show)
    try:
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Skip')]"))).send_keys('\n')
    except:
        pass

    # Open the "Complete" tab
    driver.find_element_by_link_text('Completed').click()

    # Iterate over the pages of the "Completed" tab
    is_next = True
    while(is_next):
        is_next = do_work()
