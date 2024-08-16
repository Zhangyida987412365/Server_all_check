# -*- coding:utf-8 -*-
import cx_Oracle
import openpyxl
import logging

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

# 配置数据库连接参数

db2_user = "RM"
db2_password = "Doudou#$0331"
db2_dsn = "10.31.178.205:1521/orcl"


pygame.mixer.init()
vic = '新闻男声2'



def mid_orace():
    sql_queries_db2 = [
        r"sql",
        r"sql",
        r"sql",
        r"sql",
        
    ]

    #print(sql_queries_db2[0])


    try:
        # 连接到数据库2并处理查询结果
        connection2 = cx_Oracle.connect(user=db2_user, password=db2_password, dsn=db2_dsn)
        cursor2 = connection2.cursor()
        for i, sql_query in enumerate(sql_queries_db2, start=1):
            cursor2.execute(sql_query)
            results = cursor2.fetchall()
            if i == 1:
                print("当前过车中间表数据量:", results)
                tuple_result1 = results[0]
                int_tuple_result1 = int(float(tuple_result1[0]))
                if int_tuple_result1 >= 5000:
                    print(f"检测到新的异常记录，播放音乐！")
                    bf.play_voc(f'当前中间表数据量偏高')
                    pygame.mixer.music.load(f"H:\自动巡检集指\music\语音提示信息工作中\{vic}\当前中间表数据量偏高.MP3")  # 修改为正确的文件路径
                    pygame.mixer.music.play()
                    print(f'表大小目前:{int_tuple_result1}积压异常记录日志')
                    logger_error.error(f"表大小目前:{int_tuple_result1}积压异常")
                    
            if i==2:
                tuple_result2 = results[0]
                int_tuple_result2 = int(float(tuple_result2[0]))
                if int_tuple_result2 >= 500:
                    bf.play_voc(f'过车表大小偏高数据量约为{int_tuple_result2}')
                print("过车表大小:", int_tuple_result2,'MB')  #  >500
            if i==3:
                tuple_result3 = results[0]                
                int_tuple_result3 = int(float(tuple_result3[0]))
                if int_tuple_result3 >= 1000:
                    bf.play_voc(f'违法表数据量偏高数据量约为{int_tuple_result3}')
                print("违法表数据量:", int_tuple_result3)   # >1000
            if i==4:
                tuple_result4 = results[0]                
                int_tuple_result4 = int(float(tuple_result4[0]))
                #if int_tuple_result4 >= 500:
                    #bf.play_voc(f'违法表大小偏高数据量约为{int_tuple_result4}')
                print("违法表大小:", int_tuple_result4,'MB')# 500MB
                
        cursor2.close()
        connection2.close()
        

    except cx_Oracle.DatabaseError as e:
        print("数据库错误：", e)

# 测试代码
#mid_orace()
