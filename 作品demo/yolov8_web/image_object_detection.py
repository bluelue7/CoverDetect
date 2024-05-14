import cv2
from imread_from_url import imread_from_url  #  环境的Lib/sitepackage内的
from PIL import Image
from yolov8 import YOLOv8

# Initialize yolov8 object detector
model_path = "models/best.onnx"   # ！！！需要更改模型路径
yolov8_detector = YOLOv8(model_path, conf_thres=0.2, iou_thres=0.3)   # ！！！要改自己的置信。。参数

# Read image
# img_url = "https://ts1.cn.mm.bing.net/th/id/R-C.09b6c9c005ee749e39ac38ab7d342c4e?rik=QIwnYpHp5%2bSxKA&riu=http%3a%2f%2fwww.smc-cover.com%2fuploads%2fallimg%2f150818%2f1-150QQ00GD15.JPG&ehk=JzS9xxhyI6WqWEPtpaBrNjwS%2fiQU7RaKkPJzI0GaVBI%3d&risl=&pid=ImgRaw&r=0"  # ！！！图像的路径（如果是网上的图片链接）
# img = imread_from_url(img_url)                                           #  !!!注意这里的img是什么形式的(BGR)

image_path="D:\\workplace\\Flask\\demo1\\uploads\\20221220154855.png"
img = cv2.imread(image_path)

# img=Image.open("D:\\pythonfrompycharm\\yolov8_web\\doc\\img\\img.png")
# Detect Objects

boxes, scores, class_ids = yolov8_detector(img)  # 自动调用call函数

# Draw detections
combined_img = yolov8_detector.draw_detections(img)  # 获取结果图像
cv2.namedWindow("Detected Objects", cv2.WINDOW_NORMAL)  # 创窗口
cv2.imshow("Detected Objects", combined_img)  # 展示窗口+做好标注的图像combined_img
# cv2.imwrite("doc/img/detected_objects2.jpg", combined_img)  # 保存画好的图像到文件夹
cv2.waitKey(0)
