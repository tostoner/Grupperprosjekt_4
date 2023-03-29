import pyrealsense2 as rs
import csv
import matplotlib.pyplot as plt
import time
import numpy as np


pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
selected_xrange = range(166, 450+1)
depths = []
x_coords = []
pipeline.start(config)

fig, ax = plt.subplots()
plt.ion()
start_time = time.time()
try:
    while True:
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()

        # Get the depth sensor's intrinsic properties
        profile = depth_frame.profile
        intrinsics = profile.as_video_stream_profile().intrinsics

        # Define the x-coordinate that you want to export
        y_coord = int(intrinsics.height/2)

        # Initialize a list to store the depth values

        tempDepths=[]
        temp_x_coords=[]
        for x in selected_xrange:
            depth = depth_frame.get_distance(x, y_coord)
            if depth > 0.5 and depth < 1.0175:
                tempDepths.append(depth)
                temp_x_coords.append(x)
            else:
                tempDepths.append(99)
                temp_x_coords.append(99)
           # print(tempDepths)
            if tempDepths:
                d = min(tempDepths)
                if d is not None:
                    d_index = tempDepths.index(d)
                    depths.append(d)
                    x_coords.append(temp_x_coords[d_index])
                    #print(d)
                tempDepths.clear()
                temp_x_coords.clear()
                ax.clear()
        ax.plot(depths)
        ax.set_xlabel('y')
        ax.set_ylabel('depth')
        ax.set_title('Depth values for x = {}'.format(y_coord))
        plt.pause(0.01)

        # Update the plot
        # Sleep for a short period of time to prevent high CPU usage
        time.sleep(0.5)
        print("loop")

        # Stop the loop after 10 seconds
        if time.time() - start_time >= 10:
            print("break")
            break


finally:
    pipeline.stop()
    i=0

