#!/usr/bin/env python
# coding: utf-8

# ## Electric Vehicle Adoption Analysis for Business Decision-Making

# ### Table of Content

# * Introduction
# * Exploratory Analysis
# * Conclusion
# 

# ### Introduction

# Electric vehicles (EVs) have gained significant popularity as a clean and sustainable means of transportation. To harness the
# 
# potential of this growing market, businesses need to understand EV adoption patterns, consumer preferences, and market trends.
# 
# This case study aims to analyze an electric vehicle population dataset to provide valauable insights for businesses in the EV
# 
# industry.

# ### About the dataset

# This dataset shows the Battery Electric Vehicles (BEVs) and Plug-in Hybrid Electric Vehicles (PHEVs) that are currently
# 
# registered through Washington State Department of Licensing (DOL). It features 124716 rows and 17 columns of EV related data 
# 
# across the United States of America.

# ### Objectives

# The primary objectives of this data analysis project are:
# 
# a) Identify the geographic distribution of EVs: Determine which counties, cities and states have the highest concentration of electric vehicles.
# 
# b) Analyze EV model and manufacturers: Examine the market share and trends of different EV manufacturers and their respective models.
# 
# c) Investigate EV range to understand consumer preferences.
# 
# d) Analyze utility provider influence: Investigate the role of electric utility providers in promoting EV adoption.
# 
# e) Investigate CAFV eligibilty: Determine the proportion of EVs eligible for Clean Alternative Fuel Vehicle (CAFV) incentives.

# ### Methodology

# a) Data Cleaning: Remove any duplicates, missing values, or irrelevant columns from the dataset.
# 
# b) Descriptive Analysis: Generate descriptive statistics and visualizations and to gain an overall understanding of the dataset.
# 
# c) Geographic Analysis: Utilize geographical data to map the distribution of electric vehicles across counties, cities, and states.
# 
# d) Manufacturer and Model Analysis: Analyze the market share of different EV manufacturers and investigate the popularity of specific EV models.
# 
# e) Electric Range Analysis: Explore the electric range of EVs from popular manufacturers.
# 
# f) Electric Utility Analysis: Analyze the role of electric utility providers in promoting EV adoption by assessing their market penetration.
# 
# g) CAFV Eligibility Analysis: Calculate the percentage of EVs eligible for CAFV incentives to unerstand the potential impact on customer choices.

# ### Expected Outcomes

# a) Identification of hotspots for EV adoption: Pinpoint areas with high concentration of EVs, allowing businesses to prioritize 
# marketing and infrastucture investments.
# 
# b) Insights into manufacturer and model preferences: Determine the most popular EV manufacturers and models, helping businesses 
# understand consumer preferences and plan inventory accordingly.
# 
# c) Understanding the electric range and it's effect on the adoption of certain EVs: Determine the sensitivity of EV buyers based 
# on electric range.
# 
# d) Evaluation of utility provider influence: Understand the role of electric utility providers in shaping EV adoption rates.
# 
# e) CAFV eligibility impact: Assess the influence of CAFV eligibilty on consumer choices, potentially indicating the 
# effectiveness of incentives and suggesting improvements. 

# ### Exploratory Analysis

# #### Importing the python packages to be used for analysis

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# ### Data Manipulation

# Here we will take a first look at the dataset by loading it into our workspace and determining what parts of our dataset might
# 
# require a bit of cleaning or transformation.

# In[2]:


# Load the dataframe using the pandas read_csv function
# Then assign the variable name 'evpd' to the dataframe
# Finally, we will print the dataframe

evpd = pd.read_csv('Downloads/Electric_Vehicle_Population_Data.csv')
evpd


# If you glance through, you will realize our dataframe contains 17 columns and 124,716 rows, Immediately we can establish that
# 
# certain columns will be requiring cleaning and transformation processes. The following columns will prove crucial to our 
# 
# analysis.
# 
# * The counties, cities and state columns will prove essential to our geographical distribution of EVs.
# 
# 
# * The Make and model columns, we will use for manufacturer and model Analysis.
# 
# 
# * We will also be analyzing the electric vehicle type, CAFV eligibility, electric range and electric utility columns.
# 
# 

# In[3]:


# Check for basic information regarding our dataset

evpd.info()


# From the results, our dataset does not include any null values. Also, all our columns have consistent data types.

# In[4]:


# Check for unique values in each column of the dataset

evpd.nunique()


# The results above gives us a breakdown of the unique contents of each column. 

# In[5]:


# Check for the basic statistics and aggregations of the numerical columns in the dataset

evpd.describe()


# The results above show the count, mean, standard deviation, minimum, percentile and maximum values of numeric columns in the 
# 
# dataset. The results also show inconsistencies in the Base MSRP column where the minimum and percentile values up to the 75th 
# 
# percentile is zero(0), as a result that column lacks the needed integrity for analysis. 

# ### Data Cleaning

# For data cleaning we will carry out the following tasks:
# 
# * Drop the columns VIN (1-10), Postal Code, Base MSRP, Legislative District, DOL Vehicle ID, Vehicle Location and 2020 Census Tract, as they will not be needed for this analysis.
# 
# 
# * Create a new column for CAFV eligibility that will show more consistent results than what currently is.
# 
# 
# * Remove duplicate records from the dataset.
# 
# 
# * Remove all rows with electric range as zero(0), as it is impossible to have electric cars with an electric range of zero.
# 
# 
# * Rename all of the column headers, this time with consistent formatting.

# ### Dropping columns not needed for analysis

# In[6]:


# dropping unnecessary columns

evpd.drop(['VIN (1-10)', 'Postal Code', 'Base MSRP', 'Legislative District', 'DOL Vehicle ID', 'Vehicle Location', '2020 Census Tract'], axis=1, inplace=True)

# view columns to check for the effect of the changes made

evpd.head(0)


# ### Creating a new column for CAFV eligibility

# In[7]:


# creating a new column 'cafv_eligibility2' where cafv_eligibility options will reflect only, eligible, ineligible or unknown

conditions = [
    evpd['Clean Alternative Fuel Vehicle (CAFV) Eligibility'] == 'Clean Alternative Fuel Vehicle Eligible',
    evpd['Clean Alternative Fuel Vehicle (CAFV) Eligibility'] == 'Not eligible due to low battery range',
]

values = ['Eligible', 'Ineligible']
evpd.loc[:, 'cafv_eligibility2'] = np.select(conditions, values, default='Other')

# check for the effect of the changes made

evpd


# ### Renaming column headers and introducing consistent naming formats

# In[8]:


# making all columns lowercase

evpd.rename(columns = lambda x : x.lower(), inplace=True)
evpd.head(0)

# renaming mispelt columns

evpd.rename(columns = {'model year':'model_year', 'make':'manufacturer', 'electric vehicle type':'electric_vehicle_type', 'clean alternative fuel vehicle (cafv) eligibility':'cafv_eligibility', 'electric range':'electric_range'}, inplace=True)


# ### Removing duplicates from the dataset

# In[9]:


# removing duplicate records from the dataset, we will assign 'df1' as the new variable name for the dataset

df = evpd
df1 = df.drop_duplicates()

# Checking the new copy of the dataset after removing duplicates

df1


# ### Removing all rows that have electric range as zero

# In[10]:


# removing all rows that have electric range as zero and assign a new variable name 'df2' to the cleaned dataset

df2 = df1[df1.electric_range !=0]


# ### Descriptive Analysis

# In[11]:


# Check the basic statistics and aggregations of the numerical columns in the cleaned dataset

df2.describe()


# After cleaning out all electric range values = 0, it's range of values now look okay to work with. Also the highest electric 
# 
# range for an EV in this dataset is 337 miles.

# In[12]:


# plotting a simple histogram of the numerical columns of the dataset using the histogram function

df2.hist(figsize=[6,6]);


# The histogram shows that a greater proportion of the EV models in the dataset were manufactured between 2017 to 2020. Also a 
# 
# large proportion of the vehicles in this dataset have an electric range below 100 miles.

# ### Geographical Analysis of the distribution of EVs
# 
# In this analysis we will, the counties, cities and states with the highest concentration of Evs in this dataset and represent 
# 
# same using charts.

# In[13]:


# Check to see the Top10 counties with the highest EV adoption

top_counties = df2['county'].value_counts().head(10)


# In[14]:


# Top10 counties represented in a bar chart

plt.figure(figsize=(10, 6))
sns.barplot(x=top_counties.index, y=top_counties.values)
plt.xlabel('County')
plt.ylabel('Count')
plt.title('Top 10 Counties')
plt.xticks(rotation=45)
plt.tight_layout()

# Show the plot

plt.show()


# The results above shows that the King's, Pierce and Snohomish counties have the highest concentration of EVs in The United 
# 
# States of America in this dataset.

# In[15]:


# Check to see the Top10 cities with the highest EV adoption

top_cities = df2['city'].value_counts().head(10)


# In[16]:


# Top10 cities represented in a bar chart

plt.figure(figsize=(10, 6))
sns.barplot(x=top_cities.index, y=top_cities.values)
plt.xlabel('City')
plt.ylabel('Count')
plt.title('Top 10 Cities')
plt.xticks(rotation=45)
plt.tight_layout()

# Show the plot
plt.show()


# The results above shows that the cities of Seatle, Spokane and Bothell have the highest concentration of EVs in The United 
# 
# States of America in this dataset.  

# In[17]:


# Check to see the Top10 states with the highest EV adoption

top_states = df2['state'].value_counts().head(10)


# In[18]:


# Top10 states represented in a bar chart

plt.figure(figsize=(10, 6))
sns.barplot(x=top_states.index, y=top_states.values)
plt.xlabel('state')
plt.ylabel('count')
plt.title('Top 10 states')
plt.xticks(rotation=45)
plt.tight_layout()

# Show the plot
plt.show()


# The results above shows that Washington DC has the highest concentration of EVs in The United 
# 
# States of America in this dataset. 

# ### Manufacturer and model market share analysis
# 
# In this analysis we will explore the market share of the various manufacturers, we will also look at the models that are highly 
# 
# sort after by consumers. These details will be represented using charts.

# In[19]:


# manufacturer market share Analysis

manufacturer_counts = df2['manufacturer'].value_counts()
total_count = manufacturer_counts.sum()
manufacturer_market_share = (manufacturer_counts / total_count) * 100


# In[20]:


# Sort manufacturers by market share in descending order
manufacturer_market_share_sorted = manufacturer_market_share.sort_values(ascending=False)

# Plotting the market share of EV manufacturers
plt.figure(figsize=(14, 10))
manufacturer_market_share_sorted.plot(kind='barh')
plt.xlabel('Market Share (%)')
plt.ylabel('Manufacturer')
plt.title('Market Share of EV Manufacturers')
plt.xticks(rotation=45)

# Add market share percentage as text on each bar
for i, v in enumerate(manufacturer_market_share_sorted.values):
    plt.text(v, i, f'{v:.2f}%', va='center')
    
plt.tight_layout()
plt.show()


# In this dataset, the results above shows that Tesla, Chervolet and BMW are the manufacturers with the highest market share of 
# 
# EVs in The United States of America. Nissan, Ford, Toyota, Kia, Volvo, Jeep and Audi make up the top 10 manufacturers with the 
# 
# highest market shares.

# In[21]:


# Top10 EV models in use

top_models = df2.groupby(['manufacturer', 'model']).size().reset_index(name='count')
top_models = top_models.sort_values('count', ascending=False).head(10)


# In[22]:


# Top10 EV models in use represented in a bar chart

# Set up the data for plotting
models = top_models['manufacturer'] + ' ' + top_models['model']
counts = top_models['count']

# Create the bar chart
plt.figure(figsize=(10, 6))
sns.barplot(x=models, y=counts)
plt.xticks(rotation=45)
plt.xlabel('Car Model')
plt.ylabel('Count')
plt.title('Top 10 Purchased Electric Vehicle Models')
plt.tight_layout()

# Show the chart
plt.show()


# The chart shows the top10 EV models that are clearly sort after by consumers.

# ### Manufacturer and Electric Range Analysis
# 
# 
# In this section, we will explore the various manufacturers and the electric range of their vehicles, we will check the minimum,
# 
# maximum and mean values of their electric range and also show the distribution for the top10 manufacturers using scatterplots.

# In[23]:


#showing the maximum, minimum and mean values for the range of EVs

ev_range = df2.groupby(['manufacturer']).aggregate({'electric_range': ['mean', 'min', 'max']})
ev_range


# In[24]:


# Get the top 10 manufacturers by count
top_10_manufacturers = df2['manufacturer'].value_counts().nlargest(10).index

# Filter the DataFrame to include only the rows with the top 10 manufacturers
filtered_df = df2[df2['manufacturer'].isin(top_10_manufacturers)]

# Increase the size of the scatter plot
plt.figure(figsize=(10, 6))

# Create a scatter plot for each manufacturer
for make in top_10_manufacturers:
    make_data = filtered_df[filtered_df['manufacturer'] == make]
    plt.scatter(make_data['manufacturer'], make_data['electric_range'], label=make)

# Set labels and title for the plot
plt.xlabel('Manufacturer')
plt.ylabel('Electric Range')
plt.title('Top Electric Vehicle Makes by Counts and Electric Range')
plt.legend()

# Show the scatter plot
plt.show()


# The results show the amongst the ten most purchased brands, Tesla offers the best electric range for a greater proportion of its EVs 

# ### Battery Vehicle Type Analysis
# 
# In this analysis we will explore the battery vehicle type preference of the consumers.

# In[25]:


# checking the count of the different types of electric vehicle type

df2['electric_vehicle_type'].value_counts()


# In[26]:


# Representing this in a pie chart

# Generate the value counts for 'caf_eligibility2'
value_counts = df2.electric_vehicle_type.value_counts()

# Set the size of the figure
fig, ax = plt.subplots(figsize=(7, 7))

# Create the pie chart with percentage values
value_counts.plot(kind='pie', autopct='%1.1f%%', ax=ax)

# Add a title to the chart
plt.title('Electric Vehicle Type Distribution')

# Display the chart
plt.show()


# The results show 54.7% of the EV population use plug-in Hybrid Electric Vehicle and 45.3% use battery electric vehicles.

# ### CAFV Eligibility Analysis

# In[27]:


# checking the count of eligible EVs compared with those that are ineligible

df2['cafv_eligibility2'].value_counts()


# In[28]:


# Representing this in a pie chart

# Generate the value counts for 'caf_eligibility2'
value_counts = df2.cafv_eligibility2.value_counts()

# Set the size of the figure
fig, ax = plt.subplots(figsize=(7, 7))

# Create the pie chart with percentage values
value_counts.plot(kind='pie', autopct='%1.1f%%', ax=ax)

# Add a title to the chart
plt.title('Cafv Eligibility Distribution')

# Display the chart
plt.show()


# The results show 65.7% of the EV population are eligible and 34.3% are ineligible clean alternative fuel vehicle.

# ### Electric Utility Analysis
# 
# In this analysis we will explore the market share of electric utility providers, to know which ones are most active in the EV business. 

# In[29]:


# Analysis to ascertain the market share of each EV utility provider
utility_counts = df2['electric utility'].value_counts()
total_count = utility_counts.sum()
utility_market_share = (utility_counts / total_count) * 100
utility_market_share


# This result shows that there are 71 different utility providers across the United States. We will go on to 

# In[30]:


top_ums = utility_market_share.head(20)


# In[31]:


# Plotting the market share of the Top20 electric utility providers
plt.figure(figsize=(14, 10))
top_ums.plot(kind='barh')
plt.xlabel('Electric Utility Provider')
plt.ylabel('Market Share of Electric Utility Providers')
plt.title('Market share (%)')
plt.xticks(rotation=45)
# Add market share percentage as text on each bar
for i, v in enumerate(top_ums.values):
    plt.text(v, i, f'{v:.2f}%', va='center')
plt.tight_layout()
plt.show()


# From the results, Puget sound energy INC has the highest market share for a single outlet, nevertherless, Bonneville power 
# 
# administration has a greater spread of outlets across counties and cities.

# ### Conclusion

# By conducting a comprehensive analysis of the electric vehicle population dataset, this case study was aimed at providing 
# 
# valuable insights for businesses operating in the electric vehicle industry. The outcomes will support decision-making 
# 
# processes, allowing businesses to tailor their strategies to target specific geographic areas, understand consumer preferences, 
# 
# optimize electric range and pricing, and collaborate with utility providers. These insights should contribute to the sustainable 
# 
# growth and development of the electric vehicle market.
# 
# However, a few issues were encountered that may likely skew our results in a way, 98.96% of the EVs used in this analysis are in 
# 
# the US state of Washington DC, as a result our analysis will mostly support business decision-making in that state and not 
# 
# necessarily the rest of the United States.
# 
# Also the base MSRP column had a majority of its values as zero, hence it could not be used for analysis of product pricing and 
# 
# its effect in the EV market. 
