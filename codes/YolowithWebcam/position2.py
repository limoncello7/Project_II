import math

# Robot parameters
base_height = 6  # Base height (cm)
rArm_length = 9.5  # Length of the rear arm (cm)
fArm_claw_length = 18  # Length of the front arm plus claw (cm)
base_rotation_range = (0, 180)  # Range of base rotation (degrees)
base_rArm_joint_range = (45, 180)  # Range of rotation at the base-rear arm joint (degrees)
rArm_fArm_joint_range = (35, 120)  # Range of rotation at the rear arm-front arm joint (degrees)

def adjust_angles_to_range(x, y):
    z = 3  # Final height of the mechanical claw
    
    # Calculate base rotation angle
    base_rotation_angle = math.degrees(math.atan2(y, x))
    if base_rotation_angle < 0:
        base_rotation_angle += 360  # Normalize angle to [0, 360)
    
    # Ensure base rotation angle is within the range
    base_rotation_angle = min(max(base_rotation_angle, base_rotation_range[0]), base_rotation_range[1])
    
    # Calculate the horizontal projection length
    projection_length = math.sqrt(x**2 + y**2)
    
    # Calculate angle of inclination at the base-rear arm joint
    base_rArm_joint_angle = math.degrees(math.atan2(z - base_height, projection_length))
    
    # Adjust base to rear arm joint angle if out of range and calculate the best effort for rear to front arm joint angle
    if base_rArm_joint_angle < base_rArm_joint_range[0]:
        base_rArm_joint_angle = base_rArm_joint_range[0]  # Set to minimum range value if below
        # Calculate the new angle for rear arm to front arm joint, attempting to reach the target
        # This is a simplified approach and may need refinement for accuracy
        delta_z = rArm_length * math.sin(math.radians(base_rArm_joint_angle)) + fArm_claw_length * math.sin(math.radians(rArm_fArm_joint_range[0])) - (z - base_height)
        new_projection_length = rArm_length * math.cos(math.radians(base_rArm_joint_angle)) + fArm_claw_length * math.cos(math.radians(rArm_fArm_joint_range[0]))
        rArm_fArm_joint_angle = math.degrees(math.atan2(delta_z, new_projection_length))
    else:
        # If base to rear arm joint angle is within range, calculate rear to front arm joint angle normally
        cos_angle = (rArm_length**2 + fArm_claw_length**2 - projection_length**2 - (z - base_height)**2) / (2 * rArm_length * fArm_claw_length)
        cos_angle = max(min(cos_angle, 1), -1)  # Ensure the value is within [-1, 1]
        rArm_fArm_joint_angle = math.degrees(math.acos(cos_angle))
    
    return base_rotation_angle, base_rArm_joint_angle, rArm_fArm_joint_angle

x = float(input("Enter x coordinate: "))
y = float(input("Enter y coordinate: "))

angles = adjust_angles_to_range(x, y)
print(f"Base rotation angle: {angles[0]:.2f} degrees")
print(f"Base to rear arm joint angle: {angles[1]:.2f} degrees")
print(f"Rear arm to front arm joint angle: {angles[2]:.2f} degrees")
