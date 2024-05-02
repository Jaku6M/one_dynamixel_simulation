import xml.etree.ElementTree as ET
import os
import sys

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
    # Change directory to ~/Humanoid_workspace and build the specific package
    workspace_dir = os.path.expanduser('~/Humanoid_workspace')
    if os.path.isdir(workspace_dir):
        os.chdir(workspace_dir)
        # Run colcon build command for the specified package
        command = 'colcon build --packages-select one_dynamixel_simulation'
        os.system(command)
        print(f"Built package 'one_dynamixel_simulation' in {workspace_dir}.")
    else:
        print(f"Error: Workspace directory not found at {workspace_dir}.")

# # Przykładowe wywołanie funkcji z wartościami z MATLABa
# xml_file_path = '/home/jaku6m/Humanoid_workspace/src/one_dynamixel_simulation/urdf/MX28AR.xacro'
# change_xml_values(xml_file_path, damping_value=0.2, friction_value=0.2, spring_stiffness_value=1.0, spring_reference_value=0.01)
# print(f"Zmieniono wartosci w pliku {xml_file_path}.")

if __name__ == "__main__":
    # Retrieve parameters from command line arguments
    damping_value = float(sys.argv[1])
    friction_value = float(sys.argv[2])
    spring_stiffness_value = float(sys.argv[3])
    spring_reference_value = float(sys.argv[4])

    # Specify the path to the XML file
    xml_file_path = '/home/jaku6m/Humanoid_workspace/src/one_dynamixel_simulation/urdf/MX28AR.xacro'

    # Call the function to change XML values with received parameters
    change_xml_values(xml_file_path, damping_value, friction_value, spring_stiffness_value, spring_reference_value)

    print(f"Changed values in file {xml_file_path}.")