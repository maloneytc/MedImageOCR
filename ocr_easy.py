import sys
import zipfile
import io
import pydicom

from PIL import Image, ImageOps
import numpy as np

import easyocr


def ocr(dcm_file, conf_thresh=0.5):
    try:
        this_dcm = pydicom.read_file(dcm_file)
    except Exception as e:
        raise e
    
    # Use verbose = False to suppress message about using the CPU vs GPU
    reader = easyocr.Reader(['en'], gpu=False, verbose=False)

    pix_array = this_dcm.pixel_array
    pil_image = Image.fromarray(np.uint8(pix_array))
    result = reader.readtext(np.array(pil_image.convert('RGB')))
    
    ocr_text = []
    
    if len(result) > 0:
        for this_res in result:
            bb, text, conf = this_res
            if conf > conf_thresh:
                ocr_text.append({'bounds':[[int(that) for that in this] for this in bb], 'text':text, 'confidence':float(conf)})

    return {'OCR': ocr_text, 'StudyUID': this_dcm.StudyInstanceUID, 'SeriesUID': this_dcm.SeriesInstanceUID}


def zip_ocr(zip_path, conf_thresh=0.5):
    results = []
    read_series = []

    with zipfile.ZipFile(zip_path) as this_zip:
        for file_name in this_zip.namelist():
            data = this_zip.read(file_name)
            file_obj = io.BytesIO(data)

            try:
                this_dcm = pydicom.read_file(file_obj)
                file_obj.seek(0)
            except:
                results.append({'file_name':file_name, 'Error': "Could not read file as a DICOM."})
                continue
            
            ## Only read one file per series
            try:
                if this_dcm.SeriesInstanceUID in read_series:
                    continue
                else:
                    read_series.append(this_dcm.SeriesInstanceUID)
            except:
                results.append({'file_name':file_name, 'Error': "Could not read Series UID."})
                continue
            
            result = ocr(file_obj, conf_thresh=conf_thresh)
            result['file_name'] = file_name
            result['Error'] = None

            results.append(result)

    return results

if __name__ == "__main__":
    zip_file = sys.argv[1]
    res = zip_ocr(zip_file)

    print(res)
