import os
import subprocess
import time
import json
import csv

def launch_gazebo_simulation():
    # Open a new terminal and launch Gazebo simulation
    subprocess.Popen(['gnome-terminal', '--', 'ros2', 'launch', 'one_dynamixel_simulation', 'MX28AR_gazebo.launch.py'])

def send_joint_trajectory_command():
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

    subprocess.Popen(['gnome-terminal', '--','ros2', 'action', 'send_goal', '/joint_trajectory_controller/follow_joint_trajectory', 'control_msgs/action/FollowJointTrajectory', '-f', trajectory_json])

def extract_feedback_data(feedback_text):
    # Initialize variables to store extracted data
    time_sec = None
    positions = None
    velocities = None

    # Split the feedback text into lines
    lines = feedback_text.strip().split('\n')

    # Parse each line to extract relevant information
    for line in lines:
        line = line.strip()
        if line.startswith('sec:'):
            time_sec = int(line.split(':')[-1].strip())
        elif line.startswith('positions:'):
            positions = [float(value.strip()) for value in line.split(':')[-1].split()]
        elif line.startswith('velocities:'):
            velocities = [float(value.strip()) for value in line.split(':')[-1].split()]

    return time_sec, positions, velocities

def save_feedback_data_to_csv(feedback_file_path, output_csv_file):
    with open(feedback_file_path, 'r') as feedback_file, open(output_csv_file, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Time (sec)', 'Position', 'Velocity'])

        feedback_text = feedback_file.read()
        feedback_blocks = feedback_text.strip().split('\n\nFeedback:\n    ')

        for feedback_block in feedback_blocks:
            time_sec, positions, velocities = extract_feedback_data(feedback_block)
            if time_sec is not None and positions is not None and velocities is not None:
                csv_writer.writerow([time_sec, positions[0], velocities[0]])

if __name__ == '__main__':
    launch_gazebo_simulation()
    send_joint_trajectory_command()
    time.sleep(10)
    feedback_file_path = '/home/jaku6m/Desktop/OPTYMALIZACJA/OptcsvGazeboFiles/output_file.txt'  # Path to the feedback text file
    output_csv_file = '/home/jaku6m/Desktop/OPTYMALIZACJA/OptcsvGazeboFiles/feedback_data.csv'  # Path to the output CSV file
    save_feedback_data_to_csv(feedback_file_path, output_csv_file)