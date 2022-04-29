


function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toGMTString();
    document.cookie = cname + "=" + cvalue + "; " + expires;
}
function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i].trim();
        if (c.indexOf(name) == 0) { return c.substring(name.length, c.length); }
    }
    return "";
}
$(document).ready(function () {
    var isUpload1 = false;
    var isUpload2 = false;
    var isOK = getCookie("fileName");
    if (isOK != '') {
        ShowSourced();
    }
    $('#inputFile').change(function (evt) {
        isUpload1 = true;
        var _file = this.files[0],
            //获取的的图片
            fileType = _file.type; //图片类型 



        setCookie("fileName", _file.name, 30);
        var reader = new FileReader();
        reader.readAsDataURL(_file);
        reader.onload = function (e) {
            // txshow.src = this.result;
            var base64 = this.result.substring(this.result.indexOf(',') + 1);
            changeImg(base64, '#coreImg')
            console.log(base64);
        }


        // base64 = getBase64Image(_file);
    })
    $('#submitSource').on('click', function () {
        if (isUpload1 == false) {
            alert('请先上传图片')
            return
        }
        console.log('true')
        ShowSourced();
        isUpload1 = false;

    })

    // 下面是相似度计算的第2图片

    $('#inputFile2').change(function (evt) {
        isUpload2 = true;
        var _file = this.files[0],
            //获取的的图片
            fileType = _file.type; //图片类型 
        setCookie("fileName2", _file.name, 30);
        var reader = new FileReader();
        reader.readAsDataURL(_file);
        reader.onload = function (e) {
            // txshow.src = this.result;
            var base64 = this.result.substring(this.result.indexOf(',') + 1);
            changeImg(base64, '#coreImg')
            console.log(base64);
        }



        // base64 = getBase64Image(_file);
    })
    $('#submitSource2').on('click', function () {
        if (isUpload2 == false) {
            alert('请先上传图片')
            return
        }
        console.log('true')
        SimilarityCompare();
        isUpload2 = false;
    })





})

function uploading(fileName) {
    // var formData = new FormData();
    // formData.append('file', $('#upload')[0].files[0]);
    $.ajax({
        url: 'http://127.0.0.1:5050/source',
        type: 'POST',
        data: '',

        success: function (data) {
            console.log(data['file'])
            img = changeImg(data['file'], '#coreImg')
            console.log('success!')
        },
        error: function () {
            console.log('error');
        }
    });
}

function changeImg(data, idString) {

    img = 'data:image/jpeg;base64,' + data;
    $(idString).attr('src', img);
    // $(idString).animate({
    //     animate__bounceIn
    // });
    return img;
}



// //组件更新
// var $update = document.querySelector("#update");
// $update.addEventListener("click", function () {
//     simpleCrop.updateBox({
//         cropSizePercent: 0.7,
//         size: {
//             width: 600,
//             height: 600,
//         },
//     });
//     simpleCrop.initBoxBorder({
//         borderColor: "#0BFF00",
//     });
//     simpleCrop.show();
// });


// uploadFile(files[0])

function CannyDetect() {
    $.ajax({
        url: 'http://127.0.0.1:5050/CannyDetect',
        type: 'POST',
        data: '',

        success: function (data) {
            console.log(data['file'])
            img = changeImg(data['file'], '#coreImg')
            console.log('success!')
        },
        error: function () {
            console.log('error');
        }
    });
}

function ConnerDetect() {
    $.ajax({
        url: 'http://127.0.0.1:5050/HarrisDetect',
        type: 'POST',
        data: '',
        success: function (data) {
            console.log(data['file'])
            img = changeImg(data['file'], '#coreImg')
            console.log('success!')
        },
        error: function () {
            console.log('error');
        }
    });
}


function ConnerDetect2() {
    $.ajax({
        url: 'http://127.0.0.1:5050/SubPixDetect',
        type: 'POST',
        data: '',

        success: function (data) {
            console.log(data['file'])
            img = changeImg(data['file'], '#coreImg')
            console.log('success!')
        },
        error: function () {
            console.log('error');
        }
    });
}

function FaceDetect() {
    $.ajax({
        url: 'http://127.0.0.1:5050/FaceDetect',
        type: 'POST',
        data: '',

        success: function (data) {
            console.log(data['file'])
            img = changeImg(data['file'], '#coreImg')
            console.log('success!')
        },
        error: function () {
            console.log('error');
        }
    });
}
function SimilarityCompare() {


    $.ajax({
        url: 'http://127.0.0.1:5050/ImageSimilarity',
        type: 'POST',
        data: '',

        success: function (data) {
            if (data['msg'] == '-2') {
                alert('请先上传图片')
                return
            }
            console.log(data['result'])
            img = changeImg(data['file'], '#coreImg')
            alert("两张图的相似度是" + data['result'])
        },
        error: function () {
            console.log('error');
        }
    });
};
function ShowSourced() {
    $.ajax({
        url: 'http://127.0.0.1:5050/source',
        type: 'POST',
        data: '',

        success: function (data) {
            console.log(data['file'])
            img = changeImg(data['file'], '#coreImg')
            console.log('success!')
        },
        error: function () {
            console.log('error');
        }
    });
}






// var mask = '<div id="hicap_mask" style="width:100%;height:100rem;top:0px;left:0px;position:fixed;background:#FFF;opacity:0.9;z-index:998;"></div>';
// var loading = '<div id="loading"><img src="/public/images/loading.gif" style="width:10rem;position:absolute;left:50%;top:50%;z-index:999;margin-left:-5rem;margin-top:-5rem;" /></div>';

// $(document).on('ajaxStart', function (e) {
//     $(mask).appendTo('.wrapper1');
//     $(loading).appendTo('.wrapper1');
// })

// $(document).on('ajaxStop', function (e) {
//     $("#hicap_mask").remove();
//     $("#loading").remove();
// })










// var isUpload = false;
// $(document).ready(function () {
//     // imgPath = uploading('source.jpg');
//     var simpleCrop = new SimpleCrop({
//         title: "图片裁剪",
//         src: './images/img_13.png',
//         size: {
//             width: 800,
//             height: 600,
//         },
//         cropSizePercent: 0.6,
//         funcBtns: ["close", "crop", "reset"],
//         borderColor: "#fff",
//         coverColor: "rgba(0,0,0,.5)",
//         startAngle: -360,
//         endAngle: 360,
//         cropCallback: function ($resultCanvas) {
//             console.log("cropCallback");
//             $resultCanvas.style.marginRight = "10px";
//             $resultCanvas.style.width = "50%";
//             $('upload').value = $resultCanvas;

//             // document.body.appendChild($resultCanvas);
//         },
//         uploadCallback: function (src) {
//             console.log("uploadCallback " + src);
//         },
//         closeCallback: function () {
//             console.log("closeCallback");
//         },

//     });


//     // 选取裁剪图片;
//     $('#submitSource').on('click', function () {
//         isUpload = true;
//         console.log('true')
//         console.log($('#upload').value)
//     })
//     $("#upload").change(function (evt) {

//         var files = evt.target.files;
//         if (files.length > 0) {

//             simpleCrop.show(files[0]);
//         }


//     });


// })