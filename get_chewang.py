#!python3
import requests
import shutil
import os
import zipfile
import time
import datetime
import sys

dir_name = 'post_chewang'
zip_name = "post_chewang.zip"
url = 'http://10.2.52.29:9000/post_chewang.zip'
password = '1472'

def rmtree(bak=True):
	if os.path.isdir(dir_name):
		if bak:
			os.rename(dir_name,f'{dir_name}_bak_{datetime.datetime.now().strftime("%Y%m%d-%H%M%S")}')
			print(f'原始文件夹{dir_name}备份完成')
		else:
			shutil.rmtree(dir_name)
			print(f'原始文件夹{dir_name}删除完成')
	else:
		print(f'原始文件夹{dir_name}不存在，不删除了')
def download_zip():
	r = requests.get(url)
	with open(zip_name, "wb") as code:
		code.write(r.content)
	print(f'{zip_name}下载完成')
def unzip():
	zip_file = zipfile.ZipFile(zip_name)
	for names in zip_file.namelist():
		zip_file.extract(names,'')
	zip_file.close()
	print(f'解压文件{zip_name}完成')
	
def rm_zip():
	os.remove(zip_name)
	print(f'删除文件{zip_name}')
	
if __name__ == '__main__':
	s = input('请输入执行密码')
	if s != password:
		print('密码输入错误')
		time.sleep(5)
		sys.exit(-1)
	download_zip()
	rmtree()
	unzip()
	rm_zip()
	time.sleep(2)

