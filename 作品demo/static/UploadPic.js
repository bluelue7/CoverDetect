//配置项
var colNumber = 1;	//列数
var rowNumber = 2;	//行数
var width = 300;	//框高
var height = 100;	//框宽


function makeUI() {
	//从html标签读取配置项
	var htmlColNumber = $('#UploadPic').attr('Col');
	var htmlRowNumber = $('#UploadPic').attr('Row');
	colNumber = htmlColNumber ? parseInt(htmlColNumber) : colNumber;
	rowNumber = htmlRowNumber ? parseInt(htmlRowNumber) : rowNumber;

	var htmlWidth = $('#UploadPic').attr('Width');
	var htmlHeight = $('#UploadPic').attr('Height');
	width = width ? parseInt(htmlWidth) : width;
	height = height ? parseInt(htmlHeight) : height;


	//开始搭建UI
	var html = "<table class='UploadPic'>";

	for (var i = 0; i < rowNumber; i++) {
		html += "<tr>";
		for (var j = 0; j < colNumber; j++) {
			html += "<td><input type='file' id='file_Input' name='pic" + (i * rowNumber + j + 1) + "' /></td>";
		}
		html += "</tr>";
	}
	html += "</table>";

	$('#UploadPic').html(html);
	$('.UploadPic tr td').css('width', width).css('height', height);
}

/**
根据input[file]对象获取添加的图片url
*/
function getObjectURL(file) {
	var url = null;
	if (window.createObjectURL != undefined) {
		url = window.createObjectURL(file)
	} else if (window.URL != undefined) {
		url = window.URL.createObjectURL(file)
	} else if (window.webkitURL != undefined) {
		url = window.webkitURL.createObjectURL(file)
	}
	return url
}


function changeToShow() {
    $('input[type="file"]').change(function () {
        var src = getObjectURL(this.files[0]);
        $(this).parent().css('background', 'url(' + src + ') no-repeat center center').css('background-size', '100%');
    });
}

// 页面加载完成，绑定选中显示图片和“开始检测”按钮的点击事件
$(document).ready(function () {
    makeUI();
    changeToShow();
});

