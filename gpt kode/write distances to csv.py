import pyrealsense2 as rs
import csv
import time

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

pipeline.start(config)

start_time = time.time()
try:
    while True:
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()

        # Get the depth sensor's intrinsic properties
        profile = depth_frame.profile
        intrinsics = profile.as_video_stream_profile().intrinsics

        # Define the x-coordinate that you want to export
        x_coord = 320
        y_range = range(100,320)

        # Initialize variables to store the biggest depth and its corresponding y-coordinate
        max_depth = 0
        max_y = None

        with open('depth_values.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['y', 'z'])
            for y in y_range:
                depth = depth_frame.get_distance(x_coord, y)
                if 0.49 <= depth <= 1:
                    csvwriter.writerow([y, depth])
                    if depth > max_depth:
                        max_depth = depth
                        max_y = y

        if max_depth > 0:
            print('Biggest depth: {} at y = {}'.format(max_depth, max_y))

        # Sleep for a short period of time to prevent high CPU usage
        time.sleep(0.1)

        # Stop the loop after 10 seconds
        if time.time() - start_time >= 30:
            print("timeout")
            break

finally:
    pipeline.stop()
