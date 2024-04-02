import math

def calculate_robot_arm_angles(x, y):
    # Robot parameters
    base_height = 6  # Base height (cm)
    rArm_length = 9.5  # Length of the rear arm (cm)
    fArm_claw_length = 18  # Length of the front arm plus claw (cm)
    z = 3  # Final height of the mechanical claw

    # Angle ranges
    base_rotation_range = (0, 360)  # Adjusted range of base rotation to [0, 360] degrees for full circular motion
    base_rArm_joint_range = (45, 180)  # Range of rotation at the base-rear arm joint (degrees)
    rArm_fArm_joint_range = (35, 120)  # Range of rotation at the rear arm-front arm joint (degrees)

    # Calculate base rotation angle and normalize
    base_rotation_angle = math.degrees(math.atan2(y, x))
    if base_rotation_angle < 0:
        base_rotation_angle += 360  # Adjust for negative angles to ensure a 0 to 360 range

    # The rest of the calculations remain unchanged
    # Calculate the horizontal and effective distances
    projection_length = math.sqrt(x**2 + y**2)
    effective_length = math.sqrt(projection_length**2 + (z - base_height)**2)

    # Adjust angle calculations based on the effective length
    if effective_length > (rArm_length + fArm_claw_length) or effective_length < abs(rArm_length - fArm_claw_length):
        base_rArm_joint_angle = base_rArm_joint_range[0]  # Move to limit if out of range
        rArm_fArm_joint_angle = rArm_fArm_joint_range[1] if effective_length > (rArm_length + fArm_claw_length) else rArm_fArm_joint_range[0]
    else:
        # Normal angle calculation
        angle_a = math.acos((rArm_length**2 + effective_length**2 - fArm_claw_length**2) / (2 * rArm_length * effective_length))
        angle_b = math.acos((rArm_length**2 + fArm_claw_length**2 - effective_length**2) / (2 * rArm_length * fArm_claw_length))

        base_rArm_joint_angle = math.degrees(angle_a )
        rArm_fArm_joint_angle = math.degrees(angle_b)

    # Apply angle ranges
    base_rArm_joint_angle = max(min(base_rArm_joint_angle, base_rArm_joint_range[1]), base_rArm_joint_range[0])
    rArm_fArm_joint_angle = max(min(rArm_fArm_joint_angle, rArm_fArm_joint_range[1]), rArm_fArm_joint_range[0])
    
    return base_rotation_angle, base_rArm_joint_angle, rArm_fArm_joint_angle

# Example testing code
try:
    x = float(input("Enter x coordinate: "))
    y = float(input("Enter y coordinate: "))
    angles = calculate_robot_arm_angles(x, y)
    print(f"Base rotation angle: {angles[0]:.2f} degrees")
    print(f"Base to rear arm joint angle: {angles[1]:.2f} degrees")
    print(f"Rear arm to front arm joint angle: {angles[2]:.2f} degrees")
except ValueError:
    print("Invalid input. Please enter a numeric value.")
