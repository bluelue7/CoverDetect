from flask import Flask, render_template, request, jsonify, url_for
from werkzeug.utils import secure_filename
import os, time, calendar

import cv2
from imread_from_url import imread_from_url  # 环境的Lib/sitepackage内的
from PIL import Image
from yolov8_web.yolov8 import YOLOv8

app = Flask(__name__)  # 实例化一个Flask类对象

UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# 多张
@app.route('/multi', methods=['GET', 'POST'])
def multi():  # put application's code here
    if request.method == 'POST':
        files = request.files.getlist('images[]')
        responses = []
        model_path = "./yolov8_web/models/best.onnx"  # ！！！需要更改模型路径
        yolov8_detector = YOLOv8(model_path, conf_thres=0.2, iou_thres=0.3)  # ！！！要改自己的置信。。参数
        i = 1
        for file in files:
            name = os.path.splitext(file.filename)[0]
            suffix = os.path.splitext(file.filename)[-1]  # 获取文件后缀（扩展名）
            print(i)
            print(suffix)
            basePath = os.path.dirname(__file__)  # 当前文件所在路径print(basePath)
            nowTime = calendar.timegm(time.gmtime())  # 获取当前时间戳改文件名print(nowTime)
            upload_path = os.path.join(basePath, 'uploadimg',
                                       str(nowTime))  # 改到upload目录下# 注意：没有的文件夹一定要先创建，不然会提示没有该路径print(upload_path)
            print(i)
            print(upload_path)
            upload_path = os.path.abspath(upload_path)  # 将路径转换为绝对路径print("绝对路径：",upload_path)

            print(i)
            print(upload_path)

            file.save(upload_path + suffix)  # 保存文件
            process_path = os.path.join(basePath, 'static/images/processedimg',
                                        str(nowTime))
            process_path = os.path.abspath(process_path)

            print(i)
            print(process_path)
            # http 路径
            # url = 'http://xxxx.cn/upload/' + str(nowTime) + str(nowTime) + suffix
            #

            img = cv2.imread("./uploadimg/" + str(nowTime) + suffix)  # 读取照片

            boxes, scores, class_ids = yolov8_detector(img)  # 自动调用call函数

            # Draw detections
            combined_img = yolov8_detector.draw_detections(img)  # 获取结果图像

            cv2.imwrite(process_path + suffix, combined_img)  # 保存画好的图像到文件夹
            print("here" + process_path)
            image_url = url_for('static',
                                filename='images/processedimg/' + str(nowTime) + suffix)  # 如果是目录的方式，图片似乎必须存static下
            # 否则要搞一个专门生成图片路径的函数
            response_data = {
                'boxes': boxes.tolist(),  # 将 NumPy 数组转换为列表
                'scores': scores.tolist(),  # 将 NumPy 数组转换为列表
                'class_ids': class_ids.tolist(),  # 将 NumPy 数组转换为列表
                'image_url': image_url  # 直接包含 image_url
            }
            responses.append(response_data)
        return {'files': responses}

    else:
        return render_template('multipic.html')


# 单张
@app.route('/index', methods=['GET', 'POST'])
def index():  # put application's code here
    if request.method == 'POST':
        file = request.files['image']
        if file:
            suffix = os.path.splitext(file.filename)[-1]  # 获取文件后缀（扩展名）
            basePath = os.path.dirname(__file__)  # 当前文件所在路径print(basePath)
            nowTime = calendar.timegm(time.gmtime())  # 获取当前时间戳改文件名print(nowTime)
            upload_path = os.path.join(basePath, 'uploadimg',
                                       str(nowTime))  # 改到upload目录下# 注意：没有的文件夹一定要先创建，不然会提示没有该路径print(upload_path)

            upload_path = os.path.abspath(upload_path)  # 将路径转换为绝对路径print("绝对路径：",upload_path)

            file.save(upload_path + suffix)  # 保存文件

            process_path = os.path.join(basePath, 'static/images/processedimg',
                                        str(nowTime))

            process_path = os.path.abspath(process_path)

            # http 路径
            # url = 'http://xxxx.cn/upload/' + str(nowTime) + str(nowTime) + suffix
            #

            model_path = "./yolov8_web/models/best.onnx"  # ！！！需要更改模型路径

            yolov8_detector = YOLOv8(model_path, conf_thres=0.2, iou_thres=0.3)  # ！！！要改自己的置信。。参数

            print(file.filename)
            img = cv2.imread("./uploadimg/" + str(nowTime) + suffix)  # 读取照片

            boxes, scores, class_ids = yolov8_detector(img)  # 自动调用call函数

            # Draw detections
            combined_img = yolov8_detector.draw_detections(img)  # 获取结果图像

            cv2.imwrite(process_path + suffix, combined_img)  # 保存画好的图像到文件夹

            image_url = url_for('static',
                                filename='images/processedimg/' + str(nowTime) + suffix)  # 如果是目录的方式，图片似乎必须存static下
            # 否则要搞一个专门生成图片路径的函数
            response_data = {
                'boxes': boxes.tolist(),  # 将 NumPy 数组转换为列表
                'scores': scores.tolist(),  # 将 NumPy 数组转换为列表
                'class_ids': class_ids.tolist(),  # 将 NumPy 数组转换为列表
                'image_url': image_url  # 直接包含 image_url
            }
            print(boxes)
            print(class_ids)
            print(scores)
        return jsonify(response_data)



    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run()
