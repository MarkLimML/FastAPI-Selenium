from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

def createDriver() -> webdriver.Chrome:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    prefs = {"profile.managed_default_content_settings.images":2}
    chrome_options.headless = True


    chrome_options.add_experimental_option("prefs", prefs)
    myDriver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    return myDriver

def getGoogleHomepage(driver: webdriver.Chrome) -> str:
    driver.get("https://www.google.com")
    return driver.page_source

def doBackgroundTask(inp):
    print("Doing background task")
    print(inp.msg)
    print("Done")

def doSiteCheck(url):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)

    driver.get(url)

    CheckSite = ""
    CheckReason = []
    #Check for site if link is correct
    titlechk = "'क्लास सेंट्रल • सर्वश्रेष्ठ पाठ्यक्रम खोजें, चाहे वे कहीं भी हों।'"
    titlechk2 = "कक्षा केंद्रीय • सर्वोत्तम पाठ्यक्रम खोजें, जहां भी वे मौजूद हैं।"

    if driver.title != titlechk or driver.title != titlechk2:
        CheckSite = "Fail"
        CheckReason.append("Wrong Page")

    #Check for top left dropdown functionality
    nav_element = driver.find_element(By.XPATH,'//*[@id="page-home"]/div[1]/header/div[1]/nav/div[1]')
    nav_element2 = driver.find_element(By.XPATH,'//*[@id="page-home"]/div[1]/header/div[1]/nav/div[2]')
    nav_element3 = driver.find_element(By.XPATH,'//*[@id="page-home"]/div[1]/header/div[1]/nav/div[2]/div')
    print(nav_element.get_attribute('class'))
    print(nav_element2.get_attribute('class'))
    
    action = ActionChains(driver)
    action.move_to_element(nav_element).perform()

    wait = WebDriverWait(driver, 3)
    wait.until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="page-home"]/div[1]/header/div[1]/nav/div[1]/nav')))

    if 'main-nav-dropdown js-main-nav-dropdown is-open' != driver.find_element(By.XPATH,'//*[@id="page-home"]/div[1]/header/div[1]/nav/div[1]/nav').get_attribute('class'):
        CheckSite = "Fail"
        CheckReason.append("Javascript dropdown not working properly")

    action.move_to_element(nav_element2)
    action.perform()

    wait.until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="page-home"]/div[1]/header/div[1]/nav/div[2]/div')))

    
    if 'animate-fade-entered bg-white z-top absolute width-1-3 border-all border-gray-light shadow-light padding-medium' !=  driver.find_element(By.XPATH,'//*[@id="page-home"]/div[1]/header/div[1]/nav/div[2]/div').get_attribute('class'):
        CheckSite = "Fail"
        CheckReason.append("Javascript dropdown not working properly")

    #Check for site image are high resolution
    images = driver.find_elements(By.TAG_NAME,'img')

    for img in images:
        src = img.get_attribute('src')
        print(src)
        if "blur" in src:
            CheckSite = "Fail"
            CheckReason.append("Images not high resolution")
            break
    
    #Check for page language (root and inner pages)
    all_texts = driver.find_elements(By.XPATH,"//*[text()]")

    for texts in all_texts:
        if texts.text == texts.get_attribute('data-translate'):
            CheckSite = "Fail"
            CheckReason.append("Inner pages not translated")
            break

    print(url)
    print(CheckReason)
    driver.close()
    return CheckSite,",".join(CheckReason)