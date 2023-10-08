import os
import pytesseract
import cv2
import numpy as np
import requests
import json
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\_\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
tessdata_dir = r'C:\Users\_\AppData\Local\Programs\Tesseract-OCR\tessdata'
os.environ['TESSDATA_PREFIX'] = tessdata_dir
url = 'https://medeczane.sgk.gov.tr/doktor/SayiUretenImageYeniServlet'
best_text = None
min_digits = 6
while best_text is None:
    response = requests.get(url)
    content = response.content
    with open('SayiUretenImageYeniServlet.png', 'wb') as f:
        f.write(content)
    img = cv2.imread('SayiUretenImageYeniServlet.png')
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    resized_img = cv2.resize(gray_img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    blurred_img = cv2.medianBlur(resized_img, 3)
    _, thresh_img = cv2.threshold(blurred_img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    kernel = np.ones((2, 2), np.uint8)
    dilated_img = cv2.dilate(thresh_img, kernel, iterations=1)
    config = '-c tessedit_char_whitelist=0123456789 --psm 6'
    text = pytesseract.image_to_string(dilated_img, config=config)
    filtered_text = ''.join([c for c in text if c.isdigit()])
    if len(filtered_text) == min_digits:
        best_text = filtered_text
result = {"result": [int(best_text)]}
result_json = json.dumps(result)
print(result_json)