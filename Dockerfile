FROM ubuntu:22.04

WORKDIR /app
COPY . .

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 curl libjpeg-dev vim tesseract-ocr -y
RUN apt-get upgrade -y

RUN apt-get -y install python3-pip

RUN pip3 install pylibjpeg pylibjpeg-libjpeg pydicom
RUN pip3 install opencv-python==4.6.0.66
RUN pip3 install pytesseract
RUN pip3 install pillow
RUN pip3 install matplotlib
RUN pip3 install easyocr

# Initialize easyocr by downloading the english model
RUN python3 init_ocr.py

ENTRYPOINT [ "python3", "-u", "ocr_easy.py" ]