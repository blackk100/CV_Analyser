# coding=utf-8
"""
:Name: analyser.py
:Description: Python Script for analysing interference patterns by using OpenCV
:Author: blackk100 (blackk100.github.io)
:External Dependencies: NumPy and OpenCV (see 'Pipfile' for packages)
:Made with: PyCharm Community and pipenv
"""

import numpy  # NumPy
import cv2    # OpenCV


def read() -> (numpy.uint8, str):
	"""
	Reads and returns an image (includes user interactions)

	:return: NumPy uint8 array (OpenCV Image Representation) & file name
	:rtype: (numpy.uint8, str)
	"""
	from pathlib import Path
	while True:
		print("Enter relative path to the image to be read (including the filename with extension):")
		path = input()
		file = Path(path)
		if file.is_file():
			break
		else:
			print("ERROR: Incorrect file-path!!\n")
			continue
	while True:
		print("Enter the image read mode:")
		print("\t0 -- Gray-scale")
		print("\t1 -- Color")
		try:
			mode = int(input())
			if mode in [0, 1]:
				if mode == 0:
					mode = cv2.IMREAD_GRAYSCALE
				elif mode == 1:
					mode = cv2.IMREAD_COLOR
				else:
					mode = cv2.IMREAD_UNCHANGED
				break
			else:
				raise ValueError
		except ValueError:
			print("ERROR: Value out of range!!\n")
			continue
	image = cv2.imread(path, mode)
	return image, file.name


def save(image, o_name, color=-2, denoise=-2, gradient=-2, edge=False, histogram=-1) -> None:
	"""
	Used for saving an image with modified names.

	:param image: NumPy uint8 array (OpenCV Image Representation)
	:type image: numpy.uint8

	:param o_name: Original Name of the Image
	:type o_name: str

	:param color: Color change modifier

		* -1 -- HSV to BGR
		* 0  -- BGR to Gray-scale
		* 1  -- BGR to HSV
		* 2  -- HSV to Gray-scale
	:type color: int

	:param denoise: De-noising modifier

		* -11 -- Low Reduction   ; Color Image
		* 10  -- Moderate Reduction; Color Image
		* 11  -- High Reduction  ; Color Image
		* -1  -- Low Reduction   ; Gray-scale Image
		* 0   -- Moderate Reduction; Gray-scale Image
		* 1   -- High Reduction  ; Gray-scale Image
	:type denoise: int

	:param gradient: Gradient modifier

		* -1 -- Scharr Derivative (Y-Axis)
		* 0  -- Laplacian Derivative
		* 1  -- Scharr Derivative (X-Axis)
	:type gradient: int

	:param edge: Edge detection flag
	:type edge: int

	:param histogram: Histogram generated modifier

	:type histogram: int

	:return: None
	:rtype: None
	"""
	name = o_name
	if color != -2:
		if color == -1:
			name += "_HSV-BGR"
		elif color == 0:
			name += "_BGR-Gray"
		elif color == 1:
			name += "_BGR-HSV"
		elif color == 2:
			name += "_HSV-Gray"
	if denoise != -2:
		if denoise == -11:
			name += "_low-color"
		elif denoise == 10:
			name += "_moderate-color"
		elif denoise == 11:
			name += "_high-color"
		elif denoise == -1:
			name += "_low-gray"
		elif denoise == 0:
			name += "_moderate-gray"
		elif denoise == 1:
			name += "_high-gray"
	if gradient != -2:
		if gradient == -1:
			name += "_scharr-y"
		elif gradient == 0:
			name += "_laplacian"
		elif gradient == 1:
			name += "_scharr-x"
	if edge is True:
		name += "_edges"
	if histogram != -1:
		if histogram == 0:
			name += "_histogram-curves"
		elif histogram == 1:
			name += "_histogram-lines"
	name += ".jpeg"
	cv2.imwrite(name, image, (cv2.IMWRITE_JPEG_QUALITY, 100))


def change_color(image, mode = 0) -> numpy.uint8:
	"""
	Changes the image color-space

	NOTE: This function isn't used widely within the analyser,
			however it may be used in the future when expanding the analyser

	:param image: NumPy uint8 array (OpenCV Image Representation)
	:type image: numpy.uint8

	:param mode: Image color conversion mode (default = 0)

		* -1 -- HSV to BGR
		* 0  -- BGR to Gray-scale
		* 1  -- BGR to HSV
		* 2  -- HSV to Gray-scale
	:type mode: int

	:return: NumPy uint8 array (OpenCV Image Representation)
	:rtype: numpy.uint8
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


def de_noise(image, mode=1, quality=0) -> numpy.uint8:
	"""
	Removes noise from the input image

	NOTE: Other functions (image gradients, edge detections, etc.) de-noise the image on their own

	:param image: NumPy uint8 array (OpenCV Image Representation)
	:type image: numpy.uint8

	:param mode: Image color mode (default = 1).

		* 0 -- Gray-scale Image
		* 1 -- Colored Image
	:type mode: int

	:param quality: De-noising quality (default = 0)

		* -1 -- low (Moderate Noise, High End Image Detail, Very Low Colored Image Distortion)
		* 0  -- moderate (Low Noise, Moderate End Image Detail, Low Colored Image Distortion)
		* 1  -- high (Very Low Noise, Low End Image Detail, Moderate Colored Image Distortion)
	:type quality: int

	:return: NumPy uint8 array (OpenCV Image Representation)
	:rtype: numpy.uint8
	"""
	t_img = image
	dst = None
	template_window_size = 7
	search_window_size = 21
	if quality == -1:
		h = 5
		h_color = 5
	elif quality == 0:
		h = 10
		h_color = 10
	elif quality == 1:
		h = 15
		h_color = 15
	else:
		h = 0
		h_color = 0
	if mode == 1:
		cv2.fastNlMeansDenoisingColored(t_img, dst, h, h_color, template_window_size, search_window_size)
	else:
		cv2.fastNlMeansDenoising(t_img, dst, h, template_window_size, search_window_size)
	return t_img


def get_gradient(image, mode=0) -> numpy.uint8:
	"""
	Returns an image with it's gradient highlighted
	
	NOTE: This function isn't used widely within the analyser,
			however it may be used in the future when expanding the analyser

	:param image: NumPy uint8 array (OpenCV Image Representation)
	:type image: numpy.uint8

	:param mode: Image gradient calculation mode (default = 0)

		* -1 -- Scharr Derivative (Y-Axis)
		* 0  -- Laplacian Derivatives
		* 1  -- Scharr Derivative (X-Axis)
	:type mode: int

	:return: NumPy uint8 array (OpenCV Image Representation)
	:rtype: numpy.uint8
	"""
	t_img = image
	d_depth = cv2.CV_64F
	k_size = -1
	if mode == 1:
		dx = 1
		dy = 0
	elif mode == -1:
		dx = 0
		dy = 1
	else:
		dx = 0
		dy = 0
	if mode == 0:
		t_img = cv2.Laplacian(t_img, d_depth, ksize = k_size)
	elif abs(mode) == 1:
		t_img = cv2.Scharr(t_img, d_depth, dx, dy)
		t_img = numpy.absolute(t_img)
		t_img = numpy.uint8(t_img)
		"""
		Black-to-White transitions have a positive value, while White-to-Black transitions have a negative value.
		
		Hence, when data is converted to numpy.uint8 (or cv2.CV_8U), all negative slopes become zero, i.e.,
		that edge is missed.
	
		To fix this issue, the output data-type is sent to a higher range type, i.e., numpy.float64 (or cv2.CV_64F),
		it's absolute value is taken, and then it is converted back to numpy.uint8
		"""
	return t_img


def detect_edge(image, threshold_1=100, threshold_2=250) -> numpy.uint8:
	"""
	Returns a binary image of the input image with the edges highlighted using the Canny Edge Detection Algorithm

	:param image: NumPy uint8 array (OpenCV Image Representation)
	:type image: numpy.uint8

	:param threshold_1: 1st threshold for the hysteresis procedure (default = 100)
	:type threshold_1: int

	:param threshold_2: 2nd threshold for the hysteresis procedure (default = 250)
	:type threshold_2: int

	:return: NumPy uint8 array (OpenCV Image Representation)
	:rtype: numpy.uint8
	"""
	t_img = image
	gradient_mode = True
	t_img = cv2.Canny(t_img, threshold_1, threshold_2, L2gradient = gradient_mode)
	return t_img


def histogram_gen(image, mode=0):
	"""
	Returns a histogram (as curves or as lines (binary image))
	
	Based off https://github.com/opencv/opencv/blob/master/samples/python/hist.py

	:param image: NumPy uint8 array (OpenCV Image Representation)
	:type image: numpy.uint8

	:param mode: Histogram generation mode

		* 0 -- Curves
		* 1 -- Lines
	:type mode: int

	:return: NumPy uint8 array (OpenCV Image Representation)
	:rtype: numpy.uint8
	"""
	t_img = image
	bins = numpy.arange(256).reshape(256, 1)
	histogram = numpy.zeros((300, 256, 3))
	mask = None
	hist_size = [256]
	ranges = [0, 256]
	alpha = 0
	beta = 255
	norm_type = cv2.NORM_MINMAX
	color = [(255, 255, 255)]
	if mode == 0:
		if t_img.shape[2] == 3:
			color = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
		else:
			color = [(0, 0, 0)]
		is_closed = False
		for channel, colour in enumerate(color):
			hist_item = cv2.calcHist([t_img], [channel], mask, hist_size, ranges)
			cv2.normalize(hist_item, hist_item, alpha, beta, norm_type)
			hist = numpy.int32(numpy.around(hist_item))
			pts = numpy.int32(numpy.column_stack((bins, hist)))
			cv2.polylines(histogram, [pts], is_closed, colour)
	elif mode == 1:
		if len(t_img.shape) != 2:
			t_img = change_color(t_img)
		channel = 0
		hist_item = cv2.calcHist([t_img], [channel], mask, hist_size, ranges)
		cv2.normalize(hist_item, hist_item, alpha, beta, norm_type)
		hist = numpy.int32(numpy.around(hist_item))
		for x, y in enumerate(hist):
			pt1 = (x, 0)
			pt2 = (x, y)
			cv2.line(histogram, pt1, pt2, color[0])
	return numpy.flipud(histogram)
