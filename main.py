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
				print("\n ERROR: Incorrect option entered!! Please only input a number between 1 & 8 (inclusive)!!")
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
				print("ERROR: No image file loaded!!")
				continue
			else:
				if menu_opt == 2:  # Display image
					pass
				elif menu_opt == 3:  # Save image
					analyser.save(img, img_mod[0], img_mod[1], img_mod[2], img_mod[3], img_mod[4], img_mod[5])
				elif menu_opt == 4:  # Remove noise
					pass
				elif menu_opt == 5:  # Get Gradient
					pass
				elif menu_opt == 6:  # Get Edges
					pass
				elif menu_opt == 7:  # Make histogram
					pass

print("Thank you for using CV_Analyser!")
print("Made by blackk100 (https://blackk100.github.io/)")
sleep(5)
