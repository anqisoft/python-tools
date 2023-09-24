import sys
import time
from datetime import datetime

class Tester:
	DEBUGGING = True

	def __init__(self):
		pass

	def do_and_show_used_time(func: callable, func_name: str, level: int = 0) -> int:
		'''
			Call a callable function, and show used time.\n
			:param func A callable function\n
			:param func_name The name of callable function\n
			:return 0 means success, and 1 means fail.
		'''
		if Tester.DEBUGGING:
			start_datetime = datetime.now()
			start = time.time()

		TABS = '\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t'[0:level]
		has_error = False
		try:
			func()
		except Exception as e:
			has_error = True
			print(f'{TABS}has error: ', e)
			if Tester.DEBUGGING:
				exc_type, exc_val, exc_tb = sys.exc_info()
				print(exc_type)
				print(exc_val, type(exc_val))
				print(exc_tb)

		# https://cloud.tencent.com/developer/article/1731086
		# It's useless right over here.
		# print(traceback.format_exc())
		# traceback.print_exc()
		finally:
			if Tester.DEBUGGING:
				end = time.time()
				print(f'{TABS}{func_name} used {end - start:,.3f} seconds.')

				print(f'{TABS}\tto', datetime.now().strftime('%Y%m%d %H:%M:%S.%f'))
				print(f'{TABS}\tgo', start_datetime.strftime('%Y%m%d %H:%M:%S.%f'))
			pass

		return 1 if has_error else 0


def test_tester_do_and_show_used_time():
	def func0():
		for i in range(0, 1000):
			for j in range(0, 10000):
				i * j
		return 0

	def func1():
		division = 0
		# ZeroDivisionError: integer division or modulo by zero
		return 1 % division

	def func2():
		a = []
		a.append(1)
		# IndexError: list index out of range
		return a[1]

	# print(Tester.do_and_show_used_time(func0, 'Call normal function', 1))
	# print(Tester.do_and_show_used_time(func1, 'Call a function with ZeroDivisionError', 1))
	# print(Tester.do_and_show_used_time(func2, 'Call a function with IndexError', 1))

	Tester.do_and_show_used_time(func0, 'Call normal function', 1)
	Tester.do_and_show_used_time(func1, 'Call a function with ZeroDivisionError', 1)
	Tester.do_and_show_used_time(func2, 'Call a function with IndexError', 1)


if __name__ == "__main__":
	Tester.do_and_show_used_time(test_tester_do_and_show_used_time, 'test_Tester.do_and_show_used_time')
