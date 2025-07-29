"""
Hill-Climbing Basin Detection rainwater trapping algorithm.
Processes from both ends toward the global maximum for O(n) efficiency.
Measures water basins while "running up the hill" toward the peak.
"""


def calculate_area(
    area_function: list[int], position: int, left_position: int, left_wall: int
) -> int:
    """Calculate water area in a basin using cumulative ground area.

    Args:
        area_function: Cumulative sum of ground heights
        position: Current position (right boundary)
        left_position: Left boundary position
        left_wall: Height of left boundary (water level)

    Returns:
        Water area trapped in this basin
    """
    # Calculate width - if no width, no water area
    width = position - left_position - 1
    if width <= 0:
        return 0

    # Calculate area
    mountain_area = area_function[position] - area_function[left_position + 1]
    upper_area = left_wall * width
    water_area = upper_area - mountain_area

    return water_area


def water_area_one_side(sky_line: list[int], maximum_position: int) -> int:
    """Calculate water trapped from one side up to a maximum position.

    Uses a single-pass algorithm tracking the highest "left wall" seen so far.
    When we encounter a higher or equal peak, we can calculate trapped water.

    Args:
        sky_line: List of heights
        maximum_position: Stop processing at this position

    Returns:
        Total water area trapped from start to maximum_position
    """
    left_wall: int = sky_line[0]
    left_position: int = 0
    in_basin = False
    ground_area_function = [
        0,
    ]
    water_area = 0
    for position, height in enumerate(sky_line):
        if position == maximum_position:
            if in_basin:
                water_area += calculate_area(
                    ground_area_function, position, left_position, left_wall
                )
            break
        total_area = ground_area_function[-1] + height
        ground_area_function.append(total_area)
        if left_wall <= height:
            if in_basin:
                # Calculate area
                water_area += calculate_area(
                    ground_area_function, position, left_position, left_wall
                )

            left_wall = height
            left_position = position
            in_basin = False
            continue

        elif left_wall > height:
            in_basin = True

    return water_area


def main():
    sky_line = [2, 4, 0, 7, 1, 4, 2]

    # Input validation
    if not sky_line or len(sky_line) < 3:
        print("Error: Need at least 3 positions to calculate water area")
        return 0

    if any(h < 0 for h in sky_line):
        print("Error: All heights must be non-negative")
        return 0

    maximum = max(sky_line)
    # Find all positions with maximum height
    maximum_positions = [i for i, h in enumerate(sky_line) if h == maximum]

    # Area to the left of the maximum

    left_area = water_area_one_side(sky_line, maximum_positions[0])

    # Area to the right of the maximum

    right_line = sky_line[maximum_positions[-1] :]
    right_line.reverse()
    right_position = len(right_line) - 1

    right_area = water_area_one_side(right_line, right_position)

    # Area between maxima (if multiple maxima exist)
    between_area = 0
    if len(maximum_positions) > 1:
        # Calculate water trapped between first and last maximum
        start_pos = maximum_positions[0]
        end_pos = maximum_positions[-1]
        width = end_pos - start_pos - 1
        if width > 0:
            # Water level is the maximum height
            water_level = maximum
            ground_area = sum(sky_line[start_pos + 1 : end_pos])
            max_water_area = water_level * width
            # ground_area already includes intermediate maxima, so no need to subtract them again
            between_area = max_water_area - ground_area

    water_area = left_area + right_area + between_area

    print(f"Water area (Hill-Climbing Basin Detection): {water_area}")
    return water_area


if __name__ == "__main__":
    main()
