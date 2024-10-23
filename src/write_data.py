import os, csv, tkinter as tk
from polling_data import get_question
from tkinter import filedialog

def get_file_path():
    with open(os.path.join('polling-statistics','files','file_path.txt'), 'rt') as fout:
        file_path = fout.readline()
        if file_path == '':
            set_file_path()
            get_file_path()
        else:
            return file_path
def set_file_path(button):
    def open_directory():
        directory_path = filedialog.askdirectory(
            title="Select a Directory",  # Set the title of the dialog
            initialdir="/"  # Set the initial directory (root in this case)
        )

        if directory_path:
            with open(os.path.join("polling-statistics", "files", "file_path.txt"), 'wt') as fin:
                fin.write(directory_path)
            print('file_path written to ', directory_path)
            root.destroy()
            button.config(state=tk.NORMAL)

    def on_window_close():
        button.config(state=tk.NORMAL)
        root.destroy()  # Actually close the window


    # Set up the main Tkinter window
    root = tk.Tk()
    root.title("Directory Selector")
    # Bind the close event to the on_window_close function
    root.protocol("WM_DELETE_WINDOW", on_window_close)

    # Create a button that opens the directory dialog
    select_dir_button = tk.Button(root, text="Select Directory", command=open_directory)
    select_dir_button.pack(pady=20)

    # Run the Tkinter event loop
    root.mainloop()

def writeData(data):
    try:
        # "Desktop","Poll-Results.csv"
        #"polling-statistics","files","Poll-Results.csv"
        downloads_folder = os.path.expanduser("~/Downloads")
        with open(os.path.join('Downloads',f"{get_question()}-Polling Results.csv"), 'wt') as fin:
            writer = csv.writer(fin, delimiter='|')
            list_data = stringToCSVList(data)
            writer.writerows(list_data)
            #fin.writelines([data])
            print(f"Successfully Written Data to Downloads as {get_question()}-Polling Results.csv")
    except FileNotFoundError as e:
        print('File not found', e)


def stringToCSVList(string):
    temp_str = ''
    index = 0
    result = [[]]
    for letter in string:
        if letter == '|':
            result[index].append(temp_str)
            temp_str = ''
        elif letter == '\n':
            result.append([])
            index += 1
        else:
            temp_str += letter
    return result
