# Website phát hiện người đeo khẩu trang qua Camera
Trong đề tài này, mình xây dựng các mô hình Object Detection tiên tiến như [Yolov5](https://github.com/ultralytics/yolov5), [Efficientdet-Lite3](https://arxiv.org/pdf/1911.09070.pdf) và so sánh với mô hình Yolov3-tiny được tác giả xây dựng trong [bài báo này](https://link.springer.com/content/pdf/10.1007/s41403-020-00157-z.pdf).
Sau đó, mình sử dụng [Flask-SocketIO](https://flask-socketio.readthedocs.io/en/latest/) và [OpenSSL](https://www.openssl.org/) để xây dựng Website cho người dùng sử dụng chức năng phát hiện người đeo/không đeo khẩu trang qua Camera trong thời gian thực. Cuối cùng, mình đóng gói server bằng [docker](https://www.docker.com/) để dễ dàng triển khai ứng trên máy mới.

**Các thư viện sử dụng**
- [YOLOv5](https://github.com/ultralytics/yolov5)
- [Flask-SocketIO](https://flask-socketio.readthedocs.io/en/latest/)

# Docker
**Yêu cầu (chạy trên CPU)**
- [Docker Engine](https://docs.docker.com/engine/install/): 20.10.17
- [Ubuntu](https://ubuntu.com/download/desktop): 20.04 (Thêm WSL2 nếu cài trên Window)

**Yêu cầu thêm (nếu chạy trên GPU)**
- [NVIDIA Driver](https://www.nvidia.com/download/index.aspx)
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#docker)

**Run**
```
docker pull liemkg1234/fmdetection:mytag
docker run  -d -p 5000:5000 liemkg1234/fmdetection:mytag (CPU)
docker run --gpus all -d -p 5000:5000 --ulimit memlock=-1 --ulimit stack=67108864 liemkg1234/fmdetection:mytag (GPU)
https://(Your IPv4 Address):5000
```

# Pip
**Môi trường**
- [Google Colaboratory](https://research.google.com/colaboratory/)
- Pycharm
- Python 3.9.2
- CUDA Version: 11.2

**Run demo**
```
git clone https://github.com/liemkg1234/Websocket_FaceMaskDetection
cd Websocket_FaceMaskDetection
pip install -r requirements.txt
python app.py
```

## Sơ đồ tổng quát
![samples](https://github.com/liemkg1234/Websocket_FaceMaskDetection/blob/master/images/sodotongquat.PNG)

## Tập dữ liệu
- [Moxa3K](https://shitty-bots-inc.github.io/MOXA/index.html): Gồm 3000 hình ảnh được chia tỷ lệ Train/Validation/Test là 2400/400/200
- [Face Mask Detection](https://www.kaggle.com/datasets/andrewmvd/face-mask-detection): Gồm 853 hình ảnh được chia tỷ lệ Train/Validation/Test là 600/200/53

## Kết quả thực nghiệm
Các thông số chung:
- Img_size: 416x416
- Batch_size: 16
- Epochs: 100

**Moxa3k**

| Model | Size (MB) |   | AP@0.5 (%) |   | AP@[0.5:0.05:0.95] (%) |
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
|   |   | All | No_mask | Mask |   |
| Yolov3-tiny | 33.2 | 56.3 | 38.8 | 72.6 | _ |
| Yolov5s | 13.6 | 73.1 | 59.4 | 86.8 | 30.9 |
| Yolov5x | 165.0 | 71.1 | 57.9 | 84.3 | 30.3 |
| EfficientDet-Lite3 | 11.2 | 67.9 | _ | _ | 26.5 |

**Face Mask Detection**

| Model | Size (MB) |   | AP@0.5 (%) |   | AP@[0.5:0.05:0.95] (%) |
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
|   |   | All | No_mask | Mask |   |
| Yolov3-tiny | 33.2 | 72.6 | 62.3 | 82.8 | _ |
| Yolov5s | 13.6 | 84.9 | 79.5 | 90.3 | 47.8 |
| Yolov5x | 165.0 | 82.5 | 75.5 | 89.5 | 48.1 |
| EfficientDet-Lite3 | 11.2 | 82.1 | _ | _ | 53.7 |

## Demo

https://www.youtube.com/watch?v=76KhB_ZdmHE
![samples](https://github.com/liemkg1234/Websocket_FaceMaskDetection/blob/master/images/demo.PNG)
![samples](https://github.com/liemkg1234/Websocket_FaceMaskDetection/blob/master/images/demo2.PNG)

### Liên hệ
Email:  liemkg1234@gmail.com
