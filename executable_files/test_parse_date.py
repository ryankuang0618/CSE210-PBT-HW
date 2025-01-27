import importlib.util
from hypothesis import given, strategies as st
from datetime import date
import pytest

pyc_path = "../__encoded_files__/q2.encoded.pyc"
spec = importlib.util.spec_from_file_location("", pyc_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

# Strategy to generate valid dates
def valid_date_strategy():
    return st.dates(min_value=date(1, 1, 1), max_value=date(9999, 12, 31)).map(
        lambda d: d.strftime("%m/%d/%Y")
    )

# Strategy to generate invalid dates
def invalid_date_strategy():
    return st.one_of(
        st.text(min_size=1, max_size=50).filter(
            lambda x: not (len(x.split("/")) == 3 and all(part.isdigit() for part in x.split("/")))
        ),  # Generates non-date-like strings
        st.just(""),
        st.just(None),
        st.just("hello"),
        st.just("123/abc/456"),
        st.just("12-31-2021"),  # Incorrect separator
        st.just("13/31/2021"),  # Invalid month
        st.just("12/32/2021"),  # Invalid day
        st.just("12/00/2021"),  # Invalid day (0)
        st.just("00/31/2021"),  # Invalid month (0)
    )

# Test: Valid dates should return a parsed date object or similar
@given(date_str=valid_date_strategy())
def test_valid_dates(date_str):
    result = module.parse_date(date_str)
    assert result is not None, f"Expected valid date, got {result}"

# Test: Invalid dates should raise an error or return None
@given(date_str=invalid_date_strategy())
def test_invalid_dates(date_str):
    try:
        result = module.parse_date(date_str)
        assert result is None, f"Expected failure for invalid date, got {result}"
    except Exception:
        pass 

# Test: Ensure parsing rejects empty strings
@given(date_str=st.just(""))
def test_empty_string(date_str):
    result = module.parse_date(date_str)
    assert result is None, "Expected None for empty string"

# Test: Ensure parsing rejects None
@given(date_str=st.just(None))
def test_none_input(date_str):
    try:
        result = module.parse_date(date_str)
        assert result is None, "Expected None for None input"
    except Exception:
        pass 

# Test: Ensure parsing rejects non-date text
@given(date_str=st.just("hello"))
def test_non_date_text(date_str):
    result = module.parse_date(date_str)
    assert result is None, "Expected None for non-date text"

# Test: Ensure parsing rejects incorrect separators
@given(date_str=st.just("12-31-2021"))
def test_incorrect_separator(date_str):
    result = module.parse_date(date_str)
    assert result is None, "Expected None for incorrect separators"

# Test: Ensure parsing handles invalid months or days
@given(date_str=st.sampled_from(["13/31/2021", "12/32/2021", "12/00/2021", "00/31/2021"]))
def test_invalid_month_day(date_str):
    result = module.parse_date(date_str)
    assert result is None, f"Expected None for invalid month/day, got {result}"

# Test: Parsing leap year dates
@given(date_str=st.sampled_from(["02/29/2000", "02/29/2024", "02/29/2400"]))
def test_leap_year_dates(date_str):
    result = module.parse_date(date_str)
    assert result is not None, f"Expected valid leap year date, got {result}"

# Test: Reject invalid leap year dates
@given(date_str=st.sampled_from(["02/29/1900", "02/29/2021", "02/29/2100"]))
def test_invalid_leap_year_dates(date_str):
    result = module.parse_date(date_str)
    assert result is None, f"Expected None for invalid leap year date, got {result}"

# Test: Handle leading zeros in date components
@given(date_str=st.sampled_from(["01/01/2021", "09/09/2021", "03/04/0001"]))
def test_dates_with_leading_zeros(date_str):
    result = module.parse_date(date_str)
    assert result is not None, f"Expected valid date with leading zeros, got {result}"

# Test: Handle trailing whitespaces
@given(date_str=st.sampled_from(["01/01/2021 ", " 01/01/2021", "01/01/2021   "]))
def test_dates_with_whitespace(date_str):
    result = module.parse_date(date_str)
    assert result is not None, f"Expected valid date with trailing/leading whitespaces, got {result}"

# Test: Reject year outside valid range
@given(date_str=st.sampled_from(["01/01/0000", "01/01/10000", "01/01/-100"]))
def test_invalid_year_range(date_str):
    result = module.parse_date(date_str)
    assert result is None, f"Expected None for year out of range, got {result}"

# Test: Handle very large invalid inputs
@given(date_str=st.text(min_size=1000, max_size=5000))
def test_large_invalid_inputs(date_str):
    result = module.parse_date(date_str)
    assert result is None, f"Expected None for large invalid input, got {result}"

# Test: Reject partial dates
@given(date_str=st.sampled_from(["01/2021", "01/", "/2021", "01", "2021"]))
def test_partial_dates(date_str):
    result = module.parse_date(date_str)
    assert result is None, f"Expected None for partial date, got {result}"

# Test: Reject dates with extra components
@given(date_str=st.sampled_from(["01/01/2021/extra", "01/01/2021 extra", "01/01/2021/"]))
def test_extra_components(date_str):
    result = module.parse_date(date_str)
    assert result is None, f"Expected None for date with extra components, got {result}"

# Test: Dates in alternative formats should be rejected
@given(date_str=st.sampled_from(["2021/12/31", "31/12/2021", "2021-12-31", "31-12-2021"]))
def test_alternative_date_formats(date_str):
    result = module.parse_date(date_str)
    assert result is None, f"Expected None for alternative date formats, got {result}"

# Test: Reject excessively long valid-looking dates
@given(date_str=st.sampled_from(["01/01/2021111111", "12/31/2021222222"]))
def test_excessively_long_dates(date_str):
    result = module.parse_date(date_str)
    assert result is None, f"Expected None for excessively long dates, got {result}"


if __name__ == "__main__":
    pytest.main([__file__])
