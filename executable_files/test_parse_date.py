import importlib.util
from hypothesis import given, strategies as st
from datetime import date
import pytest
from dateutil.parser import parse



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

def check_parse_date(date_str):
    try:
        parsed_date = parse(date_str)
        formatted_date = parsed_date.strftime("%Y-%m-%d")
        return formatted_date
    except ValueError:
        raise ValueError(f"Invalid date format: {date_str}")
    
# Test: Valid dates should return a parsed date object or similar
@given(date_str=valid_date_strategy())
def test_valid_dates(date_str):
    result = module.parse_date(date_str)
    expected = check_parse_date(date_str)
    assert str(result) == str(expected), f"Expected valid date {expected}, got {result}. input date:{date_str}"

# Test: Invalid dates should raise an error or return None
@given(date_str=invalid_date_strategy())
def test_invalid_dates(date_str):
    try:
        result = module.parse_date(date_str)
        assert False, f"Expected Exception for invalid date"
    except Exception:
        pass 

# Test: Parsing leap year dates
@given(date_str=st.sampled_from(["02/29/2000", "02/29/2024", "02/29/2400"]))
def test_leap_year_dates(date_str):
    result = module.parse_date(date_str)
    assert result is not None, f"Expected valid leap year date, got {result}"

# Test: Reject invalid leap year dates
@given(date_str=st.sampled_from(["02/29/1900", "02/29/2021", "02/29/2100"]))
def test_invalid_leap_year_dates(date_str):
    try:
        result = module.parse_date(date_str)
        assert False, f"Expected ValueError for invalid leap year date"
    except ValueError:
        pass 

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
    try:
        result = module.parse_date(date_str)
        assert False, f"Expected ValueError for year out of range"
    except ValueError:
        pass 

# Test: Handle very large invalid inputs
@given(date_str=st.text(min_size=1000, max_size=5000))
def test_large_invalid_inputs(date_str):
    try:
        result = module.parse_date(date_str)
        assert False, f"Expected ValueError for large invalid input"
    except ValueError:
        pass 

# Test: Reject partial dates
@given(date_str=st.sampled_from(["01/2021", "01/", "/2021", "01", "2021"]))
def test_partial_dates(date_str):
    try:
        result = module.parse_date(date_str)
        assert False, f"Expected ValueError for partial date"
    except ValueError:
        pass 

# Test: Reject dates with extra components
@given(date_str=st.sampled_from(["01/01/2021/01", "01/01/2021/"]))
def test_extra_components(date_str):
    try:
        result = module.parse_date(date_str)
        assert False, f"Expected ValueError for date with extra components"
    except ValueError:
        pass 

# Test: Dates in alternative formats should be rejected
@given(date_str=st.sampled_from(["2021/12/31", "31/12/2021", "2021-12-31", "31-12-2021"]))
def test_alternative_date_formats(date_str):
    try:
        result = module.parse_date(date_str)
        assert False, f"Expected ValueError for alternative date formats"
    except ValueError:
        pass 

# Test: Years with large numbers
@given(date_str=st.sampled_from(["01/01/2021111111", "12/31/2021222222"]))
def test_excessively_long_dates(date_str):
    result = module.parse_date(date_str)
    expected = check_parse_date(date_str)
    assert str(result) == str(expected), f"Expected valid date {expected}, got {result}. input date:{date_str}"
    

if __name__ == "__main__":
    pytest.main([__file__])
