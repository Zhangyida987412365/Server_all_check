import requests
import time
import logging
import 自动巡检集群服务2 as xj
import 测试打印数据库 as ceshi
import 播放语音信息模块包 as bf

import pygame
import datetime

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

# 要检查的URL列表
urls = ["url",
        "url",
        "url",
        "url",
        "url",
        "url",

        
        "url",
        "url",
        "url",

        "url",
        "url",
        "url",
        "url",
        "url",
        "url",
        "url",
        "url",
        "url",

        ]

# 检查URL的函数
def check_urls(urls):
    # import 自动巡检集群服务.py
    for url in urls:
        try:
            # 在这里设置超时时间为5秒
            response = requests.get(url, timeout=8)
            if response.status_code == 200:
                print(datetime.datetime.now(),f"URL {url} 可以正常访问！")
                logger_normal.info(f"URL {url} 可以正常访问")
            else:
                print(datetime.datetime.now(),f"URL {url} 访问异常！状态码: {response.status_code}")

                voc_pop = f"URL {url} 访问异常"
                bf.play_voc(voc_pop)
                
                print("检测到新的异常记录，播放音乐！")
                pygame.mixer.music.load(f"H:\自动巡检集指\music\语音提示信息工作中\{vic}\集指链接访问超时.MP3")  # 修改为正确的文件路径
                pygame.mixer.music.play()

                
                logger_error.error(f"URL {url} 访问异常！状态码: {response.status_code}")
        except requests.RequestException as e:
            print(f"URL {url} 访问异常！错误: {e}")

            
            voc_pop = f"URL {url} 访问异常"
            bf.play_voc(voc_pop)
                
            
            print("检测到新的异常记录，播放音乐！")
            pygame.mixer.music.load(f"H:\自动巡检集指\music\语音提示信息工作中\{vic}\集指链接访问超时.MP3")  # 修改为正确的文件路径
            pygame.mixer.music.play()
            
            logger_error.error(f"URL {url} 访问异常！错误: {e}")
    try:
        xj.xunjianFuwu()
    except Exception as e:
        print(e)
        bf.play_voc('巡检服务时抛出了异常，可能需要重启程序')
        logger_error.error(f"错误: {e}")

# 无限循环，每分钟运行一次
while True:
    try:
        check_urls(urls)
        ceshi.mid_orace()
    except Exception as e: 
        print(e)
        bf.play_voc('巡检服务时抛出了异常，可能需要重启程序')
        logger_error.error(f"错误: {e}")
    
    print("等待下次检查...")
    time.sleep(3*60)  # 等待360秒
