import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pygame

# 初始化pygame音乐播放器
pygame.mixer.init()

class LogFileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # 当日志文件被修改时调用
        if "error_urls.log" in event.src_path:
            print("检测到新的异常记录，播放音乐！")
            pygame.mixer.music.load("H:\自动巡检集指\music\祖海 - 好运来_01.mp3")  # 修改为正确的文件路径
            pygame.mixer.music.play()
            time.sleep(5)  # 播放音乐五秒
            pygame.mixer.music.stop()  # 停止音乐播放

if __name__ == "__main__":
    path = "."  # 设置日志文件所在的目录
    event_handler = LogFileHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)  # 设置为True以递归监控所有子目录
    observer.start()
    print("开始监控异常日志...")

    try:
        # 主线程将持续运行，直到被中断
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    pygame.mixer.quit()
