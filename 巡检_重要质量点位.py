from selenium import webdriver
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

# 设置Chrome的无头模式
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")  # 确保无界面运行
chrome_options.add_argument("--disable-gpu")  # 禁用GPU加速，某些系统上需要
# 配置chomein项 一连接到远程调试端口
chrome_options.debugger_address = "127.0.0.1:9222"

# 指定 chromedriver 的路径
chrome_driver_path = r"H:\自动巡检集指\msdriver\chromedriver.exe"
service = Service(chrome_driver_path)

driver = webdriver.Chrome(service=service, options=chrome_options)

print('开始监测1')
print(driver.title)
print('监测结束')

print("重要点位运行质量查询" in driver.title)
#循环检查页面，知道找到目标标题为止
while True:
    if "重要点位运行质量查询" in driver.title:
        print("找到页面标题为<重要点位查询>！")
        print("当前页面的URL：", driver.page_source)

        a_tags = driver.find_elements(By.XPATH,"//td[@class='data'][last()]/a[text()<'80']")
        if a_tags:
            for a in a_tags:
                a.click()                
                print("点击了一个值为0的a标签")
                time.sleep(1)

                
                #获取新窗口的句柄
                new_windows_handle = driver.window_handles[-1]
                driver.switch_to.window(new_windows_handle)
                #等待新窗口的加载完全
                WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.TAG_NAME,"html")))
                #获取新窗口的源码
                time.sleep(3)
                new_window_source = driver.page_source
                print(new_window_source)
                
                #关闭当前窗口并且切换回原始窗口
                driver.close()
                driver.switch_to.window(driver.window_handles[-2])
        break
    else:
        driver.refresh()
        break
