from polling_data import get_data
import analytics
from write_data import *
import end_formatting
import os


def command_runner(file_path):
    #this is for testing so I don't have to find the file every time
    #file_path = os.path.join('Downloads','Polling-Tester.csv')
    #file_path = os.path.join('Downloads', 'complete_09_12_24_data.csv')

    #get_data is imported from polling_data and returns a list of Individuals (class)
    data = get_data(file_path)

    #runs command below with list of Individuals
    submit(data)


def submit(data):
    #data_display is the string that is being written to the end polling data

    #adds the basic Overall|Response1|Response2 etc
    data_display = str(analytics.default_constructor(data))

    data_display = end_formatting.write_all_reg_data(data, data_display)

    #PARTY SPECIFIC DATA FROM THIS POINT ON

    data_display = end_formatting.write_all_party_data(data, data_display)

    #displays the data that will eventually be written to the file (TESTING)
    #print(data_display)
    writeData(data_display)
downloads = os.path.expanduser('Downloads')
retrievalPath = os.path.join(downloads,'raw_pulse_data')
outputPath = os.path.join(downloads, 'csv-data')
clearDirectory(outputPath)
count = 0
for filename in os.listdir(retrievalPath):
    if filename != '.DS_Store':
        command_runner(os.path.join(retrievalPath,filename))
        count += 1
print(count)
