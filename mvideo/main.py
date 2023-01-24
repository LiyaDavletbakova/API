from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
import time

client = MongoClient()
db = client.mvideo
trend = db.trend_mvideo
s = Service('./chromedriver')

chromeOptions = Options()
chromeOptions.add_argument('--windows-size=1920,1080')

driver = webdriver.Chrome(service=s, options=chromeOptions)
driver.implicitly_wait(10)
driver.get('https://www.mvideo.ru/')

time.sleep(10)
# wait = WebDriverWait(driver, 10)
driver.execute_script("window.scrollTo(0, 1500);")
button_trend = driver.find_elements(By.CLASS_NAME, "tab-button")
button_trend[1].click()

goods = button_trend[0].find_elements(By.XPATH, "./ancestor::mvid-shelf-group")
names = goods[0].find_elements(By.XPATH, "//div[@class='title']")
links = goods[0].find_elements(By.XPATH, "//div[@class='title']/a[@href]")
prices = goods[0].find_elements(By.XPATH, "//div[@class='product-mini-card__price ng-star-inserted']//"
                                          "span[@class='price__main-value']")
trend_mvidio = []
for i in range(len(names)-1):
    name = names[i].text
    link = links[i].get_attribute("href")
    price = prices[i].text
    trend_mvidio.append({'name': name,
                         'link': link,
                         'price': price})

for n in trend_mvidio:
    trend.insert_one(n)
