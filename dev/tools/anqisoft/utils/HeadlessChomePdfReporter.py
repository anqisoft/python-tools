# pip install selenium==3.9.0
'''
	Author: anqisoft@gmail.com
	Date:   2023-09-21
	Python: 3.9.0
'''
import base64
import json

from selenium.webdriver.chrome.webdriver import WebDriver


class HeadlessChomePdfReporter:
	# Nearly sixty years ago, the inch was redefined to be exactly 25.4 millimeters,
	# so that conversion is now exact to any number of decimal places.
	# Previously, the inch had been defined by setting 39.37 inches to be exactly one meter
	# (i.e. 2.54000508 cm/inch).
	MM_TO_INCH_SCALE = 1 / 25.4
	MM_4 = 0.15748
	MM_5 = 0.19685
	MM_210 = 8.26772
	MM_297 = 11.6929
	MM_420 = 16.5354

	# Thanks: Life is complex, https://stackoverflow.com/users/6083423/life-is-complex
	# See: https://stackoverflow.com/questions/68164550/selenium-print-pdf-in-a4-format
	# Removed the 'driver' params from send_devtools and create_pdf
	def __init__(self, driver: WebDriver = None, options=None):
		if driver is None:
			driver = self.create_headless_chrome_driver(options)
		self.driver = driver

	def send_devtools(self, command, params=None):
		if params is None:
			params = {}

		driver = self.driver
		resource = '/session/%s/chromium/send_command_and_get_result' % driver.session_id
		url = driver.command_executor._url + resource
		body = json.dumps({'cmd': command, 'params': params})
		resp = driver.command_executor._request('POST', url, body)
		return resp.get('value')

	def create_pdf(self, file_name, params=None):
		if params is None:
			# https://vanilla.aslushnikov.com/?Page.printToPDF
			params = {
				'paperWidth': self.MM_210,
				'paperHeight': self.MM_297,

				'marginTop': self.MM_4,
				'marginBottom': self.MM_4,
				'marginLeft': self.MM_4,
				'marginRight': self.MM_4,
			}

		driver = self.driver
		command = 'Page.printToPDF'
		result = self.send_devtools(command, params)
		self.save_pdf(result, file_name)
		return

	def save_pdf(self, data, file_name):
		with open(file_name, 'wb') as file:
			file.write(base64.b64decode(data['data']))

	# print('PDF created')

	def create_headless_chrome_driver(self, options=None):
		from selenium.webdriver.chrome.options import Options as ChromeOptions

		if options is None:
			options = ChromeOptions()
			options.add_argument('--headless')
			options.add_argument('--start-maximized')
			options.add_argument("--disable-infobars")
			options.add_argument("--disable-extensions")
			options.add_argument("--disable-popup-blocking")

		# pip install webdriver-manager
		# https://stackoverflow.com/questions/38959885/python-selenium-permissionerror-winerror-5-access-is-denied
		# Download the driver for your chrome version, and place it on your chrome path.
		# http://chromedriver.chromium.org/downloads
		# from webdriver_manager.chrome import ChromeDriverManager
		# from selenium.webdriver.chrome.service import Service
		# from webbrowser import Chrome
		# driver = Chrome(service=Service(ChromeDriverManager().install()), options=options)

		# Replace it if needs.
		PATH_OF_CHROME_DRIVER = r'D:\dev\selenium\chromedriver.exe'

		from selenium import webdriver
		driver = webdriver.Chrome(executable_path=PATH_OF_CHROME_DRIVER, options=options)
		driver.maximize_window()

		self.driver = driver
		return driver

	def open_url_and_create_pdf(self, url: str, filename: str, params=None):
		driver = self.driver
		driver.get(url)

		self.create_pdf(filename, params)
		return self

	def quit(self):
		self.driver.quit()


if __name__ == '__main__':
	from os import path, makedirs

	GOAL_PATH = 'pdfs/'
	if not path.exists(GOAL_PATH):
		makedirs(GOAL_PATH)

	MM_4 = HeadlessChomePdfReporter.MM_4
	MM_210 = HeadlessChomePdfReporter.MM_210
	MM_297 = HeadlessChomePdfReporter.MM_297
	MM_420 = HeadlessChomePdfReporter.MM_420

	# https://vanilla.aslushnikov.com/?Page.printToPDF
	params = {
		# landscape: False,

		'paperWidth': MM_297,
		'paperHeight': MM_420,

		'marginTop': MM_4,
		'marginBottom': MM_4,
		'marginLeft': MM_4,
		'marginRight': MM_4,
	}

	reporter = HeadlessChomePdfReporter()
	for (url, pdf_file_name) in [
		('https://anqisoft.github.io/express_box_a3_use_svg.htm', 'express_boxes'),
		('https://anqisoft.github.io/box.htm', 'box'),
	]:
		# reporter.open_url_and_create_pdf(url, path.join(GOAL_PATH, f'{pdf_file_name}.pdf'), params)
		reporter.open_url_and_create_pdf(url, path.join(GOAL_PATH, f'{pdf_file_name}.pdf'), None)

	reporter.quit()
