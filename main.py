# coding=utf-8
"""
:Name: main.py
:Description: A Python based commandline interface to the analyser
:Author: blackk100 (blackk100.github.io)
:External Dependencies: NumPy and OpenCV (see 'Pipfile' for packages)
:Made with: PyCharm Community and pipenv
"""

from pprint import pprint  # Pretty print
from time import sleep     # Time delay
import cv2                 # OpenCV
import analyser            # CV_Analyser

if __name__ == "__main__":
	def menu() -> int:
		"""
		Prints the menu, accepts the option selected

		:return: The menu option
		:rtype: int
		"""
		strings = [
			"\n Press Ctrl + C to force exit the program anytime (the program may lag for a few minutes while "
			"computing.\n Computation speed depends upon free CPU time and Memory (RAM) available).",
			"\n Any modifications done below cannot be undo-ed, however, the original image file will remain "
			"untouched.\n Save regularly.",
			"\n Kindly keep track of all modifications you perform. CV_Analyser currently doesn't support "
			"modification tracking and external logging (or log dumping)"
			"\n Options:",
			" \t1) Read a new image",
			" \t2) Display the current image",
			" \t3) Save the current image",
			" \t4) Remove Noise from the Image (The Image Gradient extraction function does this automatically)",
			" \t5) Get the Image Gradient (The Edge Detection & Histogram Generation functions do this automatically)",
			" \t6) Detect Edges in the current image",
			" \t7) Generate a Color Frequency Histogram of the current image",
			" \t8) Exit (Hard-exits with no confirmation. DOES NOT SAVE THE CURRENT IMAGE)"
		]
		while True:
			pprint(strings)
			try:
				inpt = int(input())
				if inpt not in range(1, 9):
					raise ValueError
				else:
					return inpt
			except ValueError:
				print("\n ERROR: Incorrect option entered!! Please only enter a number between 1 & 8!!")
				continue

	img = None
	img_mod = ["", -2, -2, -2, False, -1]  # Used for saving modified files
	while True:
		menu_opt = menu()
		if menu_opt == 1:  # Image reading
			read = analyser.read()
			img = read[0]
			img_mod[0] = read[1].split(".", 1)[0]
		elif menu_opt == 8:  # Exit
			break
		else:
			if img is None:
				print("\n ERROR: No image file loaded!!")
				continue
			else:
				if menu_opt == 2:  # Display image
					pass
				elif menu_opt == 3:  # Save image
					analyser.save(img, img_mod[0], img_mod[1], img_mod[2], img_mod[3], img_mod[4], img_mod[5])
				elif menu_opt == 4:  # Remove noise
					while True:
						try:
							oupt = [
								"\n Enter the de-noising quality:",
								" \t1) Moderate Noise, High End Image Detail, Very Low Colored Image Distortion",
								" \t2) Low Noise, Moderate End Image Detail, Low Colored Image Distortion",
								" \t3) Very Low Noise, Low End Image Detail, Moderate Colored Image Distortion"
							]
							pprint(oupt)
							quality = int(input()) - 2
							if quality not in range(-1, 2):
								raise ValueError
							else:
								break
						except ValueError:
							print("\n ERROR: Incorrect option entered!! Please only enter a number between 1 & 3!!")
							continue
					while True:
						try:
							oupt = [
								"\n Enter the image colour-space (Entering an incorrect value can cause unexpected "
								"behaviour, and may even lead to the program to crash):",
								" \t1) Gray-scale",
								" \t2) Coloured"
							]
							pprint(oupt)
							mode = int(input()) - 1
							if mode not in [0, 1]:
								raise ValueError
							else:
								break
						except ValueError:
							print("\n ERROR: Incorrect option entered!! Please only enter a number between 1 & 2!!")
							continue
					img = analyser.de_noise(img, mode, quality)
				elif menu_opt == 5:  # Get Gradient
					while True:
						try:
							oupt = [
								"\n Enter the gradient type:",
								" \t1) Scharr Derivative (Y-Axis)",
								" \t2) Laplacian Derivative",
								" \t3) Scharr Derivative (X-Axis)"
							]
							pprint(oupt)
							mode = int(input()) - 2
							if mode not in range(-1, 2):
								raise ValueError
							else:
								break
						except ValueError:
							print("\n ERROR: Incorrect option entered!! Please only enter a number between 1 & 3!!")
							continue
					img = analyser.get_gradient(img, mode)
				elif menu_opt == 6:  # Get Edges
					while True:
						try:
							oupt = [
								"\n Enter the 1st threshold for the hysteresis procedure",
								" (-1 for default values)",
								" (Very high or low values can cause unusual behaviour and may even crash the program)"
							]
							pprint(oupt)
							print("\n 1st Threshold Value: ")
							threshold_1 = int(input())
							print("\n 2nd Threshold Value: ")
							threshold_2 = int(input())
							d1 = threshold_1 == -1
							d2 = threshold_2 == -1
							break
						except ValueError:
							print("\n ERROR: Incorrect value entered!! Please only an integer greater than -2!!")
							continue
					if d1:
						if d2:  # d1 and d2
							img = analyser.detect_edge(img)
						else:  # only d1
							img = analyser.detect_edge(img, threshold_2 = threshold_2)
					elif d2:   # only d2
						img = analyser.detect_edge(img, threshold_1)
					else:      # neither d1 or d2
						img = analyser.detect_edge(img, threshold_1, threshold_2)
				elif menu_opt == 7:  # Make histogram
					pass

print("Thank you for using CV_Analyser!")
print("Made by blackk100 (https://blackk100.github.io/)")
sleep(5)
