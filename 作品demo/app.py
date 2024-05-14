import numpy as np
from flask import Flask, request, jsonify, render_template, send_file, flash
import zipfile
import threading
import subprocess
import torch
import argparse
import os
# from detect import run, main
from flask import Flask, render_template, request
import os
from flask import jsonify
from sympy import false
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, jsonify, url_for
from werkzeug.utils import secure_filename
import os, time, calendar
import cv2
from PIL import Image
import io
import cv2
from imread_from_url import imread_from_url  # 环境的Lib/sitepackage内的
from PIL import Image
from yolov8_web.yolov8 import YOLOv8
from flask import send_from_directory
from flask import render_template

app = Flask(__name__)
from flask import request
from werkzeug.utils import secure_filename
import os
from flask_cors import CORS

CORS(app)

# 配置文件上传目录
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
PROCESSED_FOLDER = './static/processed_images'
app.config['PROCESSED_FOLDER'] = './static/processed_images'

UPLOAD_FOLDER_PT = './model'
app.config['UPLOAD_FOLDER_PT'] = UPLOAD_FOLDER_PT
os.makedirs(UPLOAD_FOLDER_PT, exist_ok=True)  # 确保目录存在
ALLOWED_EXTENSIONS_onnx = {'onnx'}  # 允许的文件扩展名集合

# 初始化模型示例为全局变量
model_path = "./yolov8_web/models/best.onnx"  # 模型路径
update_path = ""
yolov8_detector = YOLOv8(model_path, conf_thres=0.2, iou_thres=0.3)

thread_status = {'running': False, 'model_ready': False}
thread_lock = threading.Lock()


# @app.before_first_request
# def initialize_model():
#     global yolov8_detector
#     yolov8_detector = YOLOv8(model_path, conf_thres=0.2, iou_thres=0.3)  # 在第一个请求前进行初始化

@app.route('/pt.html')
def topt():
    return render_template('pt.html')


@app.route('/pt', methods=['GET', 'POST'])
def pt():
    if request.method == 'POST':
        if not any(key in request.files for key in ['image_train[]', 'image_val[]', 'label_train', 'label_val']):
            return jsonify({'success': False, 'error': '上传的文件不符合要求！'}), 400
        else:
            path_datasets = './ultralytics_/datasets'
            files_datasets = os.listdir(path_datasets)
            num_datasets = len(files_datasets)

            new_folder_path = path_datasets + '/data' + str(num_datasets)
            os.makedirs(new_folder_path)  # 在datasets目录下新建本次训练的资源夹 data+编号

            images_path = new_folder_path + '/images'
            labels_path = new_folder_path + '/labels'

            os.makedirs(images_path)
            os.makedirs(labels_path)
            # os.makedirs(images_path + '/test')
            os.makedirs(images_path + '/train')
            os.makedirs(images_path + '/val')
            # os.makedirs(labels_path + '/test')
            os.makedirs(labels_path + '/train')
            os.makedirs(labels_path + '/val')

            image_train_path = images_path + '/train'
            image_val_path = images_path + '/val'
            label_train_path = labels_path + '/train'
            label_val_path = labels_path + '/val'

            image_train = request.files.getlist('image_train[]')
            for file in image_train:
                filename = os.path.basename(file.filename)  # 更可靠地获取文件名

                file.save(os.path.join(image_train_path, filename))

            image_val = request.files.getlist('image_val[]')
            for file in image_val:
                filename = os.path.basename(file.filename)  # 更可靠地获取文件名
                file.save(os.path.join(image_val_path, filename))

            label_train = request.files.getlist('label_train[]')
            for file in label_train:
                filename = os.path.basename(file.filename)  # 更可靠地获取文件名
                file.save(os.path.join(label_train_path, filename))

            label_val = request.files.getlist('label_val[]')
            for file in label_val:
                filename = os.path.basename(file.filename)  # 更可靠地获取文件名
                file.save(os.path.join(label_val_path, filename))

            path_runs = './runs/detect'  # 结果所在文件夹
            files_runs = os.listdir(path_runs)
            num_runs = len(files_runs)  # 已经存在的文件数量
            thread = threading.Thread(target=process_and_save_results, args=(num_datasets,))  # 数据集的编号
            thread.start()
            return jsonify({'success': True, 'taskID': num_runs + 1})  # 模型训练结果文件夹的编号
    else:
        return render_template('pt.html')
    # model_path='runs/detect/train3/weights/best.pt'
    # return send_file(model_path,as_attachment=True,download_name='best.pt')


def process_and_save_results(num_datasets):
    yaml_name = 'data' + str(num_datasets)  # 配置yaml的编号和数据集一致
    desired_caps = {
        'path': yaml_name,  # 这里是不带.yaml后缀的！
        'train': 'images/train',
        'val': 'images/val',
        'nc': 5,
        # 真正的Python列表，但我们将其转换为字符串表示形式
        'names_list': ['good', 'broke', 'lose', 'uncovered', 'circle']
    }
    yaml_path = './ultralytics_/' + yaml_name + '.yaml'

    # 将Python列表转换为字符串表示形式，并添加方括号
    names_as_string = str(desired_caps['names_list'])

    # 构建包含注释和所需格式的YAML内容
    yaml_content = f"""  
    # dataset path  
    path: {desired_caps['path']}  
    train: {desired_caps['train']}  
    val: {desired_caps['val']}  
    # test: datasets/{desired_caps['path']}/images/test  

    # number of classes  
    nc: {desired_caps['nc']}  

    # class names (as a Python list string representation)  
    names: {names_as_string}  
    """
    # print(yaml_path)
    with open(yaml_path, 'w', encoding='utf-8') as f:
        f.write(yaml_content)
    data = 'ultralytics_/' + yaml_name + '.yaml'
    epochs = 1
    batch = 4
    model = "yolov8n.pt"
    workers = 1
    command = f"yolo detect train data={data} epochs={epochs} model={model} batch={batch} workers={workers}"
    global process_pt
    process_pt = subprocess.Popen(command, shell=True)


@app.route('/check_task_status', methods=['GET'])
def check_task_status():
    global process_pt
    status_code = process_pt.poll()
    print("来查看状态了！")
    print(status_code)
    if status_code is None:
        return jsonify({'success': True, 'status': 'running'})
    elif status_code == 0:
        return jsonify({'success': True, 'status': 'completed'})
    else:
        return jsonify({'success': False, 'status': 'failed', 'return_code': status_code})


@app.route('/download_folder/<taskId>', methods=['GET'])
def download_folder(taskId):
    # 假设这是你的文件夹路径
    print("来取下载文件了！")

    # 创建一个临时zip文件
    print(taskId)
    model_path = './runs/detect/train' + taskId  # 需要传递的文件夹

    zip_filename = 'results' + str(taskId) + '.zip'

    tmp_path = os.path.join('./temp_zip', zip_filename)
    print(tmp_path)
    # 将文件夹打包成zip文件
    with zipfile.ZipFile(tmp_path, 'w') as zipf:
        for root, dirs, files in os.walk(model_path):
            for file in files:
                print("!!")
                file_path = os.path.join(root, file)
                # 写入zip文件，保持相对路径不变
                zipf.write(file_path, os.path.relpath(file_path, model_path))
                # 发送zip文件
    return send_file(tmp_path, as_attachment=True, download_name=zip_filename)  # 注意和with平齐，前端zip有问题是这个原因


# 允许的文件扩展名
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_onnx


# 用户上传自己的pt文件
@app.route('/upload_onnx', methods=['GET', 'POST'])
def upload_file():
    global model_path
    global yolov8_detector
    global update_path
    if request.method == 'POST':
        # 检查是否有文件在请求中
        if 'file' not in request.files:
            return jsonify({'error': '没有文件部分'}), 400
        print(1)

        file = request.files['file']

        # 检查文件扩展名是否允许
        if file.filename == '' or not allowed_file(file.filename):
            return jsonify({'error': '文件类型不正确或未选择文件'}), 400

        # 保存文件
        file_path = os.path.join(app.config['UPLOAD_FOLDER_PT'], file.filename)
        file.save(file_path)
        update_path = file_path
        print(update_path)
        # 加载模型和进行预测（这部分代码根据实际情况调整）
        try:
            # 这里使用上传的模型文件初始化检测器
            yolov8_detector = YOLOv8(file_path, conf_thres=0.2, iou_thres=0.3)
            return jsonify({'success': True, 'message': '模型加载成功'})

        except Exception as e:
            # 记录错误并返回错误信息
            app.logger.error(f"Failed to load model: {e}")


@app.route('/cancel_upload', methods=['POST'])
def cancel_upload():
    global update_path
    data = request.get_json()
    if data and data.get('cancelled'):
        print('收到取消信号，执行取消操作')
        update_path = ""
        return jsonify({'success': True, 'message': '取消信号已收到'})
    else:
        return jsonify({'error': '未收到有效的取消信号'})


# 多张图片的处理
@app.route('/upload_multiple', methods=['GET', 'POST'])
def upload_files():
    global yolov8_detector
    global update_path
    if request.method == 'POST':
        if 'files[]' not in request.files:
            return 'No file part'
        else:
            if update_path:
                yolov8_detector = YOLOv8(update_path, conf_thres=0.2, iou_thres=0.3)
                print(update_path)
            else:
                yolov8_detector = YOLOv8(model_path, conf_thres=0.2, iou_thres=0.3)
                print(model_path)
            files = request.files.getlist('files[]')
            responses = []
            for file in files:
                # jh：这里可以在前端file类型的input标签上加accept="image/*"
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)  # 构造文件保存路径
                file.save(file_path)  # 保存图像文件到指定目录
                # 图像处理过程
                img = cv2.imread(file_path)  # 读取照片
                boxes, scores, class_ids = yolov8_detector(img)  # 获取检测结果

                # 绘制检测结果
                combined_img = yolov8_detector.draw_detections(img)
                processed_filename = f"{os.path.splitext(filename)[0]}_processed{os.path.splitext(filename)[-1]}"
                processed_file_path = os.path.join(app.config['PROCESSED_FOLDER'], processed_filename)
                cv2.imwrite(processed_file_path, combined_img)  # 保存处理后的图像到指定目录

                # 构造图像 URL
                image_url = url_for('static', filename=f'processed_images/{processed_filename}')
                # 构造响应数据
                if isinstance(boxes, np.ndarray):
                    response_data = {
                        'file_name': filename,
                        'processed_image_url': image_url,
                        'boxes': boxes.tolist(),
                        'scores': scores.tolist(),
                        'class_ids': class_ids.tolist(),
                    }
                else:
                    response_data = {
                        'processed_image_url': image_url,
                    }
                responses.append(response_data)  # 将当前图像的检测结果添加到 responses 中
        return {'responses': responses}  # 返回所有图像的处理结果作为 JSON 数据
    else:
        return render_template('detections.html')


# 单张图片的处理
@app.route('/upload_single', methods=['POST'])
def upload_single_file():
    global yolov8_detector
    global update_path
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file:
            if update_path:
                yolov8_detector = YOLOv8(update_path, conf_thres=0.2, iou_thres=0.3)
                print("使用用户上传的文件：" + update_path)
            else:
                yolov8_detector = YOLOv8(model_path, conf_thres=0.2, iou_thres=0.3)
                print("使用默认模型文件" + model_path)
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)  # 构造文件保存路径
            file.save(file_path)  # 保存图像文件到指定目录

            # 图像处理过程
            img = cv2.imread(file_path)  # 读取照片
            boxes, scores, class_ids = yolov8_detector(img)  # 获取检测结果

            # 绘制检测结果
            combined_img = yolov8_detector.draw_detections(img)
            processed_filename = f"{os.path.splitext(filename)[0]}_processed{os.path.splitext(filename)[-1]}"
            processed_file_path = os.path.join(app.config['PROCESSED_FOLDER'], processed_filename)
            cv2.imwrite(processed_file_path, combined_img)  # 保存处理后的图像到指定目录

            # 构造图像 URL
            image_url = url_for('static', filename=f'/processed_images/{processed_filename}')
            if isinstance(boxes, np.ndarray):
                # 构造响应数据
                response_data = {
                    'file_name': filename,
                    'processed_image_url': image_url,
                    'boxes': boxes.tolist(),
                    'scores': scores.tolist(),
                    'class_ids': class_ids.tolist(),
                }
            else:
                response_data = {
                    'processed_image_url': image_url,
                }
            return jsonify(response_data)  # 返回图像的处理结果作为 JSON 数据
    else:
        return render_template('index.html')


@app.route('/user.html')
def user():
    return render_template('user.html')


@app.route('/choose.html')
def choose():
    return render_template('choose.html')


@app.route('/set_up.html')
def set_up():
    return render_template('set_up.html')


@app.route('/detections.html')
def detections():
    return render_template('detections.html')


@app.route('/analysis.html')
def analysis():
    return render_template('analysis.html')


@app.route('/intro.html')
def intro():
    return render_template('intro.html')


@app.route('/', methods=['GET'])
def index():
    return render_template('choose.html')


@app.route('/index.html')
def return_index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
