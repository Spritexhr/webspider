import pytesseract
from PIL import Image
# 读取图片
im = Image.open('下载 (1).png')
# 识别文字
string = pytesseract.image_to_string(im)
print(string)