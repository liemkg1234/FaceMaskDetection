#Docker in Yolov5 (Using GPU) https://github.com/ultralytics/yolov5/wiki/Docker-Quickstart
# 1660ti - CUDA Version: 11.7 >>> Driver Version: 517.48 >>> (cmd : nvidia-smi)
# Install Nvidia-Docker      NVIDIA Container Toolkit
# Docker Engine - CE : 20.10.17

#######
# Start FROM NVIDIA PyTorch image https://ngc.nvidia.com/catalog/containers/nvidia:pytorch #docker run --gpus all -it --rm nvcr.io/nvidia/pytorch:22.04-py3
FROM nvcr.io/nvidia/pytorch:22.04-py3
RUN rm -rf /opt/pytorch  # remove 1.2GB dir

# Downloads to user config dir
ADD https://ultralytics.com/assets/Arial.ttf https://ultralytics.com/assets/Arial.Unicode.ttf /root/.config/Ultralytics/

# Install linux packages
RUN apt update && apt install --no-install-recommends -y zip htop screen libgl1-mesa-glx

# Install pip packages
COPY requ.txt .
RUN python -m pip install --upgrade pip
RUN pip uninstall -y torch torchvision torchtext Pillow
RUN pip install --no-cache -r requ.txt albumentations wandb gsutil notebook Pillow>=9.1.0 \
    torch torchvision --extra-index-url https://download.pytorch.org/whl/cu113

# Create working directory
RUN mkdir -p /app
WORKDIR /app

# Copy contents
COPY . /app

# Set environment variables
ENV OMP_NUM_THREADS=8

# requirements(Flask, evenlent, ...)
RUN pip install -r requirements.txt

#Run
#EXPOSE 5000
CMD ["python", "app.py"]

#Build
# docker build -t fmdetection .
#docker run --gpus all -d -p 5000:5000 --ulimit memlock=-1 --ulimit stack=67108864 fmdetection_ubuntu
# docker run  -d -p 5000:5000 fmdetection


#  Push
# docker tag e1dd2b08be8c liemkg1234/fmdetection:mytag
# docker push liemkg1234/fmdetection:mytag

# python
# import torch
# print(torch.cuda.is_available())