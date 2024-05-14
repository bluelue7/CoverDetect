document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('fileInput').addEventListener('change', function () {
        var imageContainer = document.getElementById('imagePreview');
        while (imageContainer.firstChild) {
            imageContainer.removeChild(imageContainer.firstChild);
        }

        var files = Array.from(this.files);
        files.forEach(file => {
            var reader = new FileReader();
            reader.onload = function (e) {
                var img = document.createElement('img');
                img.src = e.target.result;
                imageContainer.appendChild(img);
            }
            reader.readAsDataURL(file);
        });

        document.getElementById('loading_btn').style.display = 'block';
    });
});
//     document.getElementById('loading_btn').addEventListener('click', function () {
//         var files = document.getElementById('fileInput').files;
//         var formData = new FormData();
//
//         Array.from(files).forEach(file => {
//             formData.append('files[]', file);
//         });
//
//         fetch('/upload_multiple', {
//             method: 'POST',
//             body: formData
//         })
//             .then(response => {
//                 if (response.ok) {
//                     alert('文件上传成功！');
//
//                     document.getElementById('imagePreview').innerHTML = '';
//
//                 } else {
//                     alert('上传出错，请重试11111');
//                     //1111111111111
//                 }
//             })
//
//             .catch(error => {
//                 console.error('上传出现错误', error);
//                 alert('上传出错，请重试2222222');
//             });
//     });
// });

