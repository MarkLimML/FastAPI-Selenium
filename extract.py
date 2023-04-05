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

def doSiteCheck(driver: webdriver.Chrome, url):

    driver.get(url)

    CheckSite = ""
    CheckReason = []
    #Check for site if link is correct
    titlechk = "क्लास सेंट्रल • सर्वकालिक पाठ्यक्रम, चाहे वे कहीं भी हों।"
    titlechk2 = "कक्षा केंद्रीय • सर्वोत्तम पाठ्यक्रम खोजें, जहां भी वे मौजूद हैं।"

    if driver.title != titlechk or driver.title != titlechk2:
        CheckSite = "Fail"
        CheckReason.append("Wrong Page")

    #Check for page language (root and inner pages)
    all_texts = driver.find_elements_by_xpath("//*[text()]")

    for texts in all_texts:
        if texts.text == texts.get_attribute('data-translate'):
            CheckSite = "Fail"
            CheckReason.append("Inner pages not translated")
            break

    #Check for top left dropdown functionality
    nav_element = driver.get_element_by_class('main-nav-dropdown js-main-nav-dropdown')
    nav_element2 = driver.get_element_by_class('hidden xlarge-up-flex')
    nav_element3 = driver.get_element_by_class('bg-white z-top absolute width-1-3 border-all border-gray-light shadow-light padding-medium animate-fade-hidden')
    
    action = ActionChains(driver)
    action.move_to_element(nav_element).perform

    wait = WebDriverWait(driver, 5)
    wait.until(expected_conditions.attribute_to_be(nav_element, 'class', 'main-nav-dropdown js-main-nav-dropdown is-open'))

    if 'main-nav-dropdown js-main-nav-dropdown is-open' != nav_element.get_attribute('class'):
        CheckSite = "Fail"
        CheckReason.append("Javascript dropdown not working properly")

    action.move_to_element(nav_element2).perform

    wait.until(expected_conditions.attribute_to_be(nav_element3, 'class', 'bg-white z-top absolute width-1-3 border-all border-gray-light shadow-light padding-medium animate-fade-entered'))

    if 'bg-white z-top absolute width-1-3 border-all border-gray-light shadow-light padding-medium animate-fade-entered' !=  nav_element3.get_attribute('class'):
        CheckSite = "Fail"
        CheckReason.append("Javascript dropdown not working properly")

    #Check for site image are high resolution
    images = driver.find_element_by_tag_name('img')

    for img in images:
        src = img.get_attribute('src')
        if "blur" in src:
            CheckSite = "Fail"
            CheckReason.append("Images not high resolution")
            break

    return CheckSite,",".join(CheckReason)