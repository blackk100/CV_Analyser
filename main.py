# coding=utf-8
"""
:Name: main.py
:Description: A Python based commandline interface to the analyser
:Author: blackk100 (blackk100.github.io)
:External Dependencies: NumPy and OpenCV (see 'Pipfile' for packages)
:Made with: PyCharm Community and pipenv
"""

if __name__ == "__main__":
	from pprint import pprint  # Pretty print
	from time import sleep  # Time delay
	import cv2  # OpenCV
	import analyser  # CV_Analyser

	def menu() -> int:
		"""
		Prints the menu and accepts the option selected

		:return: The menu option
		:rtype: int
		"""
		string = [
			"\n Options:",
			" \t1) Read a new image",
			" \t2) Display the current image",
			" \t3) Save the current image",
			" \t4) Change the color-space of the current image",
			" \t5) Remove Noise from the Image (The Image Gradient extraction function does this automatically)",
			" \t6) Get the Image Gradient (The Edge Detection & Histogram Generation functions do this automatically)",
			" \t7) Detect Edges in the current image",
			" \t8) Generate a Color Frequency Histogram of the current image",
			" \t9) Exit (Hard-exits. DOES NOT SAVE THE CURRENT IMAGE!)"
		]
		while True:
			pprint(string)
			try:
				inpt = int(input())
				if inpt not in range(1, 9):
					raise ValueError
				else:
					return inpt
			except ValueError:
				print("\n ERROR: Incorrect option entered!! Please only enter a number between 1 & 8!!")
				continue

	def prog_exit() -> bool:
		""""""
		while True:
			try:
				print("Are you sure? (Y/N)")
				conf = input().capitalize()
				if conf == "Y":
					return True
				elif conf == "N":
					return False
				else:
					raise ValueError
			except ValueError:
				print("\n ERROR: Incorrect option entered!! Please only enter 'Y', 'y', 'N' or 'n'!!")
				continue

	img = None
	img_mod = ["", -2, -2, -2, False, -1]  # Used for saving modified files
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
			read = analyser.read()
			img = read[0]
			img_mod[0] = read[1].split(".", 1)[0]
		elif menu_opt == 9:  # Exit
			conf = prog_exit()
			if conf:
				break
			else:
				continue
		else:
			if img is None:
				print("\n ERROR: No image file loaded!!")
				continue
			else:
				if menu_opt == 2:  # Display image
					strings = [
						"\n Keymap:",
						" \tESC -- Exit display"
					]
					pprint(strings)
					sleep(2.5)
					print("\n Starting GUI. Refer to keymap given above.")
					sleep(2.5)
					cv2.imshow(img_mod[0], img)
					di = True
					while di:
						k = cv2.waitKey(0)
						if k == 27:
							print("ESC")
							cv2.destroyAllWindows()
							di = False
				elif menu_opt == 3:  # Save image
					analyser.save(img, img_mod[0], img_mod[1], img_mod[2], img_mod[3], img_mod[4], img_mod[5])
				elif menu_opt == 4:  # Change color-space
					pass
				elif menu_opt == 5:  # Remove noise
					while True:
						try:
							oupt = [
								"\n Enter the de-noising quality:",
								" \t1) Low      - Moderate Noise, High End Image Detail, Very Low Colored Image "
								"Distortion",
								" \t2) Moderate - Low Noise; Moderate End Image Detail, Low Colored Image Distortion",
								" \t3) High     - Very Low Noise, Low End Image Detail, Moderate Colored Image "
								"Distortion"
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
					mod = (mode * 10) + abs(quality)
					if quality < 0:
						mod *= -1
					img_mod[2] = mod
				elif menu_opt == 6:  # Get Gradient
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
					img_mod[3] = mode
				elif menu_opt == 7:  # Get Edges
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
					img_mod[4] = True
				elif menu_opt == 8:  # Make histogram
					strings = [
						"\n Keymap:",
						" \ta   -- Show histogram for color image in curve mode",
						" \tb   -- Show histogram for gray-scale image in curve mode (converts coloured image into "
						"gray-scale)",
						" \tc   -- Show histogram in line mode (converts coloured image into gray-scale)",
						" \ts   -- Save the current histogram",
						" \tESC -- Exit display"
					]
					pprint(strings)
					sleep(3)
					gray = analyser.change_color(img)
					print("\n Gray-scale image generated")
					curve_col = analyser.histogram_gen(img)
					print("\n Curve histogram for colored image generated")
					curve_gray = analyser.histogram_gen(gray)
					print("\n Curve histogram for gray-scale image generated")
					line_gray = analyser.histogram_gen(gray, 1)
					print("\n Line histogram for gra-scale image generated")
					sleep(2.5)
					print("\n Starting GUI. Refer to keymap given above.")
					sleep(2.5)
					cv2.imshow("Original Image - " + img_mod[0], img)
					ko = ""
					kn = cv2.waitKey(0)
					hf = True
					while hf:
						if kn == ord("a"):
							print("a")
							cv2.imshow("Curve Histogram (Colored) - " + img_mod[0], curve_col)
							cv2.imshow("Image (Colored) - " + img_mod[0], img)
							img_mod[5] = 0
						elif kn == ord("b"):
							print("b")
							cv2.imshow("Curve Histogram (Gray-scale) - " + img_mod[0], curve_gray)
							cv2.imshow("Image (Gray-scale) - " + img_mod[0], gray)
							img_mod[1] = 0
							img_mod[5] = 1
						elif kn == ord("c"):
							print("c")
							cv2.imshow("Line Histogram (Gray-scale) - " + img_mod[0], line_gray)
							cv2.imshow("Image (Gray-scale) - " + img_mod[0], gray)
							img_mod[1] = 0
							img_mod[5] = 1
						elif kn == ord("s"):
							print("s")
							if (ko == "") or (ko == "s"):
								print("\n ERROR: No histogram currently selected!!")
								continue
							else:
								if kn == ord("a"):
									pass
								elif kn == ord("b"):
									pass
								elif kn == ord("c"):
									pass
								else:
									pass
								analyser.save(
										img, img_mod[0], img_mod[1], img_mod[2], img_mod[3], img_mod[4],
										img_mod[5]
								)
						elif kn == 27:
							print("ESC")
							cv2.destroyAllWindows()
							hf = False
						ko, kn = kn, cv2.waitKey(0)

print("Thank you for using CV_Analyser!")
print("Made by blackk100 (https://blackk100.github.io/)")
sleep(5)
