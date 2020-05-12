from PIL import Image
from pytesseract import *
img0 = Image.open('/home/pi/Desktop/book.png')
mychars = image_to_string(img0,'chi_sim').strip()
print(mychars)
