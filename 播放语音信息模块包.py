import pyttsx3



def play_voc(str_con):
    engine = pyttsx3.init()
    engine.setProperty('volume', 1.0)  # 减慢语速
    # 设置语速（默认是200 wpm）
    engine.setProperty('rate', 150)  # 减慢语速
    engine.say(str_con)
    engine.runAndWait()

# play_voc('假设,请注意，巡检服务发现了TFC过车积压问题')
# print('执行完毕')
# exit()
