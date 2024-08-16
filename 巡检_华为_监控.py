from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import logging
import datetime
import re

import pygame
# 创建两个日志记录器
logger_normal = logging.getLogger('normal')
logger_normal.setLevel(logging.INFO)
normal_handler = logging.FileHandler('normal_urls.log')
normal_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
logger_normal.addHandler(normal_handler)

logger_error = logging.getLogger('error')
logger_error.setLevel(logging.ERROR)
error_handler = logging.FileHandler('error_urls.log')
error_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger_error.addHandler(error_handler)


pygame.mixer.init()

def xj_hauwei():
    # 设置Chrome的无头模式
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")  # 确保无界面运行
    chrome_options.add_argument("--disable-gpu")  # 禁用GPU加速，某些系统上需要
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--allow-insecure-localhost')

    chrome_options.add_argument("--log-level=3")
    chrome_options.add_experimental_option('excludeSwitches',['enable-logging'])  


    # 使用ChromeDriverManager自动处理WebDriver
    # 指定ChromeDriver的本地路径
    chrome_driver_path = r"H:\自动巡检集指\msdriver\chromedriver.exe"


    # 初始化WebDriver
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service,options=chrome_options)

    # 打开登录页面（请替换为你要登录的网站的URL）
    driver.get("url") # 这里不能开源
    time.sleep(2)
    username_box = driver.find_element(By.ID, "userName-inputEl")  # 例如，替换为用户名输入框的name属性
    password_box = driver.find_element(By.ID, "password-inputEl")  # 例如，替换为密码输入框的name属性

    username_box.send_keys("1")
    password_box.send_keys("1")
    login_button = driver.find_element(By.ID, "button-1036")  # 例如，替换为登录按钮的name属性
    login_button.click()

    time.sleep(2)
    #portal-task-40550766-homepage-homepageview-homeMenuHomePagemenu-monitor
    liseJK = driver.find_element(By.ID, "portal-task-40550766-homepage-homepageview-homeMenuHomePagemenu-monitor")  # 例如，替换为登录按钮的name属性
    liseJK.click()
    


    links = driver.find_elements(By.ID, "portal-task-40550766-monitor-monitorview-alarm-realtimealarm-innerCt")
    print(len(links))

    test = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID,'portal-task-40550766-monitor-monitorview-alarm'))
    )
    
    print(test.text)
    for element in links:
        print(element.text)
    time.sleep(200)
    
xj_hauwei()
