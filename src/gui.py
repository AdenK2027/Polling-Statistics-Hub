import tkinter as tk
from tkinter import filedialog
from polling_data import get_data
import analytics
from write_data import *
import end_formatting


#BROWSE FILE BOX
def open_file_dialog():
    global file_path
    # Set the default folder to Downloads
    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")

    # Open a file dialog with Downloads folder as default
    file_path = filedialog.askopenfilename(title="Select a file",
                                           initialdir=downloads_folder,
                                           filetypes=(("CSV files", "*.csv"),))
    if file_path:
        # Display and enable the execute button once a file path is selected
        execute_button.config(text=f"Execute", state=tk.NORMAL)
        # data = get_data(file_path)
        # for person in data:
        #     person.dump()
        #     print()

# Create the main Tkinter window
win = tk.Tk()
win.title("Polling Data Organizer")

# Create a button to open the file dialog
open_file_button = tk.Button(win, text="Open File", command=open_file_dialog)
open_file_button.pack(pady=10)


#runs when the execute button is pressed (gets around no using parameters in button funcs)
def command_runner():
    #this is for testing so I don't have to find the file every time
    #file_path = os.path.join('Downloads','Polling-Tester.csv')
    #file_path = os.path.join('Downloads', 'complete_09_12_24_data.csv')

    #get_data is imported from polling_data and returns a list of Individuals (class)
    data = get_data(file_path)

    #runs command below with list of Individuals
    submit(data)

#DISABLED FOR NOW
# def save_location_setter():
#     set_file_button.config(state=tk.DISABLED)
#     set_file_path(set_file_button)

#DISABLED FOR NOW
# set_file_button = tk.Button(win, text="Set Save Path", command=save_location_setter)
# set_file_button.pack(pady=10)

#Execute button that starts disabled and is enabled when file is selected
execute_button = tk.Button(win, text="No file selected", state=tk.DISABLED, command=command_runner)
execute_button.pack(pady=10)


def submit(data):
    #data_display is the string that is being written to the end polling data

    #adds the basic Overall|Response1|Response2 etc
    data_display = str(analytics.default_constructor(data))

    data_display = end_formatting.write_all_reg_data(data,data_display)

    #PARTY SPECIFIC DATA FROM THIS POINT ON

    data_display = end_formatting.write_all_party_data(data,data_display)

    #displays the data that will eventually be written to the file (TESTING)
    #print(data_display)
    writeData(data_display)

    #this will close the text box after inputing a file and hitting execute
    win.destroy()

#this is just for testing (runs code with predestined file path instantly)
#command_runner()

#starts the gui
win.mainloop()