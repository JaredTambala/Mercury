import json

import pandas as pd
import pytest

from PlaygroundData import FixerDataFormatter


@pytest.fixture()
def forex_data():
    with open('./tests/fixer_api_response.json') as json_file:
        data = json.load(json_file)
    return data


class TestFixerDataFormatter:

    def test_exception_when_base_missing(self, forex_data):
        with pytest.raises(KeyError) as excinfo:
            del forex_data["base"]
            FixerDataFormatter.input_format({"data": forex_data})
        assert "base" in str(excinfo.value)

    def test_exception_when_rates_missing(self, forex_data):
        with pytest.raises(KeyError) as excinfo:
            del forex_data["rates"]
            FixerDataFormatter.input_format({"data": forex_data})
        assert "rates" in str(excinfo.value)

    def test_format_correct_json(self, forex_data):
        output = FixerDataFormatter.input_format({"data": forex_data})
        expected_output = pd.read_csv(r'./tests/formatted.csv')
        pd.testing.assert_frame_equal(expected_output, output)
