# Get data from wikipedia for our periodic table

# pip install lxml

#  Imports
import pandas as pd

# Set url for data collection
url = "https://en.wikipedia.org/wiki/Periodic_table"

# Read all tables from the html
tables = pd.read_html(url)

# print how many tables are loaded
print(len(tables))

# Select a table
target_data = tables[1]

# Show 35 columns and rows
pd.set_option('display.max_columns', 35)
pd.set_option('display.max_rows', 35)

# Print data
print(target_data)

path = "P:/game/Briefcase Pi 3B/sandbox/Tutorials/periodic table/"

# Save data to a csv file
target_data.to_csv(path + 'periodic_data.csv', index=False, encoding='utf-8')

