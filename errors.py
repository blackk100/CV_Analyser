# coding=utf-8
"""
:Name: errors.py
:Description: Custom Errors for the CV_Analyser. USed for debugging until all manual testing is finished.
Contains Python2 compatible syntax to prevent further errors when called from main.py
:Author: blackk100
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

	def __init__(self):
		self.message = "Meun option out of range error!"
		super(MenuOptionOutOfRangeError, self).__init__(self.message)


class AttemptingProcessingButNoImageReadError(Exception):
	"""
	Raised when the user attempts to run any image processing functions without reading an image first
	"""

	def __init__(self):
		self.message = "No image read error!"
		super(AttemptingProcessingButNoImageReadError, self).__init__(self.message)


class IncorrectProgramExitResponseError(Exception):
	"""
	Raised when the user enters an incorrect response to the program exit prompt
	"""

	def __init__(self):
		self.message = "Incorrect response error (program exit prompt)!"
		super(IncorrectProgramExitResponseError, self).__init__(self.message)


class IncorrectImageSaveConfResponseError(Exception):
	"""
	Raised when the user enters an incorrect response to the image save confirmation prompt
	"""

	def __init__(self):
		self.message = "Incorrect response error (image save confirmation prompt)!"
		super(IncorrectImageSaveConfResponseError, self).__init__(self.message)


class NoImageInBufferError(Exception):
	"""
	Raised when attempting to save an image when there isn't any present in the image variables
	"""

	def __init__(self):
		self.message = "No image in buffer error (image save attempt)!"
		super(NoImageInBufferError, self).__init__(self.message)


class IncorrectImageSaveRetryResponseError(Exception):
	"""
	Raised when the user enters an incorrect response to the image save retry prompt
	"""

	def __init__(self):
		self.message = "Incorrect response error (image save retry prompt)!"
		super(IncorrectImageSaveRetryResponseError, self).__init__(self.message)


class IncorrectImagePreviewResponseError(Exception):
	"""
	Raised when the user enters an incorrect response to the image preview prompt
	"""
	
	def __init__(self):
		self.message = "Incorrect response error (image preview prompt)!"
		super(IncorrectImagePreviewResponseError, self).__init__(self.message)


class DenoiseQualityOutOfRangeError(Exception):
	"""
	Raised when the user enters a quality setting out of the range of selectable qualities
	"""
	
	def __init__(self):
		self.message = "De-noising quality out of range error!"
		super(DenoiseQualityOutOfRangeError, self).__init__(self.message)


class IncorrectDenoiseRetryResponseError(Exception):
	"""
	Raised when the user enters an incorrect response to the image de-noising retry prompt
	"""
	
	def __init__(self):
		self.message = "Incorrect response error (image de-noising retry prompt)!"
		super(IncorrectDenoiseRetryResponseError, self).__init__(self.message)


class GradientTypeOutOfRangeError(Exception):
	"""
	Raised when the user enters a image gradient type out of the range of selectable types
	"""
	
	def __init__(self):
		self.message = "Image gradient type out of range error!"
		super(GradientTypeOutOfRangeError, self).__init__(self.message)


class IncorrectGradientRetryResponseError(Exception):
	"""
	Raised when the user enters an incorrect response to the image gradient retry prompt
	"""
	
	def __init__(self):
		self.message = "Incorrect response error (image gradient retry prompt)!"
		super(IncorrectGradientRetryResponseError, self).__init__(self.message)


class EdgeLowerThresholdOutOfRangeError(Exception):
	"""
	Raised when the user enters a lower threshold for edge detection which is out of range
	"""
	
	def __init__(self):
		self.message = "Edge detection lower threshold out of range error!"
		super(EdgeLowerThresholdOutOfRangeError, self).__init__(self.message)


class IncorrectEdgeLowerThresholdRetryResponseError(Exception):
	"""
	Raised when the user enters an incorrect response to the edge detection lower threshold retry prompt
	"""
	
	def __init__(self):
		self.message = "Incorrect response error (edge detection - lower threshold retry prompt)!"
		super(IncorrectEdgeLowerThresholdRetryResponseError, self).__init__(self.message)


class EdgeUpperThresholdOutOfRangeError(Exception):
	"""
	Raised when the user enters an upper threshold for edge detection which is out of range
	"""
	
	def __init__(self):
		self.message = "Edge detection upper threshold out of range error!"
		super(EdgeUpperThresholdOutOfRangeError, self).__init__(self.message)


class IncorrectEdgeUpperThresholdRetryResponseError(Exception):
	"""
	Raised when the user enters an incorrect response to the edge detection upper threshold retry prompt
	"""
	
	def __init__(self):
		self.message = "Incorrect response error (edge detection - upper threshold retry prompt)!"
		super(IncorrectEdgeUpperThresholdRetryResponseError, self).__init__(self.message)
