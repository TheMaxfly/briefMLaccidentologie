"""
Integration tests for US-06: Validation minute dropdown

Tests verify that:
1. Minute field is a selectbox (not text_input or number_input)
2. Minute dropdown has 61 options (-1, 0-59)
3. All minute options have proper labels
"""

import pytest
from streamlit_lib import reference_loader


pytestmark = pytest.mark.integration


class TestUS06MinuteDropdown:
    """Integration tests for US-06: Minute field dropdown validation"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Load reference data once for all tests."""
        self.ref_data = reference_loader.load_reference_data()

    def test_minute_field_uses_selectbox_in_page_5(self):
        """
        T054: Verify minute field is a selectbox, not text_input

        Given: Page 5 source code
        When: Checking widget type for minute field
        Then: Uses st.selectbox (not st.number_input or st.text_input)
        """
        # Read the page 5 source file
        with open("streamlit_pages/5_Conditions.py", "r") as f:
            source = f.read()

        # Assert: minute uses st.selectbox
        assert "st.selectbox" in source, "Page 5 should use st.selectbox"
        assert 'key="minute_input"' in source, "Should have minute_input key"

        # Assert: minute does NOT use text_input or number_input
        lines = source.split("\n")
        minute_lines = [line for line in lines if "minute" in line.lower()]
        for line in minute_lines:
            assert "st.text_input" not in line, \
                f"Minute should NOT use st.text_input: {line}"
            assert "st.number_input" not in line, \
                f"Minute should NOT use st.number_input: {line}"

    def test_minute_dropdown_has_61_options(self):
        """
        T056: Verify data/ref_options.json includes 61 minute options

        Given: Reference data for minute field
        When: Counting options
        Then: Has exactly 61 options (-1, 0-59)
        """
        minute_options = self.ref_data["minute"]
        assert len(minute_options) == 61, \
            f"Minute should have 61 options (-1 + 0-59), got {len(minute_options)}"

    def test_minute_options_cover_full_range(self):
        """
        Verify minute options cover -1 and 0-59 without gaps

        Given: Reference data for minute field
        When: Checking all code values
        Then: Contains exactly -1, 0, 1, ..., 59
        """
        minute_codes = sorted([opt["code"] for opt in self.ref_data["minute"]])
        expected_codes = [-1] + list(range(0, 60))

        assert minute_codes == expected_codes, \
            f"Minute codes should be [-1, 0, 1, ..., 59], got gaps or extras"

    def test_minute_options_have_labels(self):
        """
        Verify all minute options have non-empty labels

        Given: Reference data for minute field
        When: Checking labels
        Then: All options have non-empty label strings
        """
        for opt in self.ref_data["minute"]:
            assert "label" in opt, f"Option {opt['code']} should have 'label' key"
            assert isinstance(opt["label"], str), \
                f"Option {opt['code']} label should be string"
            assert len(opt["label"]) > 0, \
                f"Option {opt['code']} label should not be empty"

    def test_minute_non_renseigne_is_first_or_last_option(self):
        """
        Verify "-1 — Non renseigné" is at beginning or end for easy access

        Given: Minute dropdown options
        When: Checking position of -1 option
        Then: -1 option is first or last in the list
        """
        minute_options = self.ref_data["minute"]
        codes = [opt["code"] for opt in minute_options]

        assert -1 in codes, "Should have -1 option"

        minus_1_index = codes.index(-1)
        assert minus_1_index == 0 or minus_1_index == len(codes) - 1, \
            "-1 option should be at beginning or end of list for easy access"

    def test_minute_formatted_options_are_parseable(self):
        """
        Verify all minute formatted dropdown options can be parsed back

        Given: Formatted minute dropdown options
        When: Parsing each option
        Then: All produce valid integer codes
        """
        formatted_options = reference_loader.get_dropdown_options(self.ref_data, "minute")
        assert len(formatted_options) == 61

        for option in formatted_options:
            code = reference_loader.parse_dropdown_value(option)
            assert isinstance(code, int), f"Parsed code from '{option}' should be integer"
            assert -1 <= code <= 59, f"Code {code} from '{option}' should be in [-1, 59]"

    def test_minute_selectbox_prevents_invalid_input(self):
        """
        Verify only valid minute values exist in dropdown options

        Given: Minute reference data
        When: Checking all codes
        Then: No values outside [-1, 0-59] range exist
        """
        valid_codes = set([-1] + list(range(0, 60)))
        actual_codes = set(opt["code"] for opt in self.ref_data["minute"])

        # No invalid codes
        invalid = actual_codes - valid_codes
        assert len(invalid) == 0, f"Should have no invalid codes, found: {invalid}"

        # No missing codes
        missing = valid_codes - actual_codes
        assert len(missing) == 0, f"Should have no missing codes, found: {missing}"
