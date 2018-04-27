# coding=utf-8
"""
:Name: interface.py
:Description: A terminal based interface for accessing the analyser
:Author: blackk100 - https://blackk100.github.io/
:Version: Pre-Alpha
:Dependencies: NumPy and matplotlib
"""

from pprint import pprint  # Pretty print
from time import sleep     # Time delay
import numpy               # NumPy
# import cv2                 # OpenCV
import matplotlib          # matplotlib
import errors              # Custom Errors
import analyser            # CV_Analyser


color, gray_scale = None, None
o_name = ""


def menu() -> int:
	"""
	Prints the menu and accepts the option selected

	:return: The menu option
	:rtype: int
	"""

	string = [
		"Options:",
		"\t1) Read a new image",
		"\t2) Display the current image",
		"\t3) Save the current image",
		"\t4) Remove Noise from the Image\n\t\t(The Image Gradient extraction function does this automatically)",
		"\t5) Get the Image Gradient\n\t\t(The Edge Detection & Histogram Generation functions do this automatically)",
		"\t6) Detect Edges in the current image",
		"\t7) Generate a Color Frequency Histogram of the current image",
		"\t8) Exit\n\t\t(Hard-exits. DOES NOT SAVE THE CURRENT IMAGE!)"
	]
	pprint(string)
	while True:
		try:
			inpt = int(input("Select option: "))
			if inpt not in range(1, 9):
				raise errors.MenuOptionOutOfRangeError
			else:
				return inpt
		except ValueError:
			print("ERROR: Incorrect data type error!")
		except errors.MenuOptionOutOfRangeError as e:
			print("ERROR: " + e.message)
		finally:
			print("Valid options are from 1 to 8 (inclusive).\n")


def prog_exit() -> bool:
	"""
	For exiting the interface

	:return: boolean value indicating user response
	:rtype: bool
	"""

	while True:
		try:
			print("Are you sure? (Y/N)?")
			conf = input().capitalize()
			if conf == "Y":
				return True
			elif conf == "N":
				return False
			else:
				raise errors.IncorrectProgramExitResponseError
		except errors.IncorrectProgramExitResponseError as e:
			print("ERROR: " + e.message)
		finally:
			print("Valid options are: 'Y', 'y', 'N' and 'n' only.")


def read() -> None:
	"""
	Modifies the global variables for the color & gray-scale images and the name of the image file

	:return: None
	:rtype: None
	"""
	global color
	global gray_scale
	global o_name
	color, gray_scale, o_name = analyser.read_img()


# TODO: Do this
def display(col=color, gray=gray_scale) -> None:
	"""
	Displays the current image as a matplotlib plot

	:param col: numpy.uint8 array (OpenCV Image Representation) (8-bit color image)
	:type col: numpy.uint8

	:param gray: numpy.uint8 array (OpenCV Image Representation) (8-bit Gray-scale image)
	:type gray: numpy.uint8

	:return: None
	:rtype: None
	"""
	pass


def save() -> None:
	"""
	Saves the current image (both 8-bit color and 8-bit gray-scale)

	:return: None
	:rtype: None
	"""

	print("Saving color image.")
	col_attempt = analyser.save_img(image = color, o_name = o_name + "_color")
	while not col_attempt:
		print("Unable to save the image for an unknown reason.")
		conf = False
		while not conf:
			try:
				print("Retry (Y/N)?")
				rep = input().capitalize()
				if rep not in ["Y", "N"]:
					raise errors.IncorrectImageSaveRetryResponseError
				elif rep == "Y":
					col_attempt = analyser.save_img(image = color, o_name = o_name + "_color")
				conf = True
			except errors.IncorrectImageSaveRetryResponseError as e:
				print("ERROR: " + e.message)
			finally:
				print("Valid options are: 'Y', 'y', 'N' and 'n' only.")

	print("Saving gray image.")
	gray_attempt = analyser.save_img(image = gray_scale, o_name = o_name + "_gray")
	while not gray_attempt:
		print("Unable to save the image for an unknown reason.")
		conf = False
		while not conf:
			try:
				print("Retry (Y/N)?")
				rep = input().capitalize()
				if rep not in ["Y", "N"]:
					raise errors.IncorrectImageSaveRetryResponseError
				elif rep == "Y":
					gray_attempt = analyser.save_img(image = gray_scale, o_name = o_name + "_color")
				conf = True
			except errors.IncorrectImageSaveRetryResponseError as e:
				print("ERROR: " + e.message)
			finally:
				print("Valid options are: 'Y', 'y', 'N' and 'n' only.")

	print("Done saving images.")


def change_current_image (col, gray) -> None:
	"""
	Used to change the current image after processing it. This function is automatically run after image processing.

	:param col: numpy.uint8 array (OpenCV Image Representation) (8-bit color image)
	:type col: numpy.uint8

	:param gray: numpy.uint8 array (OpenCV Image Representation) (8-bit Gray-scale image)
	:type gray: numpy.uint8

	:return: None
	:rtype: None
	"""
	global color
	global gray_scale
	print("Preview output (Y/N)?")
	conf = input()
	color, gray_scale = col, gray


# TODO: Do this
def noise() -> None:
	"""
	
	:return: None
	:rtype: None
	"""
	pass


# TODO: Do this
def gradient() -> None:
	"""
	
	:return: None
	:rtype: None
	"""
	pass


# TODO: Do this
def edges() -> None:
	"""
	
	:return: None
	:rtype: None
	"""
	pass


# TODO: Do this
def histogram() -> None:
	"""
	
	:return: None
	:rtype: None
	"""
	pass


def main() -> None:
	"""
	For running the interface

	:return: None
	:rtype: None
	"""
	img = None
	intro = [
		"\n Welcome to CV_Analyser!",
		"\n CV_Analyser is currently in alpha. The author takes no responsibility for any damages to any software"
		"or hardware. The author does not guarantee accurate results. Use at your own risk.\n",
		"\n Press Ctrl + C to force exit the program anytime (the program may lag for a few minutes while "
		"computing.\n Computation speed depends upon free CPU time and Memory (RAM) available).",
		"\n Any modifications done below cannot be undone, however, the original image file will remain "
		"untouched.\n Save regularly.",
		"\n Kindly keep track of all modifications you perform. CV_Analyser currently doesn't support "
		"modification tracking and external logging (or log dumping)",
	]
	pprint(intro)

	while True:  # Menu Navigation
		menu_opt = menu()
		if menu_opt == 1:  # Image reading
			read()
		elif menu_opt == 8:  # Exit
			rep = prog_exit()
			if rep:
				break
		else:
			if img is None:
				pass
			else:
				if menu_opt == 2:  # Display image
					display()
				elif menu_opt == 3:  # Save image
					save()
				elif menu_opt == 4:  # Remove noise
					noise()
				elif menu_opt == 5:  # Get Gradient
					gradient()
				elif menu_opt == 6:  # Get Edges
					edges()
				elif menu_opt == 7:  # Make histogram
					histogram()

	print("Thank you for using CV_Analyser!")
	print("Made by blackk100 (https://blackk100.github.io/)\n")
	sleep(5)
