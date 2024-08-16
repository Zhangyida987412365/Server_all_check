from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import logging
import datetime
from selenium.webdriver.chrome.options import Options


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





def xunjianHeZhong():

    # 设置Chrome的无头模式
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument("--headless")  # 确保无界面运行
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
    driver.get("https")
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
    login_button = driver.find_element(By.ID, "ext-gen21")  # 例如，替换为登录按钮的name属性
    login_button.click()
    # 等待登录操作完成（根据需要调整等待时间）
    time.sleep(1)

    actions = ActionChains(driver)
    actions.send_keys(Keys.RETURN).perform()

    
        
#    time.sleep(300)
    # 定位所有<a>使用了XPath表达式来找到文本为"RUNNING"的<a>标签
    agen_jiankong = driver.find_elements(By.ID, "extdd-69")
    print(driver.page_source)
    print(agen_jiankong.text)
    agen_jiankong.click()
    
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
                print(datetime.datetime.now(),f"没找到: {driver_name}")
                logger_error.error(f"URL {driver_name} 集指服务没找到")
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
        print('积压巡检结束===================================================')

        # 关闭浏览器
        driver.quit()
    else:
        print("没有找到文本为'RUNNING'的<a>标签")

    # 等待新页面加载完成（根据需要调整等待时间）
    # time.sleep(500)


        # 关闭浏览器
    driver.quit()
xunjianHeZhong()

