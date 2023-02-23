import pyrealsense2 as rs
import csv
import matplotlib.pyplot as plt
import time

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

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
        x_coord = 320

        # Initialize a list to store the depth values
        depths = []

        with open('depth_values.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['y', 'z'])
            for y in range(intrinsics.height):
                depth = depth_frame.get_distance(x_coord, y)
                if depth > 0:
                    csvwriter.writerow([y, depth])
                    depths.append(depth)

        print('Depth values for x = {} saved to depth_values.csv'.format(x_coord))

        # Update the plot
        ax.clear()
        ax.plot(depths)
        ax.set_xlabel('y')
        ax.set_ylabel('depth')
        ax.set_title('Depth values for x = {}'.format(x_coord))
        plt.pause(0.01)
    




        # Sleep for a short period of time to prevent high CPU usage
        time.sleep(0.1)

        # Stop the loop after 10 seconds
        if time.time() - start_time >= 30:
            break

finally:
    pipeline.stop()
