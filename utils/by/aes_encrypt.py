# _*_ coding: utf-8 _*_
# @Time     :   2020/8/21 10:40
# @Author       vanwhebin
import os
import execjs


class Encrypt:
	aes_dir = "utils" + os.sep + "aes"

	def get_js(self):
		js_dir = os.path.join(os.getcwd(), self.aes_dir)
		# js_files = os.listdir(js_dir)
		js_files = ['aes.js', 'ecb-mode.js']
		js_str = ''
		for js_file in js_files:
			f = open(os.path.join(js_dir, js_file), 'r', encoding='utf-8')  # 打开JS文件
			line = f.readline()
			while line:
				js_str = js_str + line
				line = f.readline()
		return js_str

	def get_aes_pass(self, pwd):
		js_str = self.get_js()
		ctx = execjs.compile(js_str)
		return ctx.call('Encrypt', pwd)

