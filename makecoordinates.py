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
dist_close = 0.49 # closest possible reading
dist_far = 1.00 # distance to conveyorbelt.

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

        # Define the camera x-coordinate that you want to read ranges on
        x_coord = 320 # select x-coordinate to read ranges from
        y_range = range(100,320) #Set top and bottom of detection range respectivly.
        
        prevMinDepth=100
        prevMaxY=100
        if depth < dist_far:
            for y in y_range:
                depth = depth_frame.get_distance(x_coord, y)
                height = dist_far - depth

                if depth<prevMinDepth:
                    prevMax = round(depth,4)
                    prevMaxY = y
                    print(f"new max depth{prevMax}, with height {y}")

                max_depths.append(round(prevMax,4))
                max_heights.append(prevMaxY)
        else:
            print(f"Nothing on conveyor")

        #Shit for å styre roboten
        #robot go to x og y




        # Sleep for a short period of time to prevent high CPU usage
        time.sleep(0.1)

        # Stop the loop after 1000 seconds
        if time.time() - start_time >= 1000:
            print("timeout")
            break

finally:
    pipeline.stop()
    print(f"{max_depths}")
    
    
   