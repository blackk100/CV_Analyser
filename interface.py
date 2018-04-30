# coding=utf-8
"""
:Name: interface.py
:Description: A terminal based interface for accessing the analyser
:Author: blackk100
:Version: Pre-Alpha
:Dependencies: NumPy, OpenCV and matplotlib
"""

from pprint import pprint      # Pretty print
from time import sleep         # Time delay
import numpy                   # NumPy
import cv2                     # OpenCV
from matplotlib import pyplot  # matplotlib (plotting module)
from matplotlib.font_manager import FontProperties  # matplotlib plots font modifiers
import errors                  # Custom Errors
import analyser                # CV_Analyser

color = None
gray_scale = None
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
		"\t2) Display image",
		"\t3) Remove Noise from Image",  # The Image Gradient extraction function does this automatically
		"\t4) Get the Image Gradient",   # The Edge Detection & Histogram Generation functions do this automatically)
		"\t5) Detect Edges in the image",
		"\t6) Generate Histograms",
		"\t7) Help"
		"\t8) Exit\n\t\t(Hard-exits. DOES NOT SAVE THE CURRENT IMAGE!)"
	]
	pprint(string)
	while True:
		try:
			inpt = int(input("Select option: "))
			if inpt not in range(1, 8):
				raise errors.MenuOptionOutOfRangeError
			else:
				return inpt
		except ValueError:
			print("ERROR: Incorrect data type error!")
		except errors.MenuOptionOutOfRangeError as e:
			print("ERROR: " + e.message)
		finally:
			print("Valid options are from 1 to 7 (inclusive).\n")


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


def prog_help() -> None:
	"""
	Shows basic help text

	:return: None
	:rtype: None
	"""
	string = [
		"About:"
		"\tCV_Analyser is a terminal based interface to the image processing library, OpenCV."
		"\tProgramming Language: Python 3"
		"\tAuthor: blackk100 - https:\\\\blackk100.github.io\\"
		"\tVersion: Pre-Alpha\n"
		"DISCLAIMER:"
		"\tCV_Analyser is currently in active development. The author takes no responsibility for any damages to any "
		"software or hardware. The author does not guarantee accurate results. Use at your own risk.\n",
		"\tPress Ctrl + C to force exit the program anytime (the program may lag for a few minutes while computing; "
		"Computation speed depends upon free CPU time and Memory (RAM) available).",
		"\tAny modifications done to the currently selected image cannot be undone, however, the original image file "
		"will remain untouched.",
		"\tKindly keep track of all modifications you perform. CV_Analyser currently doesn't support modification "
		"tracking and external logging (or log dumping)\n",
		"General:"
		"\tA prompt will ask if you wish to preview a modified image at the end of each process.",
		"\tFollowing this, another prompt will ask if you wish to save the modified image.",
		"\tThe previews have a toolbar which can be used to assist in viewing the modified image and in analysing "
		"generated histograms."
		"\t The toolbar contains a save function. It is recommended to use this function only for histograms due to "
		"the loss in image quality.\n"
		"De-noising Images:"
		"\tDe-noising images results in the removal of visual artifacts in images, at the cost of detail and "
		"sharpness."
		"\tAll CV_Analyser functions automatically de-noise the image.",
		"\tAs such, it is not necessary to compute it explicitly.\n"
		"Image Gradients:"
		"\tAn image gradient is a directional change in the intensity or color in an image."
		"\tImage gradients are fundamental to image processing."
		"\tAll CV_Analyser functions dependent on an image gradient compute it automatically.",
		"\tAs such, it is not necessary to compute it explicitly.\n"
		"Edge Detection:"
		"\tThis function utilises the Canny Edge Detection algorithm to detect and highlight the edges of 'objects'",
		"\tAny edges with an intensity (image) gradient more than upper threshold are sure to be edges.",
		"\tAny edges with an intensity (image) gradient below the lower threshold are sure to be non-edges, "
		"and are discarded.",
		"\tAny edges which lie between the two thresholds are classified edges or non-edges based on their "
		"connectivity.",
		"\tIf they are connected to “sure-edge” pixels, they are considered to be part of edges.",
		"\tOtherwise, they are also discarded.\n",
		"Histograms:"
		"\t2 Histograms are generated:"
		"\t\t1) Colour Frequency: Shows a plot of the number of times a specific colour (RGB, 8-bit) occurs in the "
		"image.",
		"\t\t2) Relative Brightness: Shows a plot of the number of times a specific monochromatic (gray-scale) color "
		"occurs in the image."
	]
	pprint(string)


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


def display(col, gray, mode=0) -> None:
	"""
	Displays the given images as a matplotlib plot.
	
	The plot consists of 2 rows with 2 images each:

	* Color images -- Original ; Processed
	* Gray-scale images -- Original ; Processed

	Is only called by image_process_end()

	:param col: numpy.uint8 array (OpenCV Image Representation) (8-bit color image)
	:type col: numpy.uint8 or list

	:param gray: numpy.uint8 array (OpenCV Image Representation) (8-bit gray-scale image)
	:type gray: numpy.uint8

	:param mode: Used to specify the image labels (default = 0)

	* 0 -- Default (NOTE: The plot becomes a 1 row, 2 column plot with the original color and gray-scale image side-by
	side)
	* 1 -- De-noised
	* 2 -- Laplacian Gradient
	* 3 -- Scharr (X-Axis) Gradient
	* 4 -- Scharr (Y-Axis) Gradient
	* 5 -- Edges
	* 6 -- Histogram
	:type mode: int

	:return: None
	:rtype: None
	"""

	title = ""
	pyplot.figure(1)
	pyplot.axis("off")
	if mode == 0:
		title = "Original Images"
		fig, ax = pyplot.subplots(ncols = 2)
		with ax[0, 0] as axis:
			axis.title("Color Image")
			axis.imshow(X = cv2.cvtColor(src = color, code = cv2.COLOR_BGR2RGB), aspect = "equal")
		with ax[0, 1] as axis:
			axis.title("Gray-scale Image")
			axis.imshow(X = gray_scale, aspect = "equal")
	elif mode != 6:
		img = [[color, col], [gray_scale, gray]]
		sub_title = [["Original Color Image", ""], ["Original Gray-scale Image", ""]]
		fig, ax = pyplot.subplots(nrows = 2, ncols = 2)
		if mode == 1:
			title = "De-noised Images"
			sub_title[0][1] = "De-noised Color Image"
			sub_title[1][1] = "De-noised Gray-scale Image"
		elif mode == 2:
			title = "Laplacian Gradient"
			sub_title[0][1] = "Laplacian Gradient on Color Image"
			sub_title[1][1] = "Laplacian Gradient on Gray-scale Image"
		elif mode == 3:
			title = "Scharr Gradient (X-Axis)"
			sub_title[0][1] = "Scharr Gradient (X-Axis) on Color Image"
			sub_title[1][1] = "Scharr Gradient (X-Axis) on Gray-scale Image"
		elif mode == 4:
			title = "Scharr Gradient (Y-Axis)"
			sub_title[0][1] = "Scharr Gradient (Y-Axis) on Color Image"
			sub_title[1][1] = "Scharr Gradient (Y-Axis) on Gray-scale Image"
		elif mode == 5:
			title = "Canny Edge Detection"
			sub_title[0][1] = "Edges in Color Image"
			sub_title[1][1] = "Edges in Gray-scale Image"
		for i in range(2):
			for j in range(2):
				with ax[i, j] as axis:
					axis.title(s = sub_title[i][j])
					if i == 0:
						axis.imshow(X = cv2.cvtColor(src = img[i][j], code = cv2.COLOR_BGR2RGB), aspect = "equal")
					else:
						axis.imshow(X = img[i], aspect = "equal")
	elif mode == 6:
		pyplot.axis("on")
		title = "Histograms"
		fig, ax = pyplot.subplots(nrows = 2, ncols = 2)
		with ax[0, 0] as axis:
			axis.title(s = "Color Image")
			axis.imshow(X = cv2.cvtColor(src = color, code = cv2.COLOR_BGR2RGB), aspect = "equal")
		with ax[0, 1] as axis:
			axis.title(s = "Color Frequency Histogram")
			colors = ["b", "g", "e"]
			for i in range(3):
				axis.plot(col[i], color = colors[i])
			axis.xlim(xmin = 0, xmax = 256)
			axis.ylim(ymin = 0)
		with ax[1, 0] as axis:
			axis.title(s = "Gray-scale Image")
			axis.imshow(X = gray_scale, aspect = "equal")
		with axis[1, 1] as axis:
			axis.title(s = "Relative Light Intensity Distribution Histogram")
			axis.plot(gray)
			axis.xlim(xmin = 0, xmax = 256)
			axis.ylim(ymin = 0)
	pyplot.suptitle(title, fontsize = 16)
	pyplot.show()


def save(col, gray) -> None:
	"""
	Saves the processed image (both 8-bit color and 8-bit gray-scale). Is only called by image_process_end()

	:param col: numpy.uint8 array (OpenCV Image Representation) (8-bit color image)
	:type col: numpy.uint8

	:param gray: numpy.uint8 array (OpenCV Image Representation) (8-bit gray-scale image)
	:type gray: numpy.uint8

	:return: None
	:rtype: None
	"""

	try:
		if col is None or gray is None:
			raise errors.NoImageInBufferError
		else:
			print("Saving color image.")
			col_attempt = analyser.save_img(image = col, o_name = o_name + "_color")
			while not col_attempt:
				conf = False
				while not conf:
					try:
						print("Retry (Y/N)?")
						rep = input().capitalize()
						if rep not in ["Y", "N"]:
							raise errors.IncorrectImageSaveRetryResponseError
						elif rep == "Y":
							col_attempt = analyser.save_img(image = col, o_name = o_name + "_color")
						conf = True
					except errors.IncorrectImageSaveRetryResponseError as e:
						print("ERROR: " + e.message)
					finally:
						print("Valid options are: 'Y', 'y', 'N' and 'n' only.")
			print("Saving gray image.")
			gray_attempt = analyser.save_img(image = gray, o_name = o_name + "_gray")
			while not gray_attempt:
				conf = False
				while not conf:
					try:
						print("Retry (Y/N)?")
						rep = input().capitalize()
						if rep not in ["Y", "N"]:
							raise errors.IncorrectImageSaveRetryResponseError
						elif rep == "Y":
							gray_attempt = analyser.save_img(image = gray, o_name = o_name + "_gray")
						conf = True
					except errors.IncorrectImageSaveRetryResponseError as e:
						print("ERROR: " + e.message)
					finally:
						print("Valid options are: 'Y', 'y', 'N' and 'n' only.")
			print("Done saving images.")
	except errors.NoImageInBufferError as e:
		print("ERROR: " + e.message)


def image_process_end(col, gray, mode=0) -> None:
	"""
	This function is automatically run after image processing. Shows a preview of the processed image and saves it
	(after user confirmation for either action)

	:param col: numpy.uint8 array (OpenCV Image Representation) (8-bit color image)
	:type col: numpy.uint8 or list

	:param gray: numpy.uint8 array (OpenCV Image Representation) (8-bit gray-scale image)
	:type gray: numpy.uint8

	:param mode: Used to specify the image labels (default = 0)

	* 0 -- Default (NOTE: The plot becomes a 1 row, 2 column plot with the original color and gray-scale image side-by
	side)
	* 1 -- De-noised
	* 2 -- Scharr (Y-Axis) Gradient
	* 3 -- Laplacian Gradient
	* 4 -- Scharr (X-Axis) Gradient
	* 5 -- Edges
	* 6 -- Histogram
	:type mode: int

	:return: None
	:rtype: None
	"""
	conf_f = False
	while not conf_f:
		try:
			print("Preview output (Y/N)?")
			conf = input().capitalize()
			if conf not in ["Y", "N"]:
				raise errors.IncorrectImagePreviewResponseError
			elif conf == "Y":
				display(col = col, gray = gray, mode = mode)
			conf_f = True
		except errors.IncorrectImagePreviewResponseError as e:
			print("ERROR: " + e.message)
		finally:
			print("Valid options are: 'Y', 'y', 'N' and 'n' only.")
	conf_f = False
	while not conf_f:
		try:
			print("Save output (Y/N)?")
			conf = input().capitalize()
			if conf not in ["Y", "N"]:
				raise errors.IncorrectImageSaveConfResponseError
			elif conf == "Y":
				save(col = col, gray = gray)
			conf_f = True
		except errors.IncorrectImageSaveConfResponseError as e:
			print("ERROR: " + e.message)
		finally:
			print("Valid options are: 'Y', 'y', 'N' and 'n' only.")


def noise() -> None:
	"""
	User interface for de-noising images

	:return: None
	:rtype: None
	"""
	strings = [
		"Specify de-noising quality:",
		"1. Low (Moderate Noise, High End Image Detail, Very Low Colored Image Distortion)",
		"2. Moderate (Low Noise, Moderate-High End Image Detail, Low Colored Image Distortion)",
		"3. High (Very Low Noise, Moderate-Low End Image Detail, Moderate Colored Image Distortion)",
		"(Recommended: Moderate)"
	]
	nf = False
	while not nf:
		try:
			pprint(strings)
			quality = int(input("Enter a number between 1-3 indicting the quality: "))
			if quality not in range(4):
				raise errors.DenoiseQualityOutOfRangeError
			color_p, gray_p = analyser.de_noise(color = color, gray = gray_scale, quality = quality - 2)
			image_process_end(col = color_p, gray = gray_p, mode = 1)
			nf = True
		except ValueError:
			print("ERROR: Incorrect data type entered!")
		except errors.DenoiseQualityOutOfRangeError as e:
			print("ERROR: " + e.message)
		finally:
			print("Valid input is only a numeric character between 1 and 3 (inclusive).")
			conf = False
			while not conf:
				try:
					print("Retry (Y/N)?")
					rep = input().capitalize()
					if rep not in ["Y", "N"]:
						raise errors.IncorrectDenoiseRetryResponseError
					elif rep == "N":
						nf = True
					conf = True
				except errors.IncorrectDenoiseRetryResponseError as e:
					print("ERROR: " + e.message)
				finally:
					print("Valid options are: 'Y', 'y', 'N' and 'n' only.")


def gradient() -> None:
	"""
	User interface for getting the image gradient

	:return: None
	:rtype: None
	"""
	strings = [
		"Specify which image gradient to generate:",
		"1. Scharr Gradient (Y-Axis)",
		"2. Laplacian Gradient",
		"3. Scharr Gradient (X-Axis)"
	]
	gf = False
	while not gf:
		try:
			pprint(strings)
			grad = int(input("Enter a number between 1-3 indicting the gradient: "))
			if grad not in range(4):
				raise errors.GradientTypeOutOfRangeError
			color_g, gray_g = analyser.get_gradient(color = color, gray = gray_scale, mode = grad - 2)
			image_process_end(col = color_g, gray = gray_g, mode = grad + 1)
			gf = True
		except ValueError:
			print("ERROR: Incorrect data type entered!")
		except errors.GradientTypeOutOfRangeError as e:
			print("ERROR: " + e.message)
		finally:
			print("Valid input is only a numeric character between 1 and 3 (inclusive).")
			conf = False
			while not conf:
				try:
					print("Retry (Y/N)?")
					rep = input().capitalize()
					if rep not in ["Y", "N"]:
						raise errors.IncorrectGradientRetryResponseError
					elif rep == "N":
						gf = True
					conf = True
				except errors.IncorrectGradientRetryResponseError as e:
					print("ERROR: " + e.message)
				finally:
					print("Valid options are: 'Y', 'y', 'N' and 'n' only.")


def edges() -> None:
	"""
	User interface for the detecting edges

	:return: None
	:rtype: None
	"""
	t1, t2 = -1, -1
	tf = False
	while not tf:
		try:
			t1 = int(input("Enter the lower gradient threshold (enter -1 for the default = 100): "))
			if t1 < -1:
				raise errors.EdgeLowerThresholdOutOfRangeError
			tf = True
		except ValueError:
			print("ERROR: Incorrect data type entered!")
		except errors.EdgeLowerThresholdOutOfRangeError as e:
			print("ERROR: " + e.message)
		finally:
			print("Valid input is only a numeric character >= -1.")
			conf = False
			while not conf:
				try:
					print("Retry (Y/N)?")
					rep = input().capitalize()
					if rep not in ["Y", "N"]:
						raise errors.IncorrectEdgeLowerThresholdRetryResponseError
					elif rep == "N":
						tf = True
					conf = True
				except errors.IncorrectEdgeLowerThresholdRetryResponseError as e:
					print("ERROR: " + e.message)
				finally:
					print("Valid options are: 'Y', 'y', 'N' and 'n' only.")
	tf = False
	while not tf:
		try:
			t2 = int(input("Enter the upper gradient threshold (enter -1 for the default = 250): "))
			if t2 < -1:
				raise errors.EdgeLowerThresholdOutOfRangeError
			tf = True
		except ValueError:
			print("ERROR: Incorrect data type entered!")
		except errors.EdgeLowerThresholdOutOfRangeError as e:
			print("ERROR: " + e.message)
		finally:
			print("Valid input is only a numeric character >= -1.")
			conf = False
			while not conf:
				try:
					print("Retry (Y/N)?")
					rep = input().capitalize()
					if rep not in ["Y", "N"]:
						raise errors.IncorrectEdgeUpperThresholdRetryResponseError
					elif rep == "N":
						tf = True
					conf = True
				except errors.IncorrectEdgeUpperThresholdRetryResponseError as e:
					print("ERROR: " + e.message)
				finally:
					print("Valid options are: 'Y', 'y', 'N' and 'n' only.")
	if t1 == -1:
		if t2 == -1:
			color_e, gray_e = analyser.detect_edge(color = color, gray = gray_scale)
		else:
			color_e, gray_e = analyser.detect_edge(color = color, gray = gray_scale, threshold_2 = t2)
	else:
		if t2 == -1:
			color_e, gray_e = analyser.detect_edge(color = color, gray = gray_scale, threshold_1 = t1)
		else:
			color_e, gray_e = analyser.detect_edge(
					color = color,
					gray = gray_scale,
					threshold_1 = t1,
					threshold_2 = t2
			)
	image_process_end(col = color_e, gray = gray_e, mode = 5)


def histogram() -> None:
	"""
	Calls the histogram generation function of the analyser after denoising the image

	:return: None
	:rtype: None
	"""
	col_d, gray_d = analyser.de_noise(color = color, gray = gray_scale)
	col_h, gray_h = analyser.histogram_gen(color = col_d, gray = gray_d)
	image_process_end(col = col_h, gray = gray_h, mode = 6)


def main() -> None:
	"""
	For running the interface

	:return: None
	:rtype: None
	"""
	intro = [
		"Welcome to CV_Analyser!",
		"CV_Analyser is currently in active development. The author takes no responsibility for any damages to any "
		"software or hardware. The author does not guarantee accurate results. Use at your own risk.\n",
		"Press Ctrl + C to force exit the program anytime (the program may lag for a few minutes while computing; "
		"Computation speed depends upon free CPU time and Memory (RAM) available).",
		"Any modifications done to the currently selected image cannot be undone, however, the original image file "
		"will remain untouched.",
		"Kindly keep track of all modifications you perform. CV_Analyser currently doesn't support modification "
		"tracking and external logging (or log dumping)",
	]
	pprint(intro)

	while True:  # Menu Navigation
		menu_opt = menu()
		if menu_opt == 1:  # Image reading
			read()
		elif menu_opt == 7:  # Help
			prog_help()
		elif menu_opt == 8:  # Exit
			rep = prog_exit()
			if rep:
				break
		else:
			if (color is None) or (gray_scale is None):  # No images in global variables
				pass
			else:  # Images present in global variables
				if menu_opt == 2:  # Display image
					display(col = color, gray = gray_scale)
				elif menu_opt == 3:  # Remove noise
					noise()
				elif menu_opt == 4:  # Get Gradient
					gradient()
				elif menu_opt == 5:  # Get Edges
					edges()
				elif menu_opt == 6:  # Make histogram
					histogram()

	print("Thank you for using CV_Analyser!")
	sleep(2)
