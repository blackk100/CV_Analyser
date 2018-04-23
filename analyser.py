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
log, err = [], ""


def read():
	""" Reads and returns an image (includes user interactions) """
	log.append("read() Started")
	from pathlib import Path  # Used for checking if the file exists
	global err
	while True:
		print("Enter relative path to the image to be read (including the filename with extension):")
		path = input()
		file = Path(path)
		log.append("Path input: " + path)
		if file.is_file():
			log.append("File-path Verified")
			break
		else:
			err = "ERROR: Incorrect file-path!!"
			print(err)
			log.append(err)
			continue
	while True:
		print("Enter the image read mode:")
		print("\t0 - Colored image")
		print("\t1 - Black and White image")
		mode = int(input())
		log.append("Mode input: " + str(mode) + "")
		if mode in [0, 1]:
			mode = cv2.IMREAD_COLOR if 0 else cv2.IMREAD_GRAYSCALE
			log.append("Image Read Mode Verified and Assigned Assigned")
			break
		else:
			err = "ERROR: Value out of range!!"
			print(err)
			log.append(err)
			continue
	image = cv2.imread(path, mode)
	return image


def denoise(image, mode=1, quality=0):
	"""
	Removes noise from the image
	
	Parameters:
		image   -- OpenCV Image Object
		mode    -- Color mode (default = 1)
					1 -- Colored image
					0 -- Gray-scale image
		quality -- used to specify the de-noising quality (default = 0)
					-1 -- low (Moderate Noise, High End Image Detail, Very Low Colored Image Distortion)
					0  -- medium (Low Noise, Moderate End Image Detail, Low Colored Image Distortion)
					1  -- high (Very Low Noise, Low End Image Detail, Moderate Colored Image Distortion)
	"""
	dst = None
	template_window_size = 7
	search_window_size = 21
	if quality == -1:
		h = 5
		if mode == 1:
			h_color = 5
	elif quality == 0:
		h = 10
		if mode == 1:
			h_color = 10
	else:
		h = 15
		if mode == 1:
			h_color = 15
	if mode == 1:
		cv2.fastNlMeansDenoisingColored(image, dst, h, h_color, template_window_size, search_window_size)
	else:
		cv2.fastNlMeansDenoising(image, dst, h, template_window_size, search_window_size)
