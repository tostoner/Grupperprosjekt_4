import pyrealsense2 as rs
import csv
import time
import datetime
import matplotlib.pyplot as plt

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

pipeline.start(config)
max_depths = []
max_heights = []
short_dist_to_conv = 0.49 # dist to closest edge of conveyor belt. min 0.49
long_dist_to_conv = 1.00 # dist to furthest edge of conveyor belt.

start_time = time.time()
max_depth = 0
max_y = None
nullCounter = 0

try:
    while True:
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()

        # Get the depth sensor's intrinsic properties
        profile = depth_frame.profile
        intrinsics = profile.as_video_stream_profile().intrinsics

        # Define the x-coordinate that you want to export
        x_coord = 320 # select x-coordinate to read ranges from
        y_range = range(100,320) #Set top and bottom of detection range respectivly(0 is top of camera). Use updating plot to find locations after mounting camera
        

        prevMax=0
        prevMaxY=0
        for y in y_range:
            depth = depth_frame.get_distance(x_coord, y)
            if short_dist_to_conv < depth < long_dist_to_conv:
                if depth>prevMax:
                    prevMax = round(depth,4)
                    prevMaxY = y
                    print(f"new max depth{prevMax}, with height {y}")

                max_depths.append(round(prevMax,4))
                max_heights.append(prevMaxY)

            if depth == 0.0: # Something to clear list after fish have passed. Maybe stupid
                nullCounter+=1
                if nullCounter >=10:
                    print(f"clearing depths. nullCountr = {nullCounter}")
                    max_depths.clear
            else:
                nullCounter = 0

        # Sleep for a short period of time to prevent high CPU usage
        time.sleep(0.1)

        # Stop the loop after 10 seconds
        if time.time() - start_time >= 10:
            print("timeout")
            break

finally:
    pipeline.stop()
    print(f"{max_depths}")
    
    
   