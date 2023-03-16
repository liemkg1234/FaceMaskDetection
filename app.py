from flask import Flask, render_template
from flask_socketio import SocketIO, emit

import numpy as np
from PIL import Image
import torch

from tools.convert_PIL_base64 import base64_to_pil_image, pil_image_to_base64
from tools.torch_utils import draw_bboxs, non_max_suppression_fast


model = torch.hub.load('ultralytics/yolov5', 'custom', path='model/853_Yolov5s/weights/best.pt', force_reload=True) #, force_reload=True
# nguong(threshold) confidence va IOU
model.conf = 0.6 #yolov5/models/common.py/AutoShape(line 527)
model.iou = 0.5

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
socketio = SocketIO(app, async_mode='eventlet', cors_allowed_origins='*') # , async_mode='gevent', cors_allowed_origins=['http://localhost:5000', 'https://localhost:5000']

# Nghe cac ket noi cua Client
@socketio.on('connect', namespace='/detect')
def connect():
    app.logger.info("Client da ket noi voi may chu")

# Nhan Frame tu Client -> Detect -> Gui lai Frame cho Client
@socketio.on('frame_Input', namespace='/detect')
def getImage(input): #type('str' base64URL)
    input = input.split(",")[1]
    image_data = input

    #Base64_2_PIL
    img_pil = base64_to_pil_image(image_data)
    #PIL_2_CV2
    img_cv2 = np.array(img_pil)

    # Detect facemask and draw bbox
    boxs = model(img_cv2)
    xxyy_pandas = boxs.pandas().xyxy[0]
    xxyy_pandas = non_max_suppression_fast(xxyy_pandas, 0.3)
    # print(xxyy_pandas)
    #draw bounding box
    img_out = draw_bboxs(img_cv2, xxyy_pandas, (255, 0, 0), (0, 255, 0), 1)
    list_class = xxyy_pandas['name'].tolist()
    str_class = ', '.join(str(x) for x in list_class)
    # print(str_class)

    #CV2_2_PIL
    img = Image.fromarray(img_out)

    #PIL_2_base64URL
    image_data = pil_image_to_base64(img).decode("utf-8")
    image_data = "data:image/jpeg;base64," + image_data

    # Gui frame&class len client
    emit('frame_Output', {'img': image_data, 'class': str_class}, namespace='/detect')


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, keyfile='key.pem', certfile='cert.pem') #https://192.168.0.110:5000/ (Wifi LAN IPv4 address) cmd ipconfig
    # socketio.run(app) port=os.environ['PORT']
