import os
import subprocess
import time
import json
import csv

def launch_gazebo_simulation():
    # Open a new terminal and launch Gazebo simulation
    subprocess.Popen(['gnome-terminal', '--', 'ros2', 'launch', 'one_dynamixel_simulation', 'MX28AR_gazebo.launch.py'])

def send_joint_trajectory_command(feedback_file_path):
    # Wait for 5 seconds before sending the joint trajectory command
    time.sleep(4)

    # Open a new terminal and send the joint trajectory command
    trajectory = {
        "trajectory": {
            "joint_names": ['joint1'],
            "points": [
                {"positions": [0.0], "time_from_start": {"sec": 1}},
                {"positions": [-1.5708], "time_from_start": {"sec": 3}},
                {"positions": [0.0], "time_from_start": {"sec": 5}},
                {"positions": [1.5708], "time_from_start": {"sec": 7}},
                {"positions": [0.0], "time_from_start": {"sec": 9}}
            ]
        }
    }

    # Convert the trajectory dictionary to a JSON-formatted string
    trajectory_json = json.dumps(trajectory)

    # subprocess.Popen(['gnome-terminal', '--','ros2', 'action', 'send_goal', '/joint_trajectory_controller/follow_joint_trajectory', 'control_msgs/action/FollowJointTrajectory', '-f', trajectory_json])
    # Open a new process to execute the ROS command and capture output
    with open(feedback_file_path, 'w') as output_file:
        process = subprocess.Popen(
            ['ros2', 'action', 'send_goal', '/joint_trajectory_controller/follow_joint_trajectory', 
             'control_msgs/action/FollowJointTrajectory', '-f', trajectory_json], 
            stdout=output_file,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        # Wait for the process to complete
        process.wait()


if __name__ == '__main__':
    launch_gazebo_simulation()
    # send_joint_trajectory_command()
    feedback_file_path = '/home/jaku6m/Desktop/OPTYMALIZACJA/OptcsvGazeboFiles/output_file.txt'  # Path to the feedback text file
    output_csv_file = '/home/jaku6m/Desktop/OPTYMALIZACJA/OptcsvGazeboFiles/feedback_data.csv'  # Path to the output CSV file
    # Send the joint trajectory command and capture feedback
    send_joint_trajectory_command(feedback_file_path) 

