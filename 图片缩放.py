import os
import os.path
from PIL import Image


# 获取当前路径
baseDir = os.getcwd()
# 得到所有路径下的图片
files = list(filter(lambda x: x!='图片缩放.py' and x!='output', os.listdir('.')))
print('初始化完成')
for file in files:
    try:
        img = Image.open(file)
        newSize = int(img.size[0] * 8 / 10), int(img.size[1] * 8 / 10)
        img = img.resize(newSize, Image.ANTIALIAS)
        output = os.path.join(baseDir, 'output')
        if not os.path.exists(output):
            os.mkdir(output)
        img.save(os.path.join(output,file))
        print(file,'转换完成')
    except OSError as e:
       print(e,file,'转换失败')
input('\n转换彻底完成,按任意键退出。。。')
