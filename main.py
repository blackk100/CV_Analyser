# coding=utf-8
"""
:Name: main.py
:Description: Run file. Checks for the correct interpreter version and gracefully exits when encountering an error
:Author: blackk100 - https://blackk100.github.io
:Version: Pre-Alpha
:Dependencies: See 'Pipfile' for project-wide dependencies
"""

from sys import version_info as vi  # Python Interpreter Version
from time import sleep              # Slowing down execution


def version_check(version) -> int:
	"""
	Checks the current python interpreter version

	:param version:
	:type version:
	:return: An integer depending on the interpreter version
	:rtype: int
	"""
	print("Current Python interpreter version: " + version[0] + "." + version[1] + "." + version[2])
	if version[0] >= 3:
		if (version[0] == 3) and (version[1] == 6) and (version[2] == 5):
			return 1
		return 0
	else:
		return -1


if __name__ == "__main__":
	try:
		import errors
		import interface
	
		check_result = version_check(vi)
		if check_result > -1:
			if check_result == 0:
				print("\n CV_Analyser has only been tested on Python 3.6.5 by the author.")
				print(
					"The author takes no responsibility for any errors occurring due to usage of an untested "
					"interpreter."
				)
			interface.main()
		else:
			raise errors.IncompatibleVersionError
	except ImportError:
		errors, interface = None, None
		print("Unable to import the required components.")
		print("Verify all dependencies are accessible from the current interpreter.")
		print("Verify all CV_Analyser files are present in the current working directory.")
	except errors.IncompatibleVersionError as e:
		print("ERROR: " + e.message)
		print("\n CV_Analyser requires Python 3.0 or greater.")
	except Exception as e:  # For catching errors that occur during actual program execution
		print("UNKNOWN ERROR OCCURRED!!")
		print("ERROR TRACEBACK: " + str(e))
else:
	print("CV_Analyser must be run independently!")
	
print("\nCV_Analyser will auto-exit in 1 minute.")
sleep(90)  # Actually takes 1.5 minutes
print("\nBye!")
sleep(1)
