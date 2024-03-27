from .FixerDataFormatter import FixerDataFormatter
from .FixerDataStoreHandler import FixerDataStoreHandler
from PlaygroundData.AbstractData import DataService

class FixerDataService(DataService):

    def __init__(self):
        super().__init__()
        pass

    def save_data_to_store(self, data):
        fdsh = FixerDataStoreHandler()
        fdsh.open_connection()
        fdsh.save_query({"data": data})
        fdsh.close_connection()
        return

    def format_data(self, data):
        format_df = FixerDataFormatter.input_format({"data": data})
        return format_df
