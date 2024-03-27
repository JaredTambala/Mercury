import json
import pandas as pd
from PlaygroundData.AbstractData import DataFormatter

class FixerDataFormatter(DataFormatter):

    def __init__(self):
        pass

    @staticmethod
    def input_format(opt):

        json_data = opt["data"]
        # get base curr
        base_curr = json_data['base']
        # get to curr
        to_curr = list(json_data['rates'][list(json_data['rates'].keys())[0]].keys())[0]
        # loop through rates and add each key-value to lists
        curr_pair = f"{base_curr}{to_curr}"
        format_dict = {"Date": [],
                       curr_pair: []
                       }
        for date, rate_dict in json_data['rates'].items():
            format_dict['Date'].append(date)
            rate = list(rate_dict.values())[0]
            format_dict[curr_pair].append(rate)

        format_df = pd.DataFrame(format_dict)
        return format_df


    @staticmethod
    def output_format(opt):
        pass

