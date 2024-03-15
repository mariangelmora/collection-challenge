#!/usr/bin/env python
# coding: utf-8

# In[89]:


# Import relevant libraries
from splinter import Browser
from bs4 import BeautifulSoup as soup
import matplotlib.pyplot as plt
import pandas as pd
from selenium import webdriver


# In[90]:


browser = Browser('chrome')


# In[91]:


# Visit the website
url = "https://static.bc-edx.com/data/web/mars_facts/temperature.html"
browser.visit(url)


# In[92]:


# Get the HTML content of the page visited by the browser
html = browser.html

# Create a BeautifulSoup object
soup_object = soup(html, 'html.parser')


# In[93]:


# Extract all rows of data
rows = soup_object.find_all('tr')
print("Number of rows found:", len(rows))


for row in rows:
    row


# In[94]:


# Empty lists
ids = []
terrestrial_dates = []
sols = []
ls_values = []
months = []
min_temps = []
pressures = []

rows = soup_object.find_all('tr')

# Loop through the scraped data to create a list of rows
for row in rows[1:]:  
    columns = row.find_all('td')
    id_val = columns[0].text.strip()
    terrestrial_date = columns[1].text.strip()
    sol = columns[2].text.strip()
    ls = columns[3].text.strip()
    month = columns[4].text.strip()
    min_temp = columns[5].text.strip()
    pressure = columns[6].text.strip()
    
    ids.append(id_val)
    terrestrial_dates.append(terrestrial_date)
    sols.append(sol)
    ls_values.append(ls)
    months.append(month)
    min_temps.append(min_temp)
    pressures.append(pressure)

# Create a Pandas DataFrame by using the list of rows and a list of the column names
data = {
    'id': ids,
    'terrestrial_date': terrestrial_dates,
    'sol': sols,
    'ls': ls_values,
    'month': months,
    'min_temp': min_temps,
    'pressure': pressures
}

df = pd.DataFrame(data)
df


# In[95]:


# Create an empty list to store rows of data
data_rows = []

# Find all rows of data
rows = soup_object.find_all('tr')

# Loop through each row to extract data
for row in rows[1:]:  # Skip the first row (header row)
    # Initialize an empty dictionary to store row data
    row_data = {}
    
    # Extract data from each column of the row
    columns = row.find_all('td')
    row_data['id'] = columns[0].text.strip()
    row_data['terrestrial_date'] = columns[1].text.strip()
    row_data['sol'] = columns[2].text.strip()
    row_data['ls'] = columns[3].text.strip()
    row_data['month'] = columns[4].text.strip()
    row_data['min_temp'] = columns[5].text.strip()
    row_data['pressure'] = columns[6].text.strip()
    
    # Append the row data dictionary to the list of rows
    data_rows.append(row_data)

# Print the list of rows
data_rows


# In[110]:


# Display the data types of each column
df.dtypes

# Convert data types as necessary
df['terrestrial_date'] = pd.to_datetime(df['terrestrial_date'])
df['sol'] = df['sol'].astype(int)
df['ls'] = df['ls'].astype(float)
df['min_temp'] = df['min_temp'].astype(float)
df['pressure'] = df['pressure'].astype(float)

# Display the data types after conversion
df.dtypes


# In[97]:


# Convert 'terrestrial_date' column to datetime
df['terrestrial_date'] = pd.to_datetime(df['terrestrial_date'])

# Convert 'sol' column to integer
df['sol'] = df['sol'].astype(int)

# Convert 'ls' column to float
df['ls'] = df['ls'].astype(float)

# Convert 'min_temp' column to float
df['min_temp'] = df['min_temp'].astype(float)

# Convert 'pressure' column to float
df['pressure'] = df['pressure'].astype(float)


# In[98]:


# Examine the data type of each column again
df.dtypes


# In[99]:


# 1. How many months are there on Mars?
unique_months = df['month'].unique()
num_months = len(unique_months)
num_months


# In[100]:


# 2. How many Martian days' worth of data are there?
num_martian_days = df['sol'].nunique()
num_martian_days


# In[111]:


# 3. What is the average low temperature by month?
avg_min_temp_by_month = df.groupby('month')['min_temp'].mean()

# Print the result
avg_min_temp_by_month



# In[79]:


# Plot the average temperature by month
plt.figure(figsize=(10, 6))
avg_min_temp_by_month.plot(kind='bar', color='orange')
plt.title('Average Low Temperature by Month on Mars')
plt.xlabel('Month')
plt.ylabel('Average Low Temperature (°C)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()


# In[103]:


# Identify the coldest and hottest months in Curiosity's location
coldest_month = avg_min_temp_by_month.idxmin()
hottest_month = avg_min_temp_by_month.idxmax()

coldest_temp = avg_min_temp_by_month[coldest_month]
hottest_temp = avg_min_temp_by_month[hottest_month]
print(coldest_month, coldest_temp, "°C")
print(hottest_month, hottest_temp, "°C")


# In[104]:


# 4. Average pressure by Martian month
avg_pressure_by_month = df.groupby('month')['pressure'].mean()
avg_pressure_by_month


# In[105]:


# Plot the average pressure by month
plt.figure(figsize=(10, 6))
avg_pressure_by_month.plot(kind='bar', color='purple')
plt.title('Average Atmospheric Pressure by Month on Mars')
plt.xlabel('Month')
plt.ylabel('Average Atmospheric Pressure (Pa)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()


# In[112]:


# 5. How many terrestrial (earth) days are there in a Martian year?
days_per_year = df.groupby(df['terrestrial_date'].dt.year)['sol'].max().diff().mean()
days_per_year


# In[107]:


# Plotting the daily minimum temperature over time
plt.figure(figsize=(10, 6))
plt.plot(df['terrestrial_date'], df['min_temp'], color='orange')
plt.title('Daily Minimum Temperature on Mars')
plt.xlabel('Terrestrial Date')
plt.ylabel('Minimum Temperature (°C)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# In[113]:


file_path = "mars_data.csv"

# Write the DataFrame to a CSV file
df.to_csv(file_path, index=False)
file_path


# In[114]:


browser.quit()


# In[ ]:




