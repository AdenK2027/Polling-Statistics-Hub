import os
from src.polling_data import question, get_data


file_path = os.path.join("files","Testing-Data.csv")
file_path = os.path.join("files","Example Template - Sheet2.csv")


individuals = get_data(file_path)

for item in individuals:
    item.dump()
    print(individuals.index(item))
    print()
print(question)