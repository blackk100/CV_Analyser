# CV_Analyser

CV_Analyser is a Python program and an accompanying terminal interface for processing images by using [OpenCV](https://opencv.org/ "OpenCV library").

## Warning
 * This project is currently under active design and development.
 * The author takes no responsibility for any damages to any software or hardware.
 * The author does not guarantee accurate results.
 * Downloading and/or running CV_Analyser implies that the user understands these risks.

## License
[MIT License](https://opensource.org/licenses/MIT "The MIT License | Open Source Initiative")

## Installation and Usage
1. Download and install [Python 3.6.5](https://www.python.org/downloads/release/python-365/ "Python Release Python 3.6.5 | Python.org")
    * Include the `pip` module.
    * Confirm that Python is accessible from a terminal (i.e., it is added to the system `PATH` variable).
2. [Clone](https://github.com/blackk100/CV_Analyser.git)/[download](https://github.com/blackk100/CV_Analyser/archive/master.zip) the repository.
3. Open a terminal, change the current working directory to that of the cloned repository/extracted 
 folder.
4. Run the following commands:

       python -m pip install pipenv
       python -m pipenv install --python 3.6.5
       python -m pipenv lock
       python -m pipenv sync
 
5. Run main.py:

       python -m pipenv run python main.py

## TODO
 * Create an executable binary file.
 * Use Java for a cross-platform GUI version.
 * Modify the histogram plots to super-impose the color of the pixel on the plotted line itself.
 * Change the histogram plots from lines to bars. Super-impose the color of the pixel on the plotted bars.
