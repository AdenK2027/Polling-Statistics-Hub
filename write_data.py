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

def clearDirectory(path):
    # Check if the directory exists
    if os.path.exists(path):
        # Iterate through all files and subdirectories in the directory
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            # Check if it's a file and remove it
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)  # Removes the file or symlink
    else:
        print(f"Directory '{path}' does not exist.")

def writeData(data):
    try:
        # "Desktop","Poll-Results.csv"
        #"polling-statistics","files","Poll-Results.csv"
        downloads_folder = os.path.expanduser("~/Downloads")

        #REMOVE BEFORE SENDING TO NICK!!!
        downloads_folder = os.path.join(downloads_folder, 'csv-data')

        with open(os.path.join(downloads_folder,f"{get_question()}-Polling Results.csv"), 'wt') as fin:
            writer = csv.writer(fin, delimiter='|')
            list_data = stringToCSVList(data)
            writer.writerows(list_data)
            #fin.writelines([data])
            print(f"Successfully Written Data to Downloads as {get_question()}-Polling Results.csv")
    except FileNotFoundError as e:
        print('File not found', e)

def CustomCapitalization(line):
    result = ''
    count = 0
    for i in range(len(line)-1):
        if (i == 0):
            result += line[0].upper()
        elif (line[i-1] == '|' or line[i-1] == ' ') or (line[i-1] == '.' and line[i+1] == ' ') and count < 8:
            result += line[i].upper()
        else:
            result += line[i]
        if line[i] == '|':
            count += 1
    result += line[len(line)-1]
    return result

def writeFormattedData(filePath,data):
    try:
        # "Desktop","Poll-Results.csv"
        #"polling-statistics","files","Poll-Results.csv"
        downloads_folder = os.path.expanduser("~/Downloads")

        #REMOVE BEFORE SENDING TO NICK!!!
        #downloads_folder = os.path.join(downloads_folder, 'csv-data')

        with open(os.path.join(filePath[:-4]) + '-formatted.csv', 'wt') as fin:
            writer = csv.writer(fin, delimiter='|')
            formattedLines = []
            for person in data:
                birthdate = str(person.birthdate)[1:-1].split(',')
                for i in range(len(birthdate)):
                    if birthdate[i][0] == " ":
                        birthdate[i] = birthdate[i][1:]
                birthdate = "/".join(birthdate)
                email = person.email
                if 'example' in email:
                    email = "No Email"
                finalLine = (f"{email}|{birthdate}|{person.party}|{person.affiliation}|{person.office}"
                      f"|{person.gender}|{person.field}|{get_question()}|{person.response}")
                finalLine = CustomCapitalization(finalLine)
                formattedLines.append(finalLine)
            writer.writerow(['Email', 'Birthdate', 'Party', 'Affiliation', 'Office', 'Gender', 'Field',
                             'Question', 'Answer'])
            for line in formattedLines:
                writer.writerow(line.split('|'))
        print(f"Successfully Written Formatting to Downloads as {filePath[:-4]}-formatted.csv")
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
