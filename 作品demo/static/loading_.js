document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('loading_btn').addEventListener('click', function () {
        // 显示加载动画和文本
        showLoadingAnimation();

        // 发送上传请求
        uploadFileAndProcessImage();
    });

    function showLoadingAnimation() {
        var loadingOverlay = document.querySelector('.lay-loader');
        loadingOverlay.style.display = 'block';

        var loadingText = document.createElement('div');
        loadingText.className = 'loading-text';
        loadingText.textContent = 'Loading';
        loadingText.style.display = 'block';
        loadingOverlay.appendChild(loadingText);
    }

    function uploadFileAndProcessImage() {
        const file = document.getElementById('file_Input').files[0];
        const formData = new FormData();
        formData.append('file', file);

        fetch('/upload_single', {
            method: 'POST',
            body: formData
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // 隐藏加载动画和文本
                hideLoadingAnimation();
                // 处理后的图片数据
                if (data && data.processed_image_url) {
                    showProcessedImage(data);
                    let type = ''
                    let coordinates_Xmin = '';
                    let coordinates_Xmax = '';
                    let coordinates_Ymin = '';
                    let coordinates_Ymax = '';
                    let score = '';
                    for(let i=0;i<data.boxes.length; i++) {

                        if (data.boxes && data.scores) {
                            if (data.class_ids.includes(0)) {
                                type += 'good ';
                            } else if (data.class_ids.includes(1)) {
                                type += 'broken ';
                            } else if (data.class_ids.includes(2)) {
                                type += 'circle ';
                            } else if (data.class_ids.includes(3)) {
                                type += 'loss ';
                            } else if (data.class_ids.includes(4)) {
                                type += 'uncovered ';
                            }
                            coordinates_Xmin += `X_min:${data.boxes[i][0]} `;
                            coordinates_Xmax += `X_max:${data.boxes[i][1]} `;
                            coordinates_Ymin += `Y_min:${data.boxes[i][2]} `;
                            coordinates_Ymax += `Y_max: ${data.boxes[i][3]} `;
                            score += `${(data.scores[i] * 100).toFixed(2)}% `; // 将得分转换成百分比格式并取两位小数

                        }else {
                            type='unidentifiable';
                        }
                        console.log(data.boxes.length);
                        const typeDiv = document.querySelector('.type');
                        typeDiv.innerHTML = type;
                        const coordinatesDiv=document.querySelector('.coordinates');
                        coordinatesDiv.innerHTML = coordinates_Xmin+"<br>"+coordinates_Xmax+"<br>"+coordinates_Ymin+"<br>"+coordinates_Ymax;
                        const scoreDiv = document.querySelector('.score');
                        scoreDiv.innerHTML = score;
                    }


                } else {
                    alert('上传出错，请重试');
                }
            })
            .catch(error => {
                console.error('上传出现错误', error);
                alert('上传出错，请重试');
            });
    }

    function hideLoadingAnimation() {
        var loadingOverlay = document.querySelector('.lay-loader');
        loadingOverlay.style.display = 'none';
        loadingOverlay.querySelector('.loading-text').remove();
    }

    function showProcessedImage(response) {
        document.getElementById('Pic').style.height='auto';
        const resultDiv = document.getElementById('result');
        document.getElementById('result').style.height = 'auto';
        resultDiv.innerHTML = '';

        const img = document.createElement('img');
        img.src = response.processed_image_url;
        resultDiv.appendChild(img);
    }
});