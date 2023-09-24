#  pip install selenium==3.9.0

import json

from anqisoft.utils import HeadlessChomePdfReporter
from anqisoft.utils import Tester


def open_url_and_export_pdf(input: str) -> int:
	reporter = HeadlessChomePdfReporter()

	MM_4 = HeadlessChomePdfReporter.MM_4
	MM_210 = HeadlessChomePdfReporter.MM_210
	MM_297 = HeadlessChomePdfReporter.MM_297
	MM_420 = HeadlessChomePdfReporter.MM_420

	# https://vanilla.aslushnikov.com/?Page.printToPDF
	default_params = {
		# landscape: False,

		'paperWidth': MM_297,
		'paperHeight': MM_420,

		'marginTop': MM_4,
		'marginBottom': MM_4,
		'marginLeft': MM_4,
		'marginRight': MM_4,
	}

	from os import path, makedirs

	# https://blog.51cto.com/yunyaniu/2912553
	with open(input, 'r', encoding='utf-8') as json_file:
		# https://www.freecodecamp.org/chinese/news/python-parse-json-how-to-read-a-json-file/
		# print(json.dumps(fcc_data, indent=4))
		# TypeError: the JSON object must be str, bytes or bytearray, not TextIOWrapper
		# data = json.loads(json_file)
		data = json.load(json_file)

		for item in data:
			# print(item)
			# url, pdf, params = json.loads(item)
			url = item['url']
			pdf = item['pdf']
			params = item['params']
			# print(url, pdf, params)

			if not pdf.endswith('.pdf'):
				# print('pdf not endswith(".pdf")', pdf)
				pdf = f'{pdf}.pdf'
			print(pdf, url)

			# <class 'str'> print(type(params))
			# params = json.loads(params)

			GOAL_PATH = path.split(pdf)[0]
			if not path.exists(GOAL_PATH):
				makedirs(GOAL_PATH)

			# reporter.open_url_and_create_pdf(url, path.join(GOAL_PATH, f'{pdf}.pdf'), default_params if params is None else params)

			# https://juejin.cn/post/6844903490427289614
			# reporter.open_url_and_create_pdf(url, pdf, default_params if params is None else {**default_params, **params})
			reporter.open_url_and_create_pdf(url, pdf, {**default_params, **params})

	reporter.quit()


def main():
	'''
		<en>Parse the console parameters:
			-F or --feature: feature name
			-I or --input: input info
			-O or --output: output info
		</en>
		<zh_cn>解析控制台参数：
			-F或--feature：功能名
			-I或--input：输入信息
			-O或--output：输出信息
		</zh_cn>
		<zh_tw>解析控制台參數：
            -F或--feature：功能名
            -I或--input：輸入資訊
            -O或--output：輸出資訊
		</zh_tw>
	'''
	import sys
	import getopt

	try:
		feature = ''
		input = ''
		output = ''
		opts, args = getopt.getopt(sys.argv[1:], 'F:I:O:', ['feature=', 'input=', 'output='])
		for opt, arg in opts:
			if opt in ('-F', '--feature'):
				feature = arg
			elif opt in ('-I', '--input'):
				input = arg
			elif opt in ('-O', '--output'):
				output = arg
		if feature == 'openUrlAndExportPdf':
			open_url_and_export_pdf(input)

	except getopt.GetoptError:
		sys.exit(2)


if __name__ == '__main__':
	Tester.do_and_show_used_time(main, 'Main')
	# main()