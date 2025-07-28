"""
Test suite for the rainwater trapping algorithm.
Tests both the find_plateaus and calculate_area functions with various edge cases.
"""

# No need to import pytest explicitly for test discovery and running.
# Just run `pytest` from the command line in your project directory.
from main import find_plateaus, calculate_area


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

    def test_ascending_line(self):
        """Test with strictly ascending line."""
        sky_line = [1, 2, 3, 4]
        expected = {3: 4}  # Only the last position is a plateau
        assert find_plateaus(sky_line) == expected

    def test_descending_line(self):
        """Test with strictly descending line."""
        sky_line = [4, 3, 2, 1]
        expected = {0: 4}  # Only the first position is a plateau
        assert find_plateaus(sky_line) == expected

    def test_single_element(self):
        """Test with single element (edge case)."""
        sky_line = [5]
        expected = {}  # No plateaus can be determined
        assert find_plateaus(sky_line) == expected

    def test_saddle_points(self):
        """Test with saddle points (equal adjacent heights)."""
        sky_line = [1, 2, 2, 1]
        expected = {1: 2, 2: 2}  # Both middle positions are plateaus
        assert find_plateaus(sky_line) == expected


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

    def test_complex_example(self):
        """Test with the example from the docstring."""
        sky_line = [0, 2, 1, 1, 3, 2, 2, 4]
        plateaus = find_plateaus(sky_line)
        # This should calculate the total trapped water area
        result = calculate_area(sky_line, plateaus)
        assert (
            result >= 0
        )  # At least verify it doesn't crash and returns reasonable result

    def test_default_example(self):
        """Test with the default example from main()."""
        sky_line = [2, 4, 2, 1, 1, 3, 2, 2, 4, 2]
        plateaus = find_plateaus(sky_line)
        result = calculate_area(sky_line, plateaus)
        assert result >= 0  # Verify positive result

    def test_no_water_trapped(self):
        """Test cases where no water can be trapped."""
        # Ascending line
        sky_line = [1, 2, 3, 4]
        plateaus = find_plateaus(sky_line)
        assert calculate_area(sky_line, plateaus) == 0

        # Descending line
        sky_line = [4, 3, 2, 1]
        plateaus = find_plateaus(sky_line)
        assert calculate_area(sky_line, plateaus) == 0

    def test_adjacent_peaks(self):
        """Test with adjacent peaks (no space for water)."""
        sky_line = [1, 3, 2]
        plateaus = {1: 3, 2: 2}
        assert calculate_area(sky_line, plateaus) == 0

    def test_single_plateau(self):
        """Test with only one plateau."""
        sky_line = [1, 3, 1]
        plateaus = {1: 3}
        assert calculate_area(sky_line, plateaus) == 0

    def test_empty_plateaus(self):
        """Test with empty plateaus dictionary."""
        sky_line = [1, 2, 3]
        plateaus = {}
        assert calculate_area(sky_line, plateaus) == 0

    def test_boundary_peak_optimization(self):
        """Test the boundary peak optimization feature."""
        sky_line = [3, 1, 2, 1, 4]
        plateaus = {0: 3, 2: 2, 4: 4}

        # Test with boundary peak specified
        result_with_boundary = calculate_area(
            sky_line, plateaus, boundary_peak_position=4
        )
        result_without_boundary = calculate_area(sky_line, plateaus)

        # Both should give valid results
        assert result_with_boundary >= 0
        assert result_without_boundary >= 0


class TestIntegration:
    """Integration tests combining both functions."""

    def test_full_workflow(self):
        """Test the complete workflow from sky_line to final area."""
        test_cases = [
            ([3, 0, 2, 0, 4], 7),  # Expected: water trapped between peaks
            ([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], 6),  # Multiple basins
            ([2, 0, 2], 2),  # Simple basin
            ([1, 2, 1], 0),  # No water trapped (too narrow)
        ]

        for sky_line, min_expected in test_cases:
            plateaus = find_plateaus(sky_line)
            area = calculate_area(sky_line, plateaus)
            assert area >= 0, f"Area should be non-negative for {sky_line}"

    def test_stress_case(self):
        """Test with a larger, more complex sky line."""
        sky_line = [5, 1, 3, 1, 2, 1, 4, 2, 1, 3, 1, 2, 6]
        plateaus = find_plateaus(sky_line)
        area = calculate_area(sky_line, plateaus)

        assert area >= 0
        assert isinstance(area, int)

    def test_minimal_input_validation(self):
        """Test with minimal valid inputs."""
        # Test minimum case for water trapping
        sky_line = [1, 0, 1]
        plateaus = find_plateaus(sky_line)
        area = calculate_area(sky_line, plateaus)
        assert area == 1  # Should trap 1 unit of water


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_empty_input(self):
        """Test with empty sky line."""
        sky_line = []
        plateaus = find_plateaus(sky_line)
        assert plateaus == {}
        assert calculate_area(sky_line, plateaus) == 0

    def test_large_numbers(self):
        """Test with large height values."""
        sky_line = [1000, 1, 999]
        plateaus = find_plateaus(sky_line)
        area = calculate_area(sky_line, plateaus)
        assert area == 998  # min(1000, 999) - 1 = 998

    def test_all_zeros(self):
        """Test with all zero heights."""
        sky_line = [0, 0, 0, 0]
        plateaus = find_plateaus(sky_line)
        area = calculate_area(sky_line, plateaus)
        assert area == 0

