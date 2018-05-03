# coding=utf-8
"""
:Name: main.py
:Description: Run file. Checks for the correct interpreter version and gracefully exits when encountering an error
:Author: blackk100
:Version: Pre-Alpha
:Dependencies: See 'Pipfile' for project-wide dependencies
"""

from sys import version_info as vi  # Python Interpreter Version
from time import sleep              # Slowing down execution
import traceback                    # Error trace-backs


def version_check(version) -> int:
	"""
	Checks the current python interpreter version

	:param version: A tuple containing version information
	:type version: Tuple

	:return: An integer depending on the interpreter version
	:rtype: int
	"""
	print("Current Python interpreter version: " + str(version[0]) + "." + str(version[1]) + "." + str(version[2]))
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

		print("\n")
		check_result = version_check(vi)
		if check_result > -1:
			if check_result == 0:
				print("\nWARNING: CV_Analyser has only been tested on Python 3.6.5!")
			print("\n")
			print("Current Working Directory: ")
			interface.main()
		else:
			raise errors.IncompatibleVersionError
	except ImportError:
		print("\nUnable to import the required components.")
		print("Verify all dependencies are accessible from the current interpreter.")
		print("Verify all CV_Analyser files are present in the current working directory.\n")
	except errors.IncompatibleVersionError as e:
		print("\nERROR: " + e.message)
		print("CV_Analyser requires Python 3.0 or greater.\n")
	except KeyboardInterrupt:
		print("\nForce exit acknowledged.\n")
	except Exception as e:  # For catching errors that occur during actual program execution
		print("\nUNKNOWN ERROR OCCURRED!!")
		print("ERROR TRACEBACK: ")
		traceback.print_exc()
		print("\n")
else:
	print("CV_Analyser must be run independently!\n")
	
print("\nCV_Analyser will auto-exit in 30 seconds.")
sleep(30)
print("\nBye!")
sleep(1)
