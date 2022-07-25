import json

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

chrome_options = Options()
chrome_options.add_argument('start-maximized')

browser = webdriver.Chrome("/Users/chromedriver", options=chrome_options)
browser.get("https://www.mvideo.ru/")

browser.refresh()

new_goods = browser.find_element_by_xpath("//div[contains(text(), 'Новинки')]")
action = ActionChains(browser)
action.move_to_element(new_goods)
action.perform()

items = browser.find_elements_by_xpath("//ul[contains(@data-init-param, '\"title\":\"Новинки\"')]/li")
items_count = len(items)

while True:
    button = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//ul[contains(@data-init-param, '\"title\":\"Новинки\"')]/../../a[@class='next-btn c-btn c-btn_scroll-horizontal c-btn_icon i-icon-fl-arrow-right']"))
    )
    button.click()
    sleep(1)
    items = browser.find_elements_by_xpath("//ul[contains(@data-init-param, '\"title\":\"Новинки\"')]/li")
    items_count_click = len(items)

    if items_count == items_count_click:
        break
    items_count = len(items)


print(len(items))

for item in items:
    item.click()
    name = browser.find_element_by_xpath("//h1[@class='fl-h1']").text
    price = browser.find_element_by_xpath("//div[@class='fl-pdp-price__current']").text
    price_old = browser.find_element_by_xpath("//div[@class='fl-pdp-price__old']").text
    print(f"Название товара: {name}, Цена: {price}, Старая Цена: {price_old}")
    browser.back()



