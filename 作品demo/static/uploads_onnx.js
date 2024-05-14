document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('upload-form');
    const fileInput = document.getElementById('file-input');
    const uploadButton = document.getElementById('upload-button');
    const completeButton = document.getElementById('complete-button');
    const cancelButton = document.getElementById('cancel-button');
    const tipDiv = document.getElementById('tip');

    // 从本地存储中加载并设置按钮状态、文件输入框内容和 tipDiv 内容
    const uploadButtonState = localStorage.getItem('uploadButtonState');
    const fileInputState = localStorage.getItem('fileInputState');
    const tipDivState = localStorage.getItem('tipDivState');

    if (uploadButtonState) {
      uploadButton.disabled = uploadButtonState === 'true';
    }

    if (fileInputState && fileInputState !== "null" && fileInputState !== "") {
      if (fileInput.files.length > 0) {
        tipDiv.innerHTML = "选择的文件：" + fileInput.files[0].name; // 在 tipDiv 中显示选择的文件名
      }
    }

    if (tipDivState) {
      tipDiv.innerHTML = tipDivState; // 恢复 tipDiv 的内容
    }

    fileInput.addEventListener('change', function() {
      if (fileInput.files.length > 0) {
        uploadButton.disabled = false;
        tipDiv.innerHTML = "选择的文件：" + fileInput.files[0].name; // 更新 tipDiv 中显示选择的文件名
      } else {
        uploadButton.disabled = true;
      }

      // 保存文件选择状态和 tipDiv 内容到本地存储
      localStorage.setItem('fileInputState', fileInput.value);
      localStorage.setItem('tipDivState', tipDiv.innerHTML);
    });

    uploadForm.addEventListener('submit', function(event) {
        event.preventDefault(); // 阻止表单默认提交行为


        const file = fileInput.files[0];
        if (!file) {
            alert('请选择一个文件！');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        fetch('/upload_onnx', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                alert('文件上传成功!');

                completeButton.disabled = false;
                cancelButton.disabled = false;

                localStorage.setItem('uploadButtonState', 'true');

            } else {
                alert('文件上传失败: ' + response.statusText);
            }
        })
        .catch(error => {
            alert('文件上传出错: ' + error.message);
        });
    });

    completeButton.addEventListener('click', function() {
        window.location.href = './index.html';
    });

    cancelButton.addEventListener('click', function() {
        // 重置按钮状态
        uploadButton.disabled = false;
        completeButton.disabled = true;
        cancelButton.disabled = true;
        // 在本地存储中移除按钮状态
        fileInput.value = '';
        localStorage.removeItem('uploadButtonState');
        localStorage.removeItem('fileInputState');
        localStorage.setItem('tipDivState', tipDiv.innerHTML='');
        fetch('/cancel_upload', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            cancelled: true
        })
        })
        .then(response => {
            if (response.ok) {
                console.log('取消信号发送成功');
            } else {
                // 发送失败处理逻辑
                console.error('取消信号发送失败');
            }
        })
        .catch(error => {
            console.error('取消信号发送失败:', error);
        });

    });
});

