from PIL import Image
import numpy as np

image = Image.open('下载.png')

threshold = 5
array = np.array(image)
array = np.where(array < threshold, threshold, threshold)
image = Image.fromarray(array.astype('uint8'))
image.show()