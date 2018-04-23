# coding=utf-8
"""
Name: analyser.py
Description: Python Script for analysing interference patterns by using OpenCV
Author: blackk100 (blackk100.github.io)
External Dependencies: NumPy and OpenCV (see 'Pipfile' for packages)
Made with: PyCharm Community and pipenv
"""
import numpy
import cv2


def read() -> int:
	"""
	Reads and returns an image (includes user interactions)

	:return: NumPy int8 array (OpenCV Image Representation)
	:rtype: int
	"""
	from pathlib import Path  # Used for checking if the file exists
	while True:
		print("Enter relative path to the image to be read (including the filename with extension):")
		path = input()
		file = Path(path)
		if file.is_file():
			break
		else:
			print("ERROR: Incorrect file-path!!")
			continue
	while True:
		print("Enter the image read mode:")
		print("\t0 - Colored image")
		print("\t1 - Black and White image")
		mode = int(input())
		if mode in [0, 1]:
			mode = cv2.IMREAD_COLOR if 0 else cv2.IMREAD_GRAYSCALE
			break
		else:
			print("ERROR: Value out of range!!")
			continue
	image = cv2.imread(path, mode)
	return image


def denoise(image, mode=1, quality=0) -> int:
	"""
	Removes noise from the input image

	:param image: NumPy int8 array (OpenCV Image Representation)
	:type image: int

	:param mode: Image color mode (default = 1).

		* 1 -- Colored Image
		* 0 -- Gray-scale Image
	:type mode: int

	:param quality: De-noising quality (default = 0)

		* -1 -- low (Moderate Noise, High End Image Detail, Very Low Colored Image Distortion)
		* 0  -- medium (Low Noise, Moderate End Image Detail, Low Colored Image Distortion)
		* 1  -- high (Very Low Noise, Low End Image Detail, Moderate Colored Image Distortion)
	:type quality: int

	:return: NumPy int8 array (OpenCV Image Representation)
	:rtype: int
	"""
	t_img = image
	dst, template_window_size, search_window_size = None, 7, 21
	if quality == -1:
		h, h_color = 5, 5
	elif quality == 0:
		h, h_color = 10, 10
	elif quality == 1:
		h, h_color = 15, 15
	else:
		h, h_color = 0, 0
	if mode == 1:
		cv2.fastNlMeansDenoisingColored(t_img, dst, h, h_color, template_window_size, search_window_size)
	else:
		cv2.fastNlMeansDenoising(t_img, dst, h, template_window_size, search_window_size)
	return t_img


def change_color(image, mode=0) -> int:
	"""
	Changes the image color-space

	:param image: NumPy int8 array (OpenCV Image Representation)
	:type image: int

	:param mode: Image color conversion mode

		* -1 -- HSV to BGR
		* 0  -- BGR to Gray-scale
		* 1  -- BGR to HSV
		* 2  -- HSV to Gray-scale
	:type mode: int

	:return: NumPy int8 array (OpenCV Image Representation)
	:rtype: int
	"""
	t_img = image
	if mode == 0:
		t_img = cv2.cvtColor(t_img, cv2.COLOR_BGR2GRAY)
	elif mode == 1:
		t_img = cv2.cvtColor(t_img, cv2.COLOR_BGR2HSV)
	elif mode == -1:
		t_img = cv2.cvtColor(t_img, cv2.COLOR_HSV2BGR)
	elif mode == 2:
		t_img = change_color(t_img, -1)
		t_img = change_color(t_img)
	return t_img


def gradient(image, mode=0) -> int:
	"""
	Returns an image with it's gradient highlighted

	:param image: NumPy int8 array (OpenCV Image Representation)
	:type image: int

	:param mode: Image gradient calculation mode

		* -1 -- Scharr Derivative (Y-Axis)
		* 0  -- Laplacian Derivatives
		* 1  -- Scharr Derivative (X-Axis)
	:type mode: int

	:return: NumPy int8 array (OpenCV Image Representation)
	:rtype: int
	"""
	t_img = image
	d_depth = cv2.CV_64F
	dst = None
	k_size = -1
	if mode == 1:
		dx, dy = 1, 0
	elif mode == -1:
		dx, dy = 0, 1
	else:
		dx, dy = 0, 0
	if mode == 0:
		t_img = cv2.Laplacian(t_img, d_depth, dst, k_size)
	elif abs(mode) == 1:
		t_img = numpy.uint8(numpy.absolute(cv2.Scharr(t_img, d_depth, dx, dy)))
		"""
		Black-to-White transitions have a positive value, while White-to-Black transitions have a negative value.
		
		Hence, when data is converted to numpy.uint8 (or cv2.CV_8U), all negative slopes are made zero, i.e.,
		that edge is missed.
		
		To fix this issue, the output data-type is sent to a higher range type, i.e., numpy.float64 (or cv2.CV_64F),
		it's absolute value is taken, and then it is converted back to numpy.uint8
		"""
	return t_img


def edge(image, threshold_1, threshold_2) -> int:
	"""
	Returns a binary image of the input image with the edges highlighted using the Canny Edge Detection Algorithm

	:param image: NumPy int8 array (OpenCV Image Representation)
	:type image: int

	:param threshold_1: First threshold for the hysteresis procedure
	:type threshold_1: int

	:param threshold_2: Second threshold for the hysteresis procedure
	:type threshold_2: int

	:return: NumPy int8 array (OpenCV Image Representation)
	:rtype: int
	"""
	return cv2.Canny(image, threshold_1, threshold_2, L2gradient = True)
