#!/usr/bin/env python
# coding: utf-8

# # Sales Analysis

# In[1]:


import pandas as pd
import os


# #### Merging 12 months data into one file

# In[2]:


df = pd.read_csv('./Sales_Data/Sales_April_2019.csv')

files = [file for file in os.listdir('./Sales_Data')]

all_month_data = pd.DataFrame()

for file in files:
    df = pd.read_csv('./Sales_Data/' + file)
    all_month_data = pd.concat([all_month_data, df])

all_month_data.to_csv('Merged_Data.csv', index=False)


#    #### Read the updated file

# In[3]:


merged_data = pd.read_csv('Merged_Data.csv')
merged_data.head()


# ### Cleaning up the data

# #### 1. Dropping NaN Values

# In[4]:


merged_data = merged_data.dropna(how='all')
merged_data.head()


# #### 2. Removing duplicated data 

# In[5]:


merged_data = merged_data[merged_data['Order Date'].str[0:2] != 'Or']


# #### 3. Converting columns to right dtype

# In[6]:


merged_data['Quantity Ordered'] = pd.to_numeric(merged_data['Quantity Ordered'])
merged_data['Price Each'] = pd.to_numeric(merged_data['Price Each'])


# ### Adding New Columns For Easy Access

# #### 1. Month (Also changing month type from str to int)

# In[7]:


#Alternative method
# merged_data['Month'] = merged_data['Order Date'].str[0:2]
# merged_data['Month'] = merged_data['Month'].astype('int32')
# merged_data.head()

merged_data['Month'] = pd.to_datetime(merged_data['Order Date']).dt.month
merged_data.head()


# #### 2. Sales

# In[8]:


merged_data['Sales'] = merged_data['Quantity Ordered'] * merged_data['Price Each']
merged_data.head()


# #### 3. City (state)

# In[9]:


# def get_city(address):
#     return address.split(',')[1]

# def get_state(address):
#     return address.split(',')[2].split(' ')[1]

merged_data['City'] = merged_data['Purchase Address'].apply(lambda x: f"{x.split(',')[1]} ({x.split(',')[2].split(' ')[1]})")
merged_data.head()


# ### Answering questions

# #### 1. What was the best month for sales and how much money was made in that month? 

# In[10]:


total_sales = merged_data.groupby('Month')['Sales'].sum()
total_sales


# In[11]:


import matplotlib.pyplot as plt

months = range(1,13)

plt.bar(months,total_sales)
plt.xticks(months)
plt.ylabel('Sales in USD Millions ($)')
plt.xlabel('Month number')

plt.show()


# #### 2. Which city had the highest number of sales?

# In[12]:


most_sold_city = merged_data.groupby('City')[['Quantity Ordered', 'Sales']].sum()
most_sold_city


# In[13]:


# need to fetch cities in the same order as the most_sold_city column
cities = [city for city, df in merged_data.groupby('City')]

plt.bar(cities, most_sold_city['Sales'])
plt.xticks(cities, rotation='vertical')
plt.xlabel('Cities')
plt.ylabel('Sales in USD Millions $')

plt.show()


# #### 3. At what time should the advertisments be played to have the maximum effect?

# In[14]:


merged_data['Order Date'] = pd.to_datetime(merged_data['Order Date'])


# In[15]:


merged_data['Hours'] = merged_data['Order Date'].dt.hour
merged_data['Minutes'] = merged_data['Order Date'].dt.minute
merged_data.head()


# In[16]:


hours = [hour for hour, df in merged_data.groupby('Hours')]

plt.plot(hours, merged_data.groupby('Hours').count())
plt.xticks(hours)
plt.grid()
plt.xlabel('Hours')
plt.ylabel('Number of Orders')

plt.show()


# #### 4. What products are sold together most often?

# In[17]:


# Look at similar ORDER IDs, create a separate dataframe

df = merged_data[merged_data['Order ID'].duplicated(keep=False)]

# show the products in the same line

df['Grouped Products'] = df.groupby('Order ID')['Product'].transform(lambda x: ', '.join(x))
df.head(10)

# Drop the duplicates

df = df[['Order ID', 'Grouped Products']].drop_duplicates()
df.head(10)


# In[18]:


# Counting most often ordered pair
from itertools import combinations
from collections import Counter

count = Counter()

for row in df['Grouped Products']:
    row_list = row.split(', ')
    count.update(Counter(combinations(row_list, 2)))
# count.update(Counter(combinations(row_list, 3))) to find most ordered triplets

count.most_common(10)
# for key, value in count.most_common(10):
# print(key, value)


# #### 5. What product sold the most and why?

# In[19]:


most_sold_product = merged_data.groupby('Product')['Quantity Ordered'].count()
most_sold_product


# In[20]:


product_list = [product for product, df in merged_data.groupby('Product')]

plt.bar(product_list, most_sold_product)
plt.xticks(product_list, rotation='vertical')
plt.xlabel('Products')
plt.ylabel('Quantity Ordered')

plt.show()


# In[ ]:




