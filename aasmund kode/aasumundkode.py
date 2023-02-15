import pyrealsense2 as rs
import numpy as np
import cv2
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Initialize the RealSense camera pipeline
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
pipeline.start(config)

# Define a function to get the 3D coordinates of a pixel in the depth image
def get_3d_coordinates(pixel_x, pixel_y, depth_frame, depth_intrinsics):
    depth = depth_frame.get_distance(pixel_x, pixel_y)
    x, y, z = rs.rs2_deproject_pixel_to_point(depth_intrinsics, [pixel_x, pixel_y], depth)
    return x, y, z

# Define the width of the transport belt
belt_width = 30  # cm

# Initialize lists to store the fish heights and positions
fish_heights = []
fish_positions = []

# Start the main loop
try:
    while True:
        # Wait for a new frame from the camera
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        if not depth_frame:
            continue

        # Get the intrinsic parameters of the camera
        depth_intrinsics = depth_frame.profile.as_video_stream_profile().intrinsics

        # Convert the depth image to a numpy array
        depth_image = np.asanyarray(depth_frame.get_data())

        # Find the minimum and maximum depths in the image
        min_depth, max_depth, _, _ = cv2.minMaxLoc(depth_image)

        # Calculate the threshold for detecting the fish
        threshold = (min_depth + max_depth) / 2

        # Convert the depth image to a binary image based on the threshold
        binary_image = cv2.threshold(depth_image, threshold, 1, cv2.THRESH_BINARY)[1]

        # Find the contours in the binary image
        contours, hierarchy = cv2.findContours(binary_image.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Find the contour with the largest area, which is assumed to be the fish
        max_contour = max(contours, key=cv2.contourArea)

        # Find the bounding box of the fish contour
        x, y, w, h = cv2.boundingRect(max_contour)

        # Calculate the height of the fish above the transport belt
        fish_height = get_3d_coordinates(x + w/2, y + h/2, depth_frame, depth_intrinsics)[2]
        fish_position = get_3d_coordinates(x + w/2, y + h/2, depth_frame, depth_intrinsics)[0]

        # Store the fish height and position in the lists
        fish_heights.append(fish_height)
        fish_positions.append(fish_position)

        # Plot the fish height and position in 3D
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(fish_position, 0, fish_height)
        ax.set_xlim([-belt_width/2, belt_width/2])
        ax.set_ylim([-1, 1])
        ax.set_zlim([0, max(fish_heights) + 0.1])
        plt.show()

except KeyboardInterrupt:
    # Stop the RealSense camera pipeline
    pipeline.stop()

    # Start the main loop
try:
    while True:
        # Wait for a new frame from the camera
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        if not depth_frame:
            continue

        # Get the intrinsic parameters of the camera
        depth_intrinsics = depth_frame.profile.as_video_stream_profile().intrinsics

        # Convert the depth image to a numpy array
        depth_image = np.asanyarray(depth_frame.get_data())

        # Find the minimum and maximum depths in the image
        min_depth, max_depth, _, _ = cv2.minMaxLoc(depth_image)

        # Calculate the threshold for detecting the fish
        threshold = (min_depth + max_depth) / 2

        # Convert the depth image to a binary image based on the threshold
        binary_image = cv2.threshold(depth_image, threshold, 1, cv2.THRESH_BINARY)[1]

        # Find the contours in the binary image
        contours, hierarchy = cv2.findContours(binary_image.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Find the contour with the largest area, which is assumed to be the fish
        max_contour = max(contours, key=cv2.contourArea)

        # Find the bounding box of the fish contour
        x, y, w, h = cv2.boundingRect(max_contour)

        # Calculate the height of the fish above the transport belt
        fish_height = get_3d_coordinates(x + w/2, y + h/2, depth_frame, depth_intrinsics)[2]
        fish_position = get_3d_coordinates(x + w/2, y + h/2, depth_frame, depth_intrinsics)[0]

        # Store the fish height and position in the lists
        fish_heights.append(fish_height)
        fish_positions.append(fish_position)
# Plot the fish height and position in 3D
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(fish_position, 0, fish_height)
        ax.set_xlim([-belt_width/2, belt_width/2])
        ax.set_ylim([-1, 1])
        ax.set_zlim([0, max(fish_heights) + 0.1])
        plt.show()
except KeyboardInterrupt:
    # Stop the RealSense camera pipeline
    pipeline.stop()