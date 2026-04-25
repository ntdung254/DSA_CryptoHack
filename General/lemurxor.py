"""Kết hợp dữ liệu của hai tệp ảnh bằng các phép tính trên từng điểm ảnh để làm lộ ra thông tin ẩn."""
from PIL import Image
import numpy as np

img1 = Image.open("lemur.png")
img2 = Image.open("flag.png")

data1 = np.array(img1)
data2 = np.array(img2)

res_data = np.bitwise_xor(data1, data2)

res_img = Image.fromarray(res_data)
res_img.save("result.png")
res_img.show()
