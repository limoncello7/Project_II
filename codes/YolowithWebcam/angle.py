import math

# Robot parameters
base_height = 6  # Base height (cm)
rArm_length = 9.5  # Length of the rear arm (cm)
fArm_claw_length = 18  # Length of the front arm plus claw (cm)
base_rotation_range = (-90, 90)  # Range of base rotation (degrees)
base_rArm_joint_range = (45, 180)  # Range of rotation at the base-rear arm joint (degrees)
rArm_fArm_joint_range = (35, 120)  # Range of rotation at the rear arm-front arm joint (degrees)

def calculate_coordinates(angles):
    base_rotation_angle, base_rArm_joint_angle, rArm_fArm_joint_angle = angles

    # Convert angles to radians
    base_rotation_angle_rad = math.radians(base_rotation_angle)
    base_rArm_joint_angle_rad = math.radians(base_rArm_joint_angle)
    rArm_fArm_joint_angle_rad = math.radians(rArm_fArm_joint_angle)

    # Calculate coordinates
    # x is the forward distance of the robot arm when base rotation angle = 90 degrees
    x = rArm_length * math.sin(base_rotation_angle_rad) + fArm_claw_length * math.sin(base_rotation_angle_rad + base_rArm_joint_angle_rad)
    # y is the distance to the right of the robot
    y = rArm_length * math.cos(base_rotation_angle_rad) + fArm_claw_length * math.cos(base_rotation_angle_rad + base_rArm_joint_angle_rad)
    # z is the height of the claw
    z = base_height + fArm_claw_length * math.sin(rArm_fArm_joint_angle_rad)
    
    return x, y, z

# Input angles
base_angle = float(input("Enter base rotation angle ((-)90-90 degrees): "))
base_rArm_angle = float(input("Enter angle at base-rear arm joint (45-180 degrees): "))
rArm_fArm_angle = float(input("Enter angle at rear arm-front arm joint (35-120 degrees): "))

# Check if angles are within the allowed range
if not (base_rotation_range[0] <= base_angle <= base_rotation_range[1] and
        base_rArm_joint_range[0] <= base_rArm_angle <= base_rArm_joint_range[1] and
        rArm_fArm_joint_range[0] <= rArm_fArm_angle <= rArm_fArm_joint_range[1]):
    print("The input angles are out of the allowed range. Please input again.")
else:
    angles = (base_angle, base_rArm_angle, rArm_fArm_angle)
    x, y, z = calculate_coordinates(angles)
    print("The corresponding XYZ coordinates are:")
    print("X: {:.2f}".format(x))
    print("Y: {:.2f}".format(y))
    print("Z: {:.2f}".format(z))
