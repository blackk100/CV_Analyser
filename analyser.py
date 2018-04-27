# coding=utf-8
"""
:Name: analyser.py
:Description: Core analyser script for processing images by using OpenCV
:Author: blackk100 - https://blackk100.github.io/
:Version: Pre-Alpha
:Dependencies: NumPy and OpenCV
"""

import numpy               # NumPy
import cv2                 # OpenCV
import errors              # Custom Errors
from pathlib import Path   # For resolving paths
from pprint import pprint  # For pretty printing lists


def read_img() -> (numpy.uint8, numpy.uint8, str):
	"""
	Reads an image and returns an array of color and gray-scale images

	:return: NumPy uint8 arrays (OpenCV Image Representations) & file name
	:rtype: (numpy.uint8, numpy.uint8, str)
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
	pprint(formats)
	while True:
		try:
			path = input()
			file = Path(path).resolve()
			if file.is_file():
				name, extn = file.name.split(".")
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
		except FileNotFoundError:
			print("ERROR: Path resolution error!")
		finally:
			print("\nEnter absolute/relative path to the image to be read (including the filename with extension)")


def save_img(image, o_name) -> bool:
	"""
	Used for saving an image.

	:param image: NumPy uint8 array (OpenCV Image Representation)
	:type image: numpy.uint8

	:param o_name: Original Name of the Image
	:type o_name: str

	:return: Returns True if the function executes completely, else False
	:rtype: bool
	"""

	try:
		print("Enter the name of the output image file.",)
		print("Do not enter an image format extension, the output format is locked to .jpeg)")
		n_name = input()
		name = o_name + n_name + ".jpeg"
		print("Entered modification: " + n_name)
		print("Actual name of the file: " + name)
		conf_f = True
		while conf_f:
			try:
				print("Are you sure? (Y/N): ")
				conf = input().capitalize()
				if conf == "Y":
					conf_f = False
				elif conf == "N":
					break
				else:
					raise errors.IncorrectImageSaveConfResponseError
			except errors.IncorrectProgramExitResponseError as e:
				print("ERROR: " + e.message)
			finally:
				print("Valid options are: 'Y', 'y', 'N' and 'n' only.")
		path = Path.cwd() / "output" / o_name / name
		path.resolve()
		cv2.imwrite(filename = str(path), img = image, params = (cv2.IMWRITE_JPEG_QUALITY, 100))
		return True
	except FileNotFoundError:
		print("ERROR: Path resolution error!")
		return False


def de_noise(color, gray, quality=0) -> (numpy.uint8, numpy.uint8):
	"""
	Removes noise from the input image

	NOTE: Other functions (getting image gradients, edge detection, etc.) de-noise the image on their own

	:param color: NumPy uint8 array (OpenCV Image Representation) (8-bit color image)
	:type color: numpy.uint8

	:param gray: NumPy uint8 array (OpenCV Image Representation) (8-bit gray-scale image)
	:type gray: numpy.uint8

	:param quality: De-noising quality (default = 0)

		* -1 -- low (Moderate Noise, High End Image Detail, Very Low Colored Image Distortion)
		* 0  -- moderate (Low Noise, Moderate-High End Image Detail, Low Colored Image Distortion)
		* 1  -- high (Very Low Noise, Moderate-Low End Image Detail, Moderate Colored Image Distortion)
	:type quality: int

	:return: NumPy uint8 arrays (OpenCV Image Representations)
	:rtype: (numpy.uint8, numpy.uint8)
	"""
	if quality == -1:
		h, h_color = 5, 5
	elif quality == 0:
		h, h_color = 10, 10
	elif quality == 1:
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
	return color_o, gray_o


def get_gradient(color, gray, mode=0) -> (numpy.uint8, numpy.uint8):
	"""
	Returns an image with it's gradient highlighted

	NOTE: Other functions (edge detection, etc.) get the image gradient on their own

	:param color: NumPy uint8 array (OpenCV Image Representation) (8-bit color image)
	:type color: numpy.uint8

	:param gray: NumPy uint8 array (OpenCV Image Representation) (8-bit gray-scale image)
	:type gray: numpy.uint8

	:param mode: Image gradient calculation mode (default = 0)

		* -1 -- Scharr Derivative (Y-Axis)
		* 0  -- Laplacian Derivatives
		* 1  -- Scharr Derivative (X-Axis)
	:type mode: int

	:return: NumPy uint8 arrays (OpenCV Image Representations)
	:rtype: (numpy.uint8, numpy.uint8)
	"""
	
	def scharr(img, x, y) -> numpy.uint8:
		"""
		Black-to-White transitions have a positive value, while White-to-Black transitions have a negative value.
		
		Hence, when data is converted to numpy.uint8 (or cv2.CV_8U), all negative slopes become zero, i.e.,
		that edge is missed.
	
		To fix this issue, the output data-type is sent to a higher range type, i.e., numpy.float64 (or cv2.CV_64F),
		Its absolute value is then taken, and subsequently converted back to numpy.uint8

		:param img: numpy.uint8 array (OpenCV Image Representation)
		:type img: numpy.uint8

		:param x: Order of x-derivative
		:type x: int

		:param y: Order of y-derivative
		:type y: int

		:return: numpy.uint8 array (OpenCV Image Representation)
		:rtype: numpy.uint8
		"""
		img_o = cv2.Scharr(src = img, ddepth = cv2.CV_64F, dx = x, dy = y)
		img_o = numpy.absolute(img_o)
		img_o = numpy.uint8(img_o)
		return img_o

	if mode == 1:
		dx, dy = 1, 0
	elif mode == -1:
		dx, dy = 0, 1
	else:
		dx, dy = 0, 0
	if mode == 0:
		color_o = cv2.Laplacian(src = color, ddepth = cv2.CV_64F, ksize = -1)
		gray_o = cv2.Laplacian(src = gray, ddepth = cv2.CV_64F, ksize = -1)
	elif abs(mode) == 1:
		color_o = scharr(img = color, x = dx, y = dy)
		gray_o = scharr(img = gray, x = dx, y = dy)
	else:
		color_o, gray_o = color, gray
	return color_o, gray_o


def detect_edge(color, gray, threshold_1=100, threshold_2=250) -> (numpy.uint8, numpy.uint8):
	"""
	Returns a binary image of the input image with the edges highlighted using the Canny Edge Detection Algorithm

	:param color: NumPy uint8 array (OpenCV Image Representation) (8-bit color image)
	:type color: numpy.uint8

	:param gray: NumPy uint8 array (OpenCV Image Representation) (8-bit gray-scale image)
	:type gray: numpy.uint8

	:param threshold_1: 1st threshold for the hysteresis procedure (default = 100)
	:type threshold_1: int

	:param threshold_2: 2nd threshold for the hysteresis procedure (default = 250)
	:type threshold_2: int

	:return: NumPy uint8 arrays (OpenCV Image Representations)
	:rtype: (numpy.uint8, numpy.uint8)
	"""
	color_o = cv2.Canny(image = color, threshold1 = threshold_1, threshold2 = threshold_2, L2gradient = True)
	gray_o = cv2.Canny(image = gray, threshold1 = threshold_1, threshold2 = threshold_2, L2gradient = True)
	return color_o, gray_o


def histogram_gen(color, gray) -> (numpy.uint8, numpy.uint8):
	"""
	Returns histograms depicting the frequency of the occurrence of a given color

	:param color: NumPy uint8 array (OpenCV Image Representation) (8-bit color image)
	:type color: numpy.uint8

	:param gray: NumPy uint8 array (OpenCV Image Representation) (8-bit gray-scale image)
	:type gray: numpy.uint8

	:return: NumPy uint8 arrays (OpenCV Image Representations)
	:rtype: (numpy.uint8, numpy.uint8)
	"""

	color_channels = cv2.split(m = color)
	color_channels_hist = []
	for i in range(color_channels):
		color_channels_hist.append(
				cv2.calcHist(
					images = [color_channels[i]],
					channels = [i],
					mask = None,
					histSize = 256,
					ranges = [0, 256]
				)
		)
	color_hist = cv2.merge(mv = color_channels_hist)

	gray_hist = cv2.calcHist(images = gray, channels = [0], mask = None, histSize = [256], ranges = [0, 256])

	return color_hist, gray_hist
