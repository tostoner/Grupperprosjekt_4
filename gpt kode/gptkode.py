import pyrealsense2 as rs
import csv
import matplotlib.pyplot as plt
import time
bottom = 10
top = 200

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

pipeline.start(config)
testnum = 0
try:
    while testnum<10:

        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()

        # Get the depth sensor's intrinsic properties
        profile = depth_frame.profile
        intrinsics = profile.as_video_stream_profile().intrinsics

        # Define the x-coordinate that you want to export
        start_y = 110
        end_y = 400 #max 479
        x_coord = 320

        # Initialize a list to store the depth values
        depths = []

        with open('depth_values.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['y', 'z'])
            for y in range(start_y,end_y):

                depth = depth_frame.get_distance(x_coord, y)
                if depth > 0:
                    csvwriter.writerow([y, depth])
                    depths.append(depth)

        print('Depth values for x = {} saved to depth_values.csv'.format(x_coord))

        with open('depth_values.csv') as df:
            reader = csv.reader(df)
            next(reader)
            for row in reader:
                y_coord = float(row[0])
                dist = float(row[1])
                top_of_fish = 0
                if dist > top_of_fish < 2:
                    fdist = dist
                    fy_coord = y_coord
            print(f'top of fish is {dist} meters away at y_coordinate {y_coord}')


    # Generate a plot of the depth values
    # plt.plot(depths)
    #plt.xlabel('y')
    #plt.ylabel('depth')
    #plt.title('Depth values for x = {}'.format(x_coord))
    #plt.show()
        testnum +=1
        time.sleep(0.1)

finally:
    pipeline.stop()
