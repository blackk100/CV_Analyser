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
	""" Reads and returns an image """
	log.append("read() Started")
	from pathlib import Path  # Used for checking if the file exists
	global err
	while True:
		print("Enter relative path to the image to be read (including the filename with extension):")
		path = input()
		file = Path(path)
		log.append("Path input: " + path + "")
		if file.is_file():
			log.append("File-path Verified")
			break
		else:
			err = "ERROR: Incorrect file-path!!"
			print(err)
			log.append("" + err + "")
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
			print("ERROR: Value out of range!!")
			continue
	img = cv2.imread(path, mode)
	return img
