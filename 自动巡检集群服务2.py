from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import logging
import datetime
import re

import pygame

import 播放语音信息模块包 as bf




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

vic = '新闻男声2'


def xunjianFuwu():
    

    drivers_to_check = [
            'TfcPassDriver',
            'RmLogDriver',
            'RecgCheckDriver',
            'VioSurveilDriver'
        ]


    jiya_error = 7

    # 设置Chrome的无头模式
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")  # 确保无界面运行
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
    driver.get("httpurl")
    # 等待页面加载
    #time.sleep(2)

    # print(driver.page_source)
    # exit()

    # 找到用户名和密码输入框（请根据实际情况替换元素的定位方法和值）
    username_box = driver.find_element(By.ID, "username")  # 例如，替换为用户名输入框的name属性
    password_box = driver.find_element(By.ID, "password")  # 例如，替换为密码输入框的name属性

    # 输入用户名和密码（替换为你的凭据）
    username_box.send_keys("1")
    password_box.send_keys("1")

    # 找到登录按钮并点击（请根据实际情况替换元素的定位方法和值）
    login_button = driver.find_element(By.ID, "loginbtn")  # 例如，替换为登录按钮的name属性
    login_button.click()
    # 等待登录操作完成（根据需要调整等待时间）
    # time.sleep(15)


    # 定位所有<a>标签，这里使用了XPath表达式来找到文本为"RUNNING"的<a>标签
    links = driver.find_elements(By.XPATH, "//a[text()='RUNNING']")

    # 假设我们想点击第一个匹配的<a>标签
    if links:
        links[0].click()
        # time.sleep(5)  # 等待页面加载，这里使用显式等待会更好

        # 需要查找的驱动文本列表


        # 检查并打印缺失的驱动
        for driver_name in drivers_to_check:
            if driver_name in driver.page_source:
                print(datetime.datetime.now(),f"找到了: {driver_name}")
            else:
                bf.play_voc(f"没找到: {driver_name}服务")
                print(datetime.datetime.now(),f"没找到: {driver_name}")
                logger_error.error(f"URL {driver_name} 集指服务没找到")

                # 播放音乐
                print("检测到新的异常记录，播放音乐！")
                pygame.mixer.music.load(f"H:\自动巡检集指\music\巡检的四个服务中有丢失的.MP3")  # 修改为正确的文件路径
                pygame.mixer.music.play()

                
                logger_error.error(f"URL {driver_name} 集指服务没找到")
                # bf.play_voc(f"URL {driver_name} 集指服务没找到")
                print('将尚未找到的服务记录日志.....error_urls.log')
            


            
          # 在这里添加更多的逻辑，如果需要
        print('巡检积压===================开始=============================...')
        # 找到点击ApplicationMase
        xpath_expression = "//tr[contains(.,'TfcPassDriver')]/descendant::a[last()]"
        a_element = driver.find_element(By.XPATH,xpath_expression)
        a_element.click()

        # 找到对应的Seaming
        xpath_Streaming = "//*[contains(text(),'Streaming')]"
        stre = driver.find_element(By.XPATH,xpath_Streaming)
        stre.click()
        
        # 打印积压部分
        xpath_thead = "//*[@id='stat-table']/thead/tr"
        thead_element = driver.find_element(By.XPATH,xpath_thead)
        thread_content = thead_element.text
        print(datetime.datetime.now(),'TfcPassDriver目前积压情况',thread_content)
        parts = thread_content.split(',')
        if len(parts) >= 2:
            match = re.match(r'\s*(\d+)',parts[1])
            if match:
                number = int(match.group(1))
                if number >= jiya_error:
                    print(f'TfcPassDriver积压acive大于{jiya_error}记录进入日志,挤压值为{number}')
                    bf.play_voc(f"TfcPassDriver目前积压情况acive大于{jiya_error}记录进入日志")
                    bf.play_voc(f"当前挤压值为{number}")
                    # 播放音乐
                    print("检测到新的异常记录，播放音乐！")
                    pygame.mixer.music.load(f"H:\自动巡检集指\music\语音提示信息工作中\{vic}\TfcPassDriver挤压大于5.MP3")  # 修改为正确的文件路径
                    pygame.mixer.music.play()        
                    
                    logger_error.error(f"TfcPassDriver积压acive大于{jiya_error}记录进入日志,挤压值为{number}")
                else:
                    print(f'TfcPassDriver积压正常acive小于{jiya_error}')
        
        # 回到服务首页
        driver.get("httpurl")


        # 找到点击ApplicationMase
        xpath_RecgCheckDriver = "//tr[contains(.,'RecgCheckDriver')]/descendant::a[last()]"
        a_RecgCheckDriver_element = driver.find_element(By.XPATH,xpath_RecgCheckDriver)
        a_RecgCheckDriver_element.click()
        # 找到对应的ApplicationMase
        xpath_ApplicationMase_Streaming = "//*[contains(text(),'Streaming')]"
        app_stre = driver.find_element(By.XPATH,xpath_ApplicationMase_Streaming)
        app_stre.click()
        # 打印积压部分
        xpath_thead_ApplicationMase = "//*[@id='stat-table']/thead/tr"
        thead1_element = driver.find_element(By.XPATH,xpath_thead_ApplicationMase)
        thread1_content = thead1_element.text
        print(datetime.datetime.now(),'RecgCheckDriver目前积压情况',thread1_content)
        parts1 = thread1_content.split(',')
        if len(parts1) >= 2:
            match = re.match(r'\s*(\d+)',parts1[1])
            if match:
                number = int(match.group(1))
                if number >= jiya_error:
                    print(f'RecgCheckDriver积压acive大于{jiya_error}记录进入日志,挤压值为{number}')
                    bf.play_voc(f'RecgCheckDriver积压acive大于{jiya_error}记录进入日志')
                    bf.play_voc(f"当前挤压值为{number}")
                    # 播放音乐
                    print("检测到新的异常记录，播放音乐！")
                    pygame.mixer.music.load(f"H:\自动巡检集指\music\语音提示信息工作中\{vic}\RecgCheckDriver积压大于5.MP3")  # 修改为正确的文件路径
                    pygame.mixer.music.play() 
                    
                    logger_error.error(f"RecgCheckDriver积压实际值acive大于{jiya_error}记录进入日志,挤压值为{number}")
                else:
                    print(f'RecgCheckDriver积压正常acive小于{jiya_error}')
        print('积压巡检结束===================================================')

        # 关闭浏览器
        driver.quit()
    else:
        print("没有找到文本为'RUNNING'的<a>标签")

    # 等待新页面加载完成（根据需要调整等待时间）
    # time.sleep(500)


        # 关闭浏览器
    driver.quit()

# 测试代码        
#xunjianFuwu()
