# coding=utf-8
"""
:Name: errors.py
:Description: Custom Errors for the CV_Analyser. USed for debugging until all manual testing is finished.
Contains Python2 compatible syntax to prevent further errors when called from main.py
:Author: blackk100 - https://blackk100.github.io/
:Version: Pre-Alpha
:Dependencies: None
"""


class IncompatibleVersionError(Exception):
	"""
	Raised when the Python Interpreter version < 3.x
	"""
	def __init__(self):
		self.message = "Incompatible Python interpreter version error!"
		super(IncompatibleVersionError, self).__init__(self.message)


class FileDoesNotExistError(FileNotFoundError):
	"""
	Raised when the path entered by the user doesn't point to a file
	"""
	def __init__(self):
		self.message = "File existence check error!"
		super(FileDoesNotExistError, self).__init__(self.message)


class FileIncorrectFormatError(Exception):
	"""
	Raised when the path entered by the user doesn't point to a compatible image file
	"""
	def __init__(self):
		self.message = "Unsupported image format error!"
		super(FileIncorrectFormatError, self).__init__(self.message)


class MenuOptionOutOfRangeError(Exception):
	"""
	Raised when the user enters an option outside the range of selectable options
	"""
	def __int__(self):
		self.message = "Meun option out of range error!"
		super(MenuOptionOutOfRangeError, self).__init__(self.message)


class IncorrectProgramExitResponseError(Exception):
	"""
	Raised when the user enters an incorrect response to the program exit prompt
	"""
	def __int__ (self):
		self.message = "Incorrect response error (program exit prompt)!"
		super(IncorrectProgramExitResponseError, self).__init__(self.message)


class IncorrectImageSaveConfResponseError(Exception):
	"""
	Raised when the user enters an incorrect response to the image save confirmation prompt
	"""
	def __int__ (self):
		self.message = "Incorrect response error (image save confirmation prompt)!"
		super(IncorrectImageSaveConfResponseError, self).__init__(self.message)


class IncorrectImageSaveRetryResponseError(Exception):
	"""
	Raised when the user enters an incorrect response to the image save retry prompt
	"""
	def __int__ (self):
		self.message = "Incorrect response error (image save retry prompt)!"
		super(IncorrectImageSaveRetryResponseError, self).__init__(self.message)
