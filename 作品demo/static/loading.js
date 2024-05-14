const countMap = {
   good: 0,
   broken: 0,
   circle: 0,
   loss: 0,
   uncovered: 0,
   unidentifiable:0
};

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('loading_btn').addEventListener('click', function () {
        // 显示加载动画和文本
        showLoadingAnimation();

        // 发送上传请求
        uploadFilesAndProcessImages();
    });
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

function uploadFilesAndProcessImages() {
    const files = document.getElementById('fileInput').files;
    const formData = new FormData();

    for (let i = 0; i < files.length; i++) {
        formData.append('files[]', files[i]);
    }

    fetch('/upload_multiple', {
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
        if (data && data.responses) {
            showProcessedImages(data.responses);
            data.responses.forEach(response => {
                if (response.class_ids) {
                    console.log(response.class_ids)
                    if (response.class_ids.includes(0)) {
                        countMap.good++;
                    } else if (response.class_ids.includes(1)) {
                        countMap.broken++;
                    } else if (response.class_ids.includes(2)) {
                        countMap.circle++;
                    } else if (response.class_ids.includes(3)) {
                        countMap.loss++;
                    } else if (response.class_ids.includes(4)) {
                        countMap.uncovered++;
                    }
                } else {
                    countMap.unidentifiable++;
                }
            });
            const settingsButton = document.getElementById('to_anal');
            settingsButton.addEventListener('click', () => {
                // 将 countMap 转换为 JSON 字符串
                localStorage.setItem("countMap", JSON.stringify(countMap));
                window.location.href = 'analysis.html?timestamp=' + Date.now();
            });
        } else {
            alert('上传出错，请重试333333333333333');
        }
    })
        .catch(error => {
            console.error('上传出现错误', error);
            alert('上传出错，请重试44444444444444444444');
            console.log(error);
        });
        }

function hideLoadingAnimation() {
    var loadingOverlay = document.querySelector('.lay-loader');
    loadingOverlay.style.display = 'none';
    loadingOverlay.querySelector('.loading-text').remove();
}

function showProcessedImages(responses) {
    document.getElementById('Pic2').style.height='auto';
    const resultDiv = document.getElementById('result');
    document.getElementById('result').style.height = 'auto';

    responses.forEach(response => {
        const img = document.createElement('img');
        img.src = response.processed_image_url;
        resultDiv.appendChild(img);
    });
}