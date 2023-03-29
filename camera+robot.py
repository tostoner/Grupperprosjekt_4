
###robot initialization. Works only in robodk
from robolink import*   # RoboDK API
from robodk import robomath, transl   # Robot toolbox
RDK = Robolink()
robot = RDK.Item('Omron TMX5-900', ITEM_TYPE_ROBOT)
perpendicular_to_conveyor_pos = -122
height_pos = 500
lenght_pos = 640

###camera initialization
import pyrealsense2 as rs
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
pipeline.start(config)

###Other libraries
import time




dist_close = 0.50 # closest possible reading
dist_to_conveyor = 1.00 # distance to conveyorbelt.
current_best_reading = dist_to_conveyor # used to compare depths

start_time = time.time()

positions = []
def findPositions():
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
            
            for y in y_range:
                depth = depth_frame.get_distance(x_coord, y)

                if depth < current_best_reading:
                    current_best_reading = depth                        
                    height_pos = dist_to_conveyor-depth
                    length_pos = y

            current_best_reading = dist_to_conveyor
                    #insert math for more precise length_pos here:
                    #

            positions.append(transl(length_pos,  perpendicular_to_conveyor_pos, height_pos))


            # Sleep for a short period of time to prevent high CPU usage
            time.sleep(0.1)

    finally:
        pipeline.stop()

def moveRobot(q):
    while True:
        position = q.get()
        robot.MoveJ(position)
        positions.pop(0)

while True:
    if len(positions) > 0:
        position = positions[0]