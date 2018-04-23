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
	else:
		h, h_color = 15, 15
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
	dst, dst_code = None, None
	if mode == 0:  # BGR to Gray-scale
		t_img = cv2.cvtColor(t_img, cv2.COLOR_BGR2GRAY, dst, dst_code)
	elif mode == 1:  # BGR to HSV
		t_img = cv2.cvtColor(t_img, cv2.COLOR_BGR2HSV, dst, dst_code)
	elif mode == -1:  # HSV to BGR
		t_img = cv2.cvtColor(t_img, cv2.COLOR_HSV2BGR, dst, dst_code)
	elif mode == 2:  # HSV to Gray-scale
		t_img = change_color(t_img, -1)
		t_img = change_color(t_img)
	return t_img
