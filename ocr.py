from pathlib import Path
import pydicom as pdm
from PIL import Image, ImageOps
import cv2
import numpy as np
import pytesseract
from pytesseract import Output
import matplotlib.pyplot as plt

def dcm_ocr(dcm_path):
    dcm = pdm.read_file(dcm_path)
    pix_array = dcm.pixel_array
    
    if pix_array.ndim == 2:
        text = ocr_grayscale(pix_array)
    elif pix_array.ndim == 3:
        text = ocr_rgb(pix_array)
        
    return text
        
def ocr_grayscale(pix_array, all_data=False):
    norm_img = np.zeros_like(pix_array)
    img = cv2.normalize(pix_array, norm_img, 0, 255, cv2.NORM_MINMAX)
    val, img = cv2.threshold(img, 250, 255, cv2.THRESH_BINARY_INV)

    pil_image = Image.fromarray(np.uint8(img))
    
    if all_data:
        results = pytesseract.image_to_data(pil_image, config='--psm 11', lang='eng', output_type=Output.DICT)
        return results
    
    img_string = pytesseract.image_to_string(pil_image, config='--psm 11', lang='eng')
    return img_string
    
def ocr_rgb(pix_array, all_data=False):
    """
    Assumes that the text is bright.
    """
    pil_rgb_image = Image.fromarray(np.uint8(pix_array))
    pil_gray_image = ImageOps.grayscale(pil_rgb_image)
    norm_img = np.zeros_like(np.asarray(pil_gray_image))
    img = cv2.normalize(np.asarray(pil_gray_image), norm_img, 0, 255, cv2.NORM_MINMAX)
    val, img = cv2.threshold(img, 20, 255, cv2.THRESH_BINARY_INV)
    
    if all_data:
        results = pytesseract.image_to_data(img, config='--psm 11', lang='eng', output_type=Output.DICT)
        return results
    
    img_string = pytesseract.image_to_string(img, config='--psm 11', lang='eng')
    return img_string

def show_ocr(dcm_path, conf_thr=25):
    dcm = pdm.read_file(dcm_path)
    pix_array = dcm.pixel_array
    if pix_array.ndim == 2:
        labeled_image = np.repeat(pix_array[:, :, np.newaxis], 3, axis=2)
        results = ocr_grayscale(pix_array, all_data=True)
        
    elif pix_array.ndim == 3:
        labeled_image = dcm_rgb.copy()
        results = ocr_rgb(pix_array, all_data=True)

    for i in range(0, len(results["text"])):
        x = results["left"][i]
        y = results["top"][i]

        w = results["width"][i]
        h = results["height"][i]    
        pad = 2
        text = results["text"][i]
        conf = int(results["conf"][i])    
        if conf > conf_thr:
            text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
            cv2.rectangle(labeled_image, (x - pad, y - pad), (x + w + pad, y + h + pad), (0, 255, 0), 1)
            cv2.putText(labeled_image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 0, 0), 2)

    plt.figure(figsize=(10,10))
    plt.imshow(labeled_image, cmap='gray')
