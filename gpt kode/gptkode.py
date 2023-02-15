import pyrealsense2 as rs
import csv
import matplotlib.pyplot as plt

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

pipeline.start(config)

try:
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

    # Generate a plot of the depth values
    plt.plot(depths)
    plt.xlabel('y')
    plt.ylabel('depth')
    plt.title('Depth values for x = {}'.format(x_coord))
    plt.show()

finally:
    pipeline.stop()
