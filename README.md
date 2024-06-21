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
```docker run --rm -v /Volumes/AMBRA_Backup/ERICH-GENE/All_Data___De_Identified/02-21-394359/CT_2_16_840_1_114444_637165914114654373_2063130837_20200123:/data ocr:latest /data/CT_20200123.zip```

### Run interactively
```docker run --rm -v /Volumes/AMBRA_Backup/ERICH-GENE/All_Data___De_Identified/02-21-394359/CT_2_16_840_1_114444_637165914114654373_2063130837_20200123:/data --env "PYTHONUNBUFFERED=1" -it --entrypoint /bin/bash ocr:latest```