# Clean up csv data for a usable format

# pip install csv

# Imports
import csv

# Path to file
file = "P:/game/Briefcase Pi 3B/Periodic_Table/periodic_data.csv"

# Function to clean up the data
def scrub_the_csv():
    cleaned_data = []
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '[', ']']

    # Clean an element
    def clean_data(element, colnum, rownum):
        index = 0
        name = ""
        number = ""
        symbol = ""
        weight = ""

        # Go thru the string and add elements to the name
        while index < len(element) and element[index] not in numbers:
            # "Â\xad" is a dash which we will skip when we find special char Â
            if element[index] == "Â":
                index += 2
            else:

                name += element[index]
                index += 1
        
        while index < len(element) and element[index] in numbers:
            number += element[index]
            index += 1

        # Go thru the string and add elements to the symbol
        while index < len(element) and element[index] not in numbers:
            # "â€‹" is a dash which we will skip when we find special char â
            if element[index] == "â":
                index += 3
            else:

                symbol += element[index]
                index += 1

        # Go thru the string and add elements to the weight
        while index < len(element):
            if element[index] in numbers:
                weight += element[index]
            index += 1

        # return the clean data
        return [name, number, symbol, weight, colnum, rownum]
        

    # Open and read the file
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        count = 0

        # print rows
        # skip rows 1 and 2 since those are headers of the table
        for row in reader:
            # print(row)
            if count > 1:
                # for each element in the row
                for i in range(len(row)):
                    # If the string isn't empty or "period 1" then clean the data
                    if len(row[i]) > 1 and row[i] != 'Period 1':
                        # append the clean data to the cleaned_data list
                        cleaned_data.append(clean_data(row[i], i, count))
            count += 1

    # print(cleaned_data)
    
    # Return the cleaned data
    return cleaned_data

scrub_the_csv()