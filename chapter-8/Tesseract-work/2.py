import pytesseract
from PIL import Image
import numpy as np

# image = Image.open('下载.png')
# print(np.array(image).shape)
# print(image.mode)

# # image = image.convert('L')

# image = image.convert('RGB')
# print(image.mode)
  
def replace_non_white_with_black(image_path):  
    # 打开图像  
    img = Image.open(image_path)  
      
    # 确保图像是RGB模式，如果不是则转换  
    if img.mode != 'RGB':  
        img = img.convert('RGB')  
      
    # 获取图像的尺寸  
    width, height = img.size  
      
    # 创建一个新的空白图像，用于保存修改后的图像  
    new_img = Image.new('RGB', (width, height), 'white')  # 初始化为白色  
      
    # 遍历图像的每个像素  
    for x in range(width):  
        for y in range(height):  
            # 获取当前像素的颜色值  
            r, g, b = img.getpixel((x, y))  
              
            # 检查像素是否为白色（这里假设白色是(255, 255, 255)）  
            if (r, g, b) != (255, 255, 255):  
                # 如果不是白色，将其设置为黑色  
                new_img.putpixel((x, y), (0, 0, 0))  
            # 否则，保持原样（但在这个例子里，因为我们初始化了new_img为白色，所以这一步其实可以省略）  
      
    # 返回修改后的图像  
    return new_img  
image = replace_non_white_with_black('chapter-8\Tesseract-work\下载二.png')
string = pytesseract.image_to_string(image)
string1 = string.replace('\n', '')
string2 = string1.replace('\x0c', '')
# print(eval(string2))
image.show()

import numpy as np  
from PIL import Image  
  
def replace_non_white_with_black_numpy(image_path):  
    # 打开图像并转换为NumPy数组  
    img = np.array(Image.open(image_path))  
      
    # 替换非白色像素为黑色  
    img[np.all(img != 255, axis=-1)] = 0  
      
    # 将NumPy数组转换回Pillow图像  
    new_img = Image.fromarray(img.astype(np.uint8))  
      
    return new_img  
  
# 使用函数并保存结果  
# modified_img_numpy = replace_non_white_with_black_numpy('path_to_your_image.jpg')  
# modified_img_numpy.save('modified_image_numpy.jpg')