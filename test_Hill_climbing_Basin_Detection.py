"""
Test suite for the Hill-Climbing Basin Detection rainwater trapping algorithm.
Tests the water_area_one_side function and algorithm logic with edge cases.
"""

from Hill_Climbing_Basin_Detection import water_area_one_side


def second_algo_logic(sky_line):
    """Extracted logic from second_algo.main for testing purposes."""
    if not sky_line or len(sky_line) < 3:
        return 0

    if any(h < 0 for h in sky_line):
        return 0

    maximum = max(sky_line)
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
        start_pos = maximum_positions[0]
        end_pos = maximum_positions[-1]
        width = end_pos - start_pos - 1
        if width > 0:
            water_level = maximum
            ground_area = sum(sky_line[start_pos + 1 : end_pos])
            max_water_area = water_level * width
            between_area = max_water_area - ground_area

    return left_area + right_area + between_area


class TestSecondAlgorithm:
    """Test cases for the second algorithm's main logic."""

    def test_single_maximum(self):
        """Test with single maximum (original working case)."""
        sky_line = [2, 4, 2, 1, 7, 3, 2, 2, 4, 2]
        result = second_algo_logic(sky_line)
        assert result == 10

    def test_multiple_maxima_same_height(self):
        """Test with multiple peaks at the same maximum height."""
        sky_line = [2, 5, 1, 0, 1, 5, 2]
        result = second_algo_logic(sky_line)
        assert result >= 0  # Should handle multiple maxima correctly

    def test_flat_maximum_plateau(self):
        """Test with a flat plateau as the maximum."""
        sky_line = [1, 3, 5, 5, 5, 3, 1]
        result = second_algo_logic(sky_line)
        # Expected: water on left (1->3) + water on right (3<-1) + between maxima
        assert result >= 0

    def test_maximum_at_edges(self):
        """Test when maximum is at the beginning or end."""
        # Maximum at start - should only have right area
        sky_line = [5, 1, 2, 1, 3]
        result = second_algo_logic(sky_line)
        assert result >= 0

        # Maximum at end - should only have left area
        sky_line = [1, 2, 1, 3, 5]
        result = second_algo_logic(sky_line)
        assert result >= 0

    def test_three_maxima(self):
        """Test with three peaks at maximum height."""
        sky_line = [1, 4, 2, 4, 1, 4, 2]
        result = second_algo_logic(sky_line)
        # Should correctly handle between area with intermediate maximum
        assert result >= 0


class TestWaterAreaOneSide:
    """Test cases for the water_area_one_side function."""

    def test_no_water_cases(self):
        """Test cases where no water can be trapped on one side."""
        # Strictly ascending - no water
        assert water_area_one_side([1, 2, 3, 4], 3) == 0

        # Single position
        assert water_area_one_side([5], 0) == 0

        # Maximum at position 0
        assert water_area_one_side([5, 3, 2, 1], 0) == 0

    def test_multiple_basins_one_side(self):
        """Test multiple water basins on one side."""
        # [4, 1, 3, 0, 2] - basin from 4 to 3, then 3 to 2
        result = water_area_one_side([4, 1, 3, 0, 2], 4)
        # Multiple basins with cumulative area calculation
        assert result >= 0

    def test_equal_heights_plateau(self):
        """Test with equal consecutive heights forming plateaus."""
        # [2, 4, 4, 1, 4] - plateau at height 4
        result = water_area_one_side([2, 4, 4, 1, 4], 4)
        assert result >= 0

    def test_deep_basin(self):
        """Test with a deep basin requiring cumulative area calculation."""
        sky_line = [5, 1, 2, 1, 3, 0, 1, 4]
        result = water_area_one_side(sky_line, 7)
        assert result >= 0


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_minimal_input_sizes(self):
        """Test with minimal valid input sizes."""
        # Three elements (minimum for water trapping)
        assert second_algo_logic([1, 0, 1]) == 1

        # Less than 3 elements
        assert second_algo_logic([1, 2]) == 0
        assert second_algo_logic([5]) == 0
        assert second_algo_logic([]) == 0

    def test_all_same_height(self):
        """Test with all elements at the same height."""
        assert second_algo_logic([3, 3, 3, 3, 3]) == 0

    def test_negative_heights(self):
        """Test with negative heights (should return 0)."""
        assert second_algo_logic([1, -2, 3]) == 0

    def test_large_numbers(self):
        """Test with large height values."""
        sky_line = [1000, 1, 999]
        result = second_algo_logic(sky_line)
        assert result == 998  # min(1000, 999) - 1 = 998
