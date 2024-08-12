import cv2
image = cv2.imread('path_to_image.jpg')

# 检查图像是否读取成功
if image is None:
    print("无法读取图像")
else:
    print("图像读取成功")
