import cv2
import numpy as np
import sys
from math import dist

print(sys.setrecursionlimit(30000))

#####
def gen_lift_pen_line(lift_height, feed_rate):
    return f'G1 Z{lift_height:.2f} F{feed_rate:.2f}'

def gen_lower_pen_line(depth, feed_rate):
    return f'G1 Z{-depth:.2f} F{feed_rate:.2f}'

def gen_move_to_loc_line(x, y):
    return f'G0 X{x:.2f} Y{y:.2f}'

def fill(x, y, pixels_to_draw, output_blob, h, w):
    if (x, y) not in pixels_to_draw:
        return
    else:
        output_blob.append((x, y))
        pixels_to_draw.remove((x, y))
        neighbours = [(x-1,y),(x+1,y),(x-1,y-1),(x+1,y+1),(x-1,y+1),(x+1,y-1),(x,y-1),(x,y+1)]
        for n in neighbours:
            fill(n[0], n[1], pixels_to_draw, output_blob, h, w)

def image_to_gcode(image, filename, max_depth=5.0, feed_rate=1500, lift_height=5, max_distance=100, edge_threshold=30, scale_x=3, scale_y=4):
    _, width = image.shape
    gcode_lines = []

    # Add header
    gcode_lines.append("(G-code output for Universal Robots' Remote TCP & Toolpath URCap)")
    gcode_lines.append("(UR Toolpath Generator Version : 1.0)")
    gcode_lines.append("%PM0")
    gcode_lines.append("N10 G21 G90")

    x, y, w, h = 0, 0, image.shape[1], image.shape[0]

    pixels_to_draw = []
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            if image[yy - y, xx - x] > edge_threshold:
                pixels_to_draw.append((xx, yy))

    print("Number of pixels = ", len(pixels_to_draw))
    blobs = []
    while pixels_to_draw:
        blob = []
        fill(pixels_to_draw[0][0], pixels_to_draw[0][1], pixels_to_draw, blob, width, h)
        blobs.append(blob)

    gcode_lines.append(gen_lift_pen_line(lift_height, feed_rate))
    pen_lifted = False

    print("Number of Blobs = ", len(blobs))
    for blob in blobs:
        # move to first point
        first_point = blob[0]
        fp_x = first_point[0]
        fp_y = first_point[1]

        x_gcode = fp_x / width * 100 * scale_x
        y_gcode = fp_y / h * 100 * scale_y
        # depth = max_depth * (1 - image[fp_y - y, fp_x - x] / 255)
        depth = 4.0
        gcode_lines.append(gen_move_to_loc_line(x_gcode, y_gcode))

        # lower pen
        gcode_lines.append(gen_lower_pen_line(depth, feed_rate))

        last_pixel = None
        # for each pixel
        for pixel in blob:
            px_x = pixel[0]
            px_y = pixel[1]
            x_gcode = px_x / width * 100 * scale_x
            y_gcode = px_y / h * 100 * scale_y

            
            if last_pixel:
                distance = dist((px_x, px_y), last_pixel)
            
                if distance > 5:
                    gcode_lines.append(gen_lift_pen_line(lift_height, feed_rate))
            else:
                distance = 0

            last_pixel = (px_x, px_y)
            # move pen to point
            gcode_lines.append(gen_move_to_loc_line(x_gcode, y_gcode))
            
            if last_pixel and distance > 5:
                gcode_lines.append(gen_lower_pen_line(depth, feed_rate))

        # lift pen
        gcode_lines.append(gen_lift_pen_line(lift_height, feed_rate))
        pen_lifted = True
                
    with open(filename, "w") as f:
        f.write("\n".join(gcode_lines))

#####

# Load the image file
image_path = "/home/antonio/Desktop/python scripts/robot club/Jpeg2Gcode/test images/scoop.png"  # Change this to the path of your image file png or jpeg
image = cv2.imread(image_path)

# Check if the image is valid
if image is None:
    print("Error: Image file not found or not valid.")
    sys.exit(1)

# Convert to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Sobel edge extraction to the image
sobel_x = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=5)
sobel_y = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=5)
sobel_edges = cv2.magnitude(sobel_x, sobel_y)
sobel_edges = cv2.normalize(sobel_edges, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

# Define your scaling factors here
scale_x = 3 ## adjust this to chnage the output scale
scale_y = 4 ## adjust this to chnage the output scale

image_to_gcode(sobel_edges, "GCODE.nc", scale_x=scale_x, scale_y=scale_y)
print("G-code saved as GCODE.nc")


