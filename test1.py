from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from selenium import webdriver




# 指定ChromeDriver的本地路径
chrome_driver_path = r"H:\自动巡检集指\msdriver\chromedriver.exe"


# 初始化WebDriver
service = Service(chrome_driver_path)

driver = webdriver.Chrome(service=service)

source = driver.page_source

print(source)  # 打印出页面的HTML源代码
