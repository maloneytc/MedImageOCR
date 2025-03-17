# MedImageOCR
Optical Character Recognition for Medical Images. 


## ocr.py
Uses Google's Tesseract engine for OCR.

### Installation
* OpenCV
** `pip install opencv-contrib-python` for full install or `pip install opencv-python` for partial
* pytesseract
** `pip install pytesseract`



## ocr_easy.py

### Build image
 ```docker build -t ocr:latest .```

### Build without a cache
```docker build --no-cache -t ocr:latest .```

### Run 
```docker run --rm -v <path to data directory>:/data ocr:latest /data/<zip file>```

### Run interactively
```docker run --rm -v <path to data directory>:/data --env "PYTHONUNBUFFERED=1" -it --entrypoint /bin/bash ocr:latest```

### Run with GPU
```docker run --rm --gpus all -v <path to data directory>:/data ocr:latest /data/<zip file>```
