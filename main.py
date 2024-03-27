import PlaygroundData.FixerData as pdata

fdrh = pdata.FixerDataRequestHandler()
data = fdrh.get_data({"start_date": "2022-01-01",
                      "end_date": "2022-09-11",
                      "from_curr": "USD",
                      "to_curr": "GBP"})
print(data)

