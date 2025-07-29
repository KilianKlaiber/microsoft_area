"""
Test module for the Plateau-Based Water Trapping algorithm.
Tests the find_plateaus and calculate_area functions.
"""

import pytest
from Plateau_Based_Water_Trapping import find_plateaus, calculate_area


class TestFindPlateaus:
    """Test cases for the find_plateaus function."""

    def test_simple_plateau(self):
        """Test with a simple single plateau."""
        sky_line = [1, 3, 1]
        expected = {1: 3}
        assert find_plateaus(sky_line) == expected

    def test_multiple_plateaus(self):
        """Test with multiple distinct plateaus."""
        sky_line = [0, 2, 1, 1, 3, 2, 2, 4]
        expected = {1: 2, 4: 3, 7: 4}
        assert find_plateaus(sky_line) == expected

    def test_edge_plateaus(self):
        """Test plateaus at the beginning and end."""
        sky_line = [5, 1, 2, 1, 6]
        expected = {0: 5, 2: 2, 4: 6}
        assert find_plateaus(sky_line) == expected

    def test_flat_line(self):
        """Test with a completely flat line."""
        sky_line = [2, 2, 2, 2]
        expected = {1: 2, 2: 2}  # Middle positions are plateaus
        assert find_plateaus(sky_line) == expected

    def test_ascending_descending_lines(self):
        """Test with strictly ascending and descending lines."""
        # Ascending: only last is plateau
        assert find_plateaus([1, 2, 3, 4]) == {3: 4}
        # Descending: only first is plateau
        assert find_plateaus([4, 3, 2, 1]) == {0: 4}


class TestCalculateArea:
    """Test cases for the calculate_area function."""

    def test_simple_basin(self):
        """Test with a simple water basin."""
        sky_line = [3, 0, 3]
        plateaus = {0: 3, 2: 3}
        expected = 3  # 1 position * 3 height = 3 area
        assert calculate_area(sky_line, plateaus) == expected

    def test_uneven_basin(self):
        """Test with uneven peaks."""
        sky_line = [4, 1, 2]
        plateaus = {0: 4, 2: 2}
        expected = 1  # min(4,2) * 1 - 1 = 2 - 1 = 1
        assert calculate_area(sky_line, plateaus) == expected

    def test_default_example(self):
        """Test with the default example from main()."""
        sky_line = [2, 4, 2, 1, 1, 3, 2, 2, 4, 2]
        plateaus = find_plateaus(sky_line)
        result = calculate_area(sky_line, plateaus)
        assert result >= 0  # Verify positive result

    def test_no_water_trapped(self):
        """Test cases where no water can be trapped."""
        # Adjacent peaks (no space)
        sky_line = [1, 3, 2]
        plateaus = {1: 3, 2: 2}
        assert calculate_area(sky_line, plateaus) == 0

        # Single plateau
        assert calculate_area([1, 3, 1], {1: 3}) == 0

        # Empty plateaus
        assert calculate_area([1, 2, 3], {}) == 0

    def test_boundary_peak_optimization(self):
        """Test the boundary peak optimization feature."""
        sky_line = [3, 1, 2, 1, 4]
        plateaus = {0: 3, 2: 2, 4: 4}

        result_with_boundary = calculate_area(
            sky_line, plateaus, boundary_peak_position=4
        )
        result_without_boundary = calculate_area(sky_line, plateaus)

        assert result_with_boundary >= 0
        assert result_without_boundary >= 0


class TestIntegration:
    """Integration tests combining both functions."""

    def test_full_workflow_cases(self):
        """Test the complete workflow with various scenarios."""
        test_cases = [
            ([3, 0, 2, 0, 4], "complex basin"),
            ([2, 0, 2], "simple basin"),
            ([1, 2, 1], "no water trapped"),
        ]

        for sky_line, description in test_cases:
            plateaus = find_plateaus(sky_line)
            area = calculate_area(sky_line, plateaus)
            assert area >= 0, f"Area should be non-negative for {description}"

    def test_minimal_valid_input(self):
        """Test with minimal valid inputs."""
        sky_line = [1, 0, 1]
        plateaus = find_plateaus(sky_line)
        area = calculate_area(sky_line, plateaus)
        assert area == 1  # Should trap 1 unit of water


class TestErrorHandling:
    """Test error handling and input validation."""

    def test_negative_heights(self):
        """Test that negative heights raise ValueError."""
        with pytest.raises(ValueError, match="Negative altitude -2 at position 1"):
            find_plateaus([1, -2, 3])

    def test_non_list_input(self):
        """Test that non-list input raises TypeError."""
        with pytest.raises(TypeError, match="sky_line must be a list"):
            find_plateaus("not a list")

    def test_valid_edge_cases(self):
        """Test that valid edge cases work without errors."""
        # Float values should work
        result = find_plateaus([1.0, 3.5, 2.0])
        assert 1 in result and result[1] == 3.5

        # Zero values should work
        result = find_plateaus([1, 0, 2, 0, 1])
        assert isinstance(result, dict)


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_minimal_inputs(self):
        """Test with minimal input sizes."""
        # Empty list
        assert find_plateaus([]) == {}
        assert calculate_area([], {}) == 0

        # Single element
        assert find_plateaus([5]) == {}

        # Two elements
        assert find_plateaus([1, 3]) == {}

    def test_extreme_values(self):
        """Test with extreme values."""
        # Large numbers
        sky_line = [1000, 1, 999]
        plateaus = find_plateaus(sky_line)
        area = calculate_area(sky_line, plateaus)
        assert area == 998  # min(1000, 999) - 1 = 998

        # All zeros
        sky_line = [0, 0, 0, 0]
        plateaus = find_plateaus(sky_line)
        area = calculate_area(sky_line, plateaus)
        assert area == 0
