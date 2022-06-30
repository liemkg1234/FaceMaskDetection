$(document).ready(function (){
    // Tao socket de connect toi server
    let namespace = '/detect'
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);

    // Tao cac bien
    let video = document.querySelector('#videoElement');
    let canvas = document.querySelector('#canvasElement');
    let ctx = canvas.getContext('2d');
    photo = document.getElementById('photo');

    // Tao funcion sendsnapshot, moi chu ki (1frame/20ms) se lay 1 frame trong video va gui ve cho server
    var localMedia = null;
    function sendSnapshot(){
        if (!localMedia){
            return;
        }

        // Dua video vao Canvas -> Gui Frame cho Server
        ctx.drawImage(video, 0, 0, video.videoWidth, video.videoHeight, 0, 0, 300, 150);
        // Frame type URL_base64
        let dataURL = canvas.toDataURL('image/jpeg');
        socket.emit('frame_Input', dataURL);
        socket.emit('output image');

        // Nhan Output tu Server
        socket.on('frame_Output', function (data){
            //Frame
            photo.setAttribute('src', data.img);
            //Class
            document.getElementById('class').innerText = data.class;
        });
    }


    // Truy cap vao webcam cua client va show len client
    var constraints = {video: {
        width: { min: 640 },
        height: { min: 480 }
    }};
    navigator.mediaDevices.getUserMedia(constraints)
        .then(function (stream){
            document.getElementById('videoElement').srcObject = stream;
            // thuc hien sendSnapshot theo chu ki
            localMedia = stream;
            setInterval(function () {sendSnapshot();}, 30); //CPU(ryzen7 4800h): 100ms, GPU(1660ti): 20ms

        }).catch(function (error){
            console.log(error);
    });
});