# Create time:2018-12-14 15:26
# Author:Chen

import requests
import random
import base64


class OcrBaidu:

	def __init__(self):
		# 过期时间30天
		self.access_token_list =[
			"24.84bded3564c54ee29eb56774c350b7b1.2592000.1549695768.282335-14594301",
			"24.c5c5f05a9c3fd5bbccdfe0c47fa0ff32.2592000.1549695826.282335-15163958",
			"24.85fc209481352cd05119d8d36dde87ed.2592000.1549695880.282335-15164274"]

	def ocr(self, image_bin, level):
		"""
		将image_bin二进制转换为base64，发送post请求识别图片中字符
		:param image_bin: 图片二进制数据
		:param level: 识别等级，通用识别精度低，每天免费次数多，高精度免费次数少
		:return: 识别出的字符
		"""
		image = base64.b64encode(image_bin)
		files = {
			"image": image,
		}
		if level == 'low':
			# 通用orc识别
			url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token={}"
		else:
			# 高精度orc识别
			url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token={}"
		# 三个账号中随机选一个使用
		access_token = random.choice(self.access_token_list)
		r = requests.post(
			url.format(access_token),
			headers={"Content-Type": "application/x-www-form-urlencoded"},
			data=files)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		# 返回图片中识别出的文字
		words = eval(r.text)["words_result"][0]["words"]
		return words

	@staticmethod
	def access_token(api_key, secret_key):
		"""
		根据用户app的apiKey和secretKey获取accessToken，获取一遍即可，可重复使用
		:param api_key:
		:param secret_key:
		:return:
		"""
		url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&" + \
			f"client_id={api_key}&client_secret={secret_key}&"
		r = requests.post(url)
		access_token_str = eval(r.text)["access_token"]
		return access_token_str


if __name__ == "__main__":
	print(OcrBaidu().access_token("appId", "secretStr"))