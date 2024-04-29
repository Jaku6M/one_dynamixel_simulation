import os
import subprocess
import time
import json
import csv
import xml.etree.ElementTree as ET

def launch_gazebo_simulation():
    # Open a new terminal and launch Gazebo simulation
    subprocess.Popen(['gnome-terminal', '--', 'ros2', 'launch', 'one_dynamixel_simulation', 'MX28AR_gazebo.launch.py'])

def send_joint_trajectory_command():
    # Wait for sending the joint trajectory command
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

def save_trajectory_data(feedback_file_path):
    # Open a new process to execute the ROS command and capture output
    with open(feedback_file_path, 'w') as output_file:
        process = subprocess.Popen(
            ['ros2', 'topic', 'echo', '--csv', '/joint_states'],
            stdout=output_file,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

def run_matlab_optimization():
    # Call MATLAB script for dynamic error analysis and optimization
    subprocess.Popen(['gnome-terminal', '--','matlab', '-r', 'run("Optimization.m")'])
    # subprocess.Popen(['gnome-terminal', '--','matlab', '-nodisplay', '-nosplash', '-nodesktop', '-r', 'run("Optimization.m")'])

def change_xml_values(xml_file, damping_value, friction_value, spring_stiffness_value, spring_reference_value):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Modify specific numerical values in <dynamics> elements
    for dynamics in root.iter('dynamics'):
        dynamics.set('damping', str(damping_value))
        dynamics.set('friction', str(friction_value))

    # Modify specific numerical values in <gazebo> elements
    for gazebo in root.iter('gazebo'):
        for spring_stiffness in gazebo.iter('springStiffness'):
            spring_stiffness.text = str(spring_stiffness_value)
        for spring_reference in gazebo.iter('springReference'):
            spring_reference.text = str(spring_reference_value)

    # Save the modified XML file
    tree.write(xml_file)

if __name__ == '__main__':
    # Launch Gazebo simulation
    launch_gazebo_simulation()

    # Wait for simulation to start and send joint trajectory command
    send_joint_trajectory_command()

    # Define output CSV file path
    output_csv_file = '/home/jaku6m/Desktop/OPTYMALIZACJA/OptcsvGazeboFiles/feedback_data.csv'

    # Save trajectory data from simulation
    save_trajectory_data(output_csv_file)

    # Run MATLAB script for dynamic error analysis and optimization
    run_matlab_optimization()

    # Example usage of ChangeVals.py to modify XML file based on optimization results
    xml_file_path = '/home/jaku6m/Humanoid_workspace/src/one_dynamixel_simulation/urdf/MX28AR.xacro'
    change_xml_values(xml_file_path, damping_value=0.3, friction_value=0.3, spring_stiffness_value=1.1, spring_reference_value=0.11)

    #while matlab running == True 
            # if NewParametersCamefromMatlab =1
        #     change_xml_values(xml_file_path, damping_value=0.3, friction_value=0.3, spring_stiffness_value=1.1, spring_reference_value=0.11)
        #     send_joint_trajectory_command()
        #     save_trajectory_data(output_csv_file)
        #     #NewDataArrived =1
            # end
    # end

    print(f"Completed the optimization process.")
