import math

# Robot parameters
base_height = 6  # Base height (cm)
rArm_length = 9.5  # Length of the rear arm (cm)
fArm_claw_length = 18  # Length of the front arm plus claw (cm)

def calculate_angles(coordinates):
    x, y = coordinates
    z = 3  # Default z = 3 (cm)

    # Calculate base rotation angle
    base_rotation_angle = math.degrees(math.atan2(y, x))

    # Calculate the horizontal projection length of the robot
    projection_length = math.sqrt(x**2 + y**2)

    # Calculate the angle of inclination at the base-rear arm joint
    projection_angle = abs(math.degrees(math.atan2(z - base_height, projection_length)))
    #calculate the distance from the base to the target point
    length=math.sqrt((z - base_height)**2 + projection_length**2)
    #through length of the 2arms and distance to form a triangle calculate all the 3 angles
    alpha=math.degrees(math.acos((rArm_length**2 + fArm_claw_length**2 - length**2)/(2*rArm_length*fArm_claw_length)))
    beta=math.degrees(math.acos((fArm_claw_length**2 + length**2 - rArm_length**2)/(2*fArm_claw_length*length)))
    gamma=math.degrees(math.acos((rArm_length**2 + length**2 - fArm_claw_length**2)/(2*rArm_length*length)))
    base_rArm_joint_angle=gamma-projection_angle
    rArm_fArm_joint_angle= alpha
    
    return base_rotation_angle, base_rArm_joint_angle, rArm_fArm_joint_angle


# Input coordinates
coordinates = tuple(map(float, input("Enter coordinates (x, y) (separated by comma): ").split(',')))

# Calculate angles
angles = calculate_angles(coordinates)

# Output the result
# if angles is not None:
#     print("c100")
#     base_angle, base_rArm_angle, rArm_fArm_angle = angles
#     print("b", base_angle)
#     print("r", base_rArm_angle)
#     print("f", rArm_fArm_angle)
#     print("c30")