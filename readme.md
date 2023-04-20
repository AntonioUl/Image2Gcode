README for Image to G-code Conversion Scripts

This repository contains two Python scripts for converting images to G-code. These scripts can be used for generating G-code files that can be executed by CNC machines, 3D printers, or other devices that understand G-code.

####

*Script 1: image_to_gcode_1.py

This script takes an input image, converts it to grayscale, and applies Sobel edge extraction. It then generates G-code to draw the detected edges on a CNC machine. The output G-code file will be saved as "GCODE.nc".
Usage:

    1.Set the image_path variable to the path of your image file (png or jpeg).
    2.Modify the scale_x and scale_y variables to define the scaling factors for the X and Y axes.
    3.Run the script.

Output:

The G-code output from this script has a fixed pen depth of 4.0 units. The pen is lifted only if the distance between two consecutive points is greater than 5 units.

(THIS SCRIPT IS GOING TO GENERATE TEH DRAWING IN A MORE TRADITIONAL WAY WITH X AND Y MOVES)

####

*Script 2: image_to_gcode_2.py

This script is similar to the first one, but with some differences in the G-code output.
Usage:

    1.Set the image_path variable to the path of your image file (png or jpeg).
    2.Modify the scale_x, scale_y, and pen_thickness variables to define the scaling factors for the X and Y axes and the pen thickness.
    3.Run the script.

Output:

The G-code output from this script has a variable pen depth, depending on the intensity of the grayscale image. The pen is lifted if the distance between two consecutive points is greater than the specified pen_thickness value.
Summary of Output Differences

    Script 1 has a fixed pen depth, while Script 2 has a variable pen depth based on the grayscale image's intensity.
    Script 1 lifts the pen when the distance between points is greater than 5 units, while Script 2 lifts the pen when the distance is greater than the specified pen_thickness.

(THIS SCRIPT WILL CREATE THE DRAWING OUT OF POINTS RATHER THAN LINES, SO IS MORE APPLICABLE FOR TUFTING OPERATIONS WHERE WE DONT WANT ANY IN CONTACT X AND Y MOVES)

####
Dependencies

    OpenCV (cv2)
    Numpy

To install the dependencies, run:

pip install opencv-python numpy

License

This project is licensed under the MIT License.

This project is a work in progressed developed by the Ulster University robotics club. With special mention going to Benn H for his contributions. 
