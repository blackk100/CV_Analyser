# coding=utf-8
"""
:Name: analyser.py
:Description: Core analyser script for processing images by using OpenCV
:Author: blackk100
:Version: Pre-Alpha
:Dependencies: NumPy and OpenCV
"""

import numpy               # NumPy
import cv2                 # OpenCV
import errors              # Custom Errors
from pathlib import Path   # For resolving paths


def pprint(strings) -> None:
	"""
	Pretty prints string arrays

	:param strings: An array of strings
	:type strings: list[str]

	:return: None
	:rtype: None
	"""

	for i in range(len(strings)):
		print(strings[i])


def read_img() -> (numpy.ndarray, numpy.ndarray, str):
	"""
	Reads an image and returns an array of color and gray-scale images

	:return: NumPy ndarray arrays (OpenCV Image Representations) & file name
	:rtype: (numpy.ndarray, numpy.ndarray, str)
	"""

	formats = [
		".bmp",
		".dib",
		".jpeg",
		".jpg",
		".jpe",
		".jp2",
		".png",
		".webp",
		".pbm",
		".pgm",
		".ppm",
		".sr",
		".ras",
		".tiff",
		".tif"
	]
	print("Enter absolute/relative path to the image to be read (including the filename with extension)")
	print("Supported image formats:")
	pprint(strings = formats)
	while True:
		try:
			path = input()
			file = Path(path).resolve()
			if file.is_file():
				extn = file.suffix.lower()
				name = file.name.lower().replace(extn, "")
				if extn in formats:
					color = cv2.imread(filename = path, flags = cv2.IMREAD_COLOR)
					gray = cv2.imread(filename = path, flags = cv2.IMREAD_GRAYSCALE)
					return color, gray, name
				else:
					raise errors.FileIncorrectFormatError
			else:
				raise errors.FileDoesNotExistError
		except (errors.FileDoesNotExistError, errors.FileIncorrectFormatError) as e:
			print("ERROR: " + e.message)
			print("\nEnter absolute/relative path to the image to be read (including the filename with extension)")
		except FileNotFoundError:
			print("ERROR: Path resolution error!")
			print("\nEnter absolute/relative path to the image to be read (including the filename with extension)")


def save_img(image, o_name) -> bool:
	"""
	Used for saving an image.

	:param image: NumPy ndarray array (OpenCV Image Representation)
	:type image: numpy.ndarray

	:param o_name: Original Name of the Image
	:type o_name: str

	:return: Returns True if the function executes completely, else False
	:rtype: bool
	"""

	try:
		path = Path.cwd()
		save_dir = ["output", o_name]
		for i in save_dir:
			path = path.joinpath(i)
			path.mkdir(exist_ok = True)
		print("Enter the name of the output image file.",)
		print("Do not enter an image format extension, the output format is locked to .jpeg)")
		print("\nFile will be saved at: " + str(path) + "\n")
		n_name = input()
		n_name += ".a"
		n_name = n_name.split(".")[0]
		name = n_name + ".jpeg"
		print("Name of the file: " + name)
		conf_f = True
		while conf_f:
			try:
				print("Are you sure? (Y/N): ")
				conf = input().capitalize()
				if conf == "Y":
					conf_f = False
				elif conf == "N":
					return save_img(image = image, o_name = o_name)
				else:
					raise errors.IncorrectImageSaveConfResponseError
			except errors.IncorrectImageSaveConfResponseError as e:
				print("ERROR: " + e.message)
				print("Valid options are: 'Y', 'y', 'N' and 'n' only.")
		cv2.imwrite(filename = str(path.joinpath(name)), img = image, params = (cv2.IMWRITE_JPEG_QUALITY, 100))
		return True
	except FileNotFoundError:
		print("ERROR: Path resolution error!")
		return False


def color_space_converter(image, color=False) -> numpy.ndarray:
	"""
	Used for converting to the correct output color-space after processing an image.

	:param image: numpy.ndarray array ()OpenCV Image Representation) (8-bit color or gray-scale image)
	:type image:

	:param color: Used to specify if the output need to be a 8-bit color or gray-scale image (default = False)
	:type color: bool

	:return: numpy.ndarray array (OpenCV Image Representation) (8-bit color or gray-scale image)
	:rtype: numpy.ndarray
	"""

	if len(image.shape) == 2:  # Single channel
		if color:
			return cv2.cvtColor(src = image, code = cv2.COLOR_GRAY2BGR)
		else:
			return image
	elif len(image.shape) == 3:  # Multi-channel
		if color:
			return image
		else:
			return cv2.cvtColor(src = image, code = cv2.COLOR_BGR2GRAY)


def de_noise(color, gray, quality=0) -> (numpy.ndarray, numpy.ndarray):
	"""
	Removes noise from the input image

	NOTE: Other functions (getting image gradients, edge detection, etc.) de-noise the image on their own

	:param color: NumPy ndarray array (OpenCV Image Representation) (8-bit color image)
	:type color: numpy.ndarray

	:param gray: NumPy ndarray array (OpenCV Image Representation) (8-bit gray-scale image)
	:type gray: numpy.ndarray

	:param quality: De-noising quality (default = 0)

		* 0 -- low (Moderate Noise, High End Image Detail, Very Low Colored Image Distortion)
		* 1 -- moderate (Low Noise, Moderate-High End Image Detail, Low Colored Image Distortion)
		* 2 -- high (Very Low Noise, Moderate-Low End Image Detail, Moderate Colored Image Distortion)
	:type quality: int

	:return: NumPy ndarray arrays (OpenCV Image Representations)
	:rtype: (numpy.ndarray, numpy.ndarray)
	"""

	if quality == 0:
		h, h_color = 5, 5
	elif quality == 1:
		h, h_color = 10, 10
	elif quality == 2:
		h, h_color = 15, 15
	else:
		h, h_color = 0, 0
	color_o = cv2.fastNlMeansDenoisingColored(
			src = color,
			h = h,
			hColor = h_color,
			templateWindowSize = 7,
			searchWindowSize = 21
	)
	gray_o = cv2.fastNlMeansDenoising(
			src = gray,
			h = h,
			templateWindowSize = 7,
			searchWindowSize = 21
	)
	return color_space_converter(image = color_o, color = True), color_space_converter(image = gray_o)


def get_gradient(color, gray, mode=0) -> (numpy.ndarray, numpy.ndarray):
	"""
	Returns an image with it's gradient highlighted

	NOTE: Other functions (edge detection, etc.) get the image gradient on their own

	:param color: NumPy ndarray array (OpenCV Image Representation) (8-bit color image)
	:type color: numpy.ndarray

	:param gray: NumPy ndarray array (OpenCV Image Representation) (8-bit gray-scale image)
	:type gray: numpy.ndarray

	:param mode: Image gradient calculation mode (default = 0)

		* 0 -- Laplacian Derivatives
		* 1 -- Scharr Derivative (X-Axis)
		* 2 -- Scharr Derivative (Y-Axis)
	:type mode: int

	:return: NumPy ndarray arrays (OpenCV Image Representations)
	:rtype: (numpy.ndarray, numpy.ndarray)
	"""
	
	def scharr(img, x, y) -> numpy.ndarray:
		"""
		Black-to-White transitions have a positive value, while White-to-Black transitions have a negative value.
		
		Hence, when data is converted to numpy.ndarray (or cv2.CV_8U), all negative slopes become zero, i.e.,
		that edge is missed.
	
		To fix this issue, the output data-type is sent to a higher range type, i.e., numpy.float64 (or cv2.CV_64F),
		its absolute value is then taken, and subsequently converted back to numpy.ndarray

		:param img: numpy.ndarray array (OpenCV Image Representation)
		:type img: numpy.ndarray

		:param x: Order of x-derivative
		:type x: int

		:param y: Order of y-derivative
		:type y: int

		:return: numpy.ndarray array (OpenCV Image Representation)
		:rtype: numpy.ndarray
		"""
		img_o = cv2.Scharr(src = img, ddepth = cv2.CV_64F, dx = x, dy = y)
		img_o = numpy.absolute(img_o)
		img_o = numpy.uint8(img_o)
		return img_o

	def laplacian(img) -> numpy.ndarray:
		"""
		Black-to-White transitions have a positive value, while White-to-Black transitions have a negative value.
		
		Hence, when data is converted to numpy.ndarray (or cv2.CV_8U), all negative slopes become zero, i.e.,
		that edge is missed.
	
		To fix this issue, the output data-type is sent to a higher range type, i.e., numpy.float64 (or cv2.CV_64F),
		its absolute value is then taken, and subsequently converted back to numpy.ndarray

		:param img: numpy.ndarray array (OpenCV Image Representation)
		:type img: numpy.ndarray

		:return: numpy.ndarray array (OpenCV Image Representation)
		:rtype: numpy.ndarray
		"""
		img_o = cv2.Laplacian(src = img, ddepth = cv2.CV_64F, ksize = 1)
		img_o = numpy.absolute(img_o)
		img_o = numpy.uint8(img_o)
		return img_o

	dx, dy = 0, 0
	if mode == 1:
		dx += 1
	elif mode == 2:
		dy += 1
	if mode == 0:
		color_o = laplacian(img = color)
		gray_o = laplacian(img = gray)
	elif mode > 0:
		color_o = scharr(img = color, x = dx, y = dy)
		gray_o = scharr(img = gray, x = dx, y = dy)
	else:
		color_o, gray_o = color, gray
	return color_space_converter(image = color_o, color = True), color_space_converter(image = gray_o)


def detect_edge(color, gray, threshold_1=100, threshold_2=200) -> (numpy.ndarray, numpy.ndarray):
	"""
	Returns a binary image of the input image with the edges highlighted using the Canny Edge Detection Algorithm

	:param color: NumPy ndarray array (OpenCV Image Representation) (8-bit color image)
	:type color: numpy.ndarray

	:param gray: NumPy ndarray array (OpenCV Image Representation) (8-bit gray-scale image)
	:type gray: numpy.ndarray

	:param threshold_1: 1st threshold for the hysteresis procedure (default = 100)
	:type threshold_1: int

	:param threshold_2: 2nd threshold for the hysteresis procedure (default = 250)
	:type threshold_2: int

	:return: NumPy ndarray arrays (OpenCV Image Representations)
	:rtype: (numpy.ndarray, numpy.ndarray)
	"""

	color_o = cv2.Canny(image = color, threshold1 = threshold_1, threshold2 = threshold_2, L2gradient = True)
	gray_o = cv2.Canny(image = gray, threshold1 = threshold_1, threshold2 = threshold_2, L2gradient = True)
	return color_space_converter(image = color_o, color = True), color_space_converter(image = gray_o)


def histogram_gen(color, gray) -> (list, numpy.ndarray):
	"""
	Returns histograms depicting the frequency of the occurrence of a given color

	:param color: NumPy ndarray array (OpenCV Image Representation) (8-bit color image)
	:type color: numpy.ndarray

	:param gray: NumPy ndarray array (OpenCV Image Representation) (8-bit gray-scale image)
	:type gray: numpy.ndarray

	:return: NumPy ndarray arrays (OpenCV Image Representations)
	:rtype: (list, numpy.ndarray)
	"""

	color_channels = cv2.split(m = color)
	color_hist = []
	for i, color in enumerate(color_channels):
		color_hist.append(
				cv2.calcHist(
					images = color,
					channels = [i],
					mask = None,
					histSize = [256],
					ranges = [0, 256]
				)
		)

	gray_hist = cv2.calcHist(
			images = [gray],
			channels = [0],
			mask = None,
			histSize = [256],
			ranges = [0, 256]
	)

	return color_hist, gray_hist
