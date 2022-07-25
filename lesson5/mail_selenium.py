from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

client = MongoClient('localhost', 27017)
db = client['Selenium']
collections = db.selenium_collection

browser = webdriver.Chrome("/Users/chromedriver")

browser.get("https://account.mail.ru/login")

browser.implicitly_wait(5)

login_elem = browser.find_element_by_name("username")
login_elem.send_keys("study.ai_172@mail.ru")
login_elem.send_keys(Keys.ENTER)

password_elem = browser.find_element_by_name("password")
password_elem.send_keys("NextPassword172!")

password_elem.send_keys(Keys.ENTER)

browser.implicitly_wait(5)

browser.find_element_by_xpath("//a[@class='llc js-tooltip-direction_letter-bottom js-letter-list-item llc_normal']").click()

while True:
    browser.implicitly_wait(2)
    name = browser.find_element_by_xpath("//span[@class='letter-contact']").text
    message = browser.find_element_by_xpath("//h2[@class='thread__subject']").text
    date = browser.find_element_by_xpath("//div[@class='letter__date']").text
    print(f"Отправитель: {name}, Сообщение: {message}, Дата: {date}")
    browser.find_element_by_xpath("//div[@class='portal-menu-element portal-menu-element_next portal-menu-element_expanded "
                                  "portal-menu-element_not-touch']").click()
# browser.close()
