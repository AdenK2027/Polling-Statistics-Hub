from polling_data import get_data
import analytics
from write_data import *
import end_formatting
import os

def submit(data, year):
    #data_display is the string that is being written to the end polling data

    #adds the basic Overall|Response1|Response2 etc
    data_display = str(analytics.default_constructor(data))

    data_display = end_formatting.write_all_reg_data(data, data_display)

    #PARTY SPECIFIC DATA FROM THIS POINT ON

    data_display = end_formatting.write_all_party_data(data, data_display)

    #displays the data that will eventually be written to the file (TESTING)
    #print(data_display)
    writeData(data_display, year)
downloads = os.path.expanduser('Downloads')
retrievalPath = os.path.join(downloads,'raw_pulse_data')
outputPath = os.path.join(downloads, 'csv-data')
clearDirectory(outputPath)
years = ['2024','2025']
for year in years:
    count = 0
    for filename in os.listdir(os.path.join(retrievalPath, year)):
        if filename != '.DS_Store':
            filePath = os.path.join(retrievalPath, year, filename)

            data = get_data(filePath, currentYear = year)
            submit(data, year)

            count += 1
    print(f"{year}: {count}")
