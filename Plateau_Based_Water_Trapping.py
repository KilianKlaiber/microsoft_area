"""
Plateau-Based Water Trapping algorithm for rainwater collection.
Regard this list to resemble a sky line of a mountain range. sky_line = [0,2,1,1,3,2,2,4]
Each index in the list is a position and each value resembles an altitude. Imagine that it rains incessantly until the water is collected between
the peaks of the 2D mountain range. Calculate the area that the water covers between the peaks.

Uses a recursive divide-and-conquer approach based on plateau (local maxima) detection.
"""


def find_plateaus(sky_line: list[int]) -> dict[int, int]:
    """
    Water is collected only between local maxima in the mountain range.
    Find all plateaus, i.e. local maxima or saddle points in the mountain range

    Args:
        sky_line: List of non-negative integers representing altitudes at each position.

    Returns:
        dict: position: height of plateaus.

    Raises:
        ValueError: If sky_line contains negative values or non-integer types.
        TypeError: If sky_line is not a list or contains non-numeric values.
    """

    # Input validation
    if not isinstance(sky_line, list):
        raise TypeError("sky_line must be a list")

    if not sky_line:
        return {}

    # Edge case more than 1 local maximum cannot be detected without at least 3 items in sky line.
    if len(sky_line) < 3:
        return {}

    last_position = len(sky_line) - 1

    plateaus: dict[int, int] = {}
    for position, height in enumerate(sky_line):
        # Check for valid altitude values
        if not isinstance(height, (int, float)):
            raise TypeError(
                f"All values must be numeric. Found {type(height).__name__} at position {position}"
            )
        if height < 0:
            raise ValueError(
                f"Negative altitude {height} at position {position}. Altitudes must be non-negative"
            )
        # Identify plateaus
        if position == 0:
            if height > sky_line[1]:
                plateaus[position] = height
        elif position < last_position:
            if height >= sky_line[position - 1] and height >= sky_line[position + 1]:
                plateaus[position] = height
        else:
            if height > sky_line[position - 1]:
                plateaus[position] = height
    return plateaus


def calculate_area(
    sky_line: list[int],
    plateaus: dict[int, int],
    boundary_peak_position: int | None = None,
) -> int:
    """Calculate area covered by water recursively.
    Find the highest and second highest peak among the plateaus and calculate the area between them.
    Repeat the same for the area outside of the range. This is done by use of recursion.

    Args:
        sky_line: List of non-negative integers representing altitudes.
        plateaus: Dictionary mapping positions to heights of local maxima.
        boundary_peak_position: Optional position to use as the highest peak for optimization.

    Returns:
        Integer: Area covered by water.

    Raises:
        ValueError: If plateaus contains invalid position indices or if boundary_peak_position is invalid.
        TypeError: If inputs are of wrong type.
    """

    # Input validation
    if not isinstance(sky_line, list):
        raise TypeError("sky_line must be a list")
    if not isinstance(plateaus, dict):
        raise TypeError("plateaus must be a dictionary")

    # Base case: need at least 2 plateaus to form a basin
    if len(plateaus) < 2:
        return 0

    # Identify location of the two highest peaks within the plateau

    if boundary_peak_position is None:
        highest_peak_position = max(plateaus.keys(), key=lambda k: sky_line[k])
    else:
        highest_peak_position = boundary_peak_position

    second_highest_peak_position = max(
        plateaus.keys(), key=lambda k: sky_line[k] if k != highest_peak_position else 0
    )

    # Identify the height and width of the area between these peaks covered by water
    height = min(
        sky_line[highest_peak_position], sky_line[second_highest_peak_position]
    )
    width = abs(highest_peak_position - second_highest_peak_position) - 1

    # If the width of the area is zero then return zero
    if width <= 0:
        return 0

    # The maximum area is the area that the water would cover if there were no elevation between the peaks.
    max_area = height * width

    # The sub area is the area covered by the elevation between the peaks
    sub_area = 0
    range_start = min(highest_peak_position, second_highest_peak_position)
    range_end = max(highest_peak_position, second_highest_peak_position)

    for position in range(range_start + 1, range_end):
        sub_area += sky_line[position]

    # The center area is the area covered by the water between the peaks.
    center_area = max_area - sub_area

    # Identify the plateaus to the left and right of the center area.
    left_plateaus: dict[int, int] = {}
    right_plateaus: dict[int, int] = {}
    for position in plateaus.keys():
        if position <= range_start:
            left_plateaus[position] = plateaus[position]
        if position >= range_end:
            right_plateaus[position] = plateaus[position]

    # Recursively calculate the area between the highest peaks in the left and right plateaus.
    if len(left_plateaus) > 1:
        left_area = calculate_area(
            sky_line, left_plateaus, boundary_peak_position=range_start
        )
    else:
        left_area = 0

    if len(right_plateaus) > 1:
        right_area = calculate_area(
            sky_line, right_plateaus, boundary_peak_position=range_end
        )
    else:
        right_area = 0

    # Calculate the total area covered by the water.

    total_area = left_area + center_area + right_area

    return total_area


def main():
    print("Plateau-Based Water Trapping Algorithm")

    sky_line = [2, 4, 2, 1, 1, 3, 2, 2, 4, 2]

    # Add validation
    if len(sky_line) < 3:
        print("Error: Need at least 3 positions to calculate water area")
        return

    plateaus = find_plateaus(sky_line)

    area = calculate_area(sky_line, plateaus)

    print(f"Water area (Plateau-Based): {area}")

    return area


if __name__ == "__main__":
    main()
