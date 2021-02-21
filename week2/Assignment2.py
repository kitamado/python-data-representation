#!/usr/bin/env python
# coding: utf-8

# # Assignment 2
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv`. This is the dataset to use for this assignment. Note: The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
# 
# Each row in the assignment datafile corresponds to a single observation.
# 
# The following variables are provided to you:
# 
# * **id** : station identification code
# * **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
# * **element** : indicator of element type
#     * TMAX : Maximum temperature (tenths of degrees C)
#     * TMIN : Minimum temperature (tenths of degrees C)
# * **value** : data value for element (tenths of degrees C)
# 
# For this assignment, you must:
# 
# 1. Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
# 2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
# 3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
# 4. Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.
# 
# The data you have been given is near **Ann Arbor, Michigan, United States**, and the stations the data comes from are shown on the map below.

# In[ ]:


import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd

def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))

    station_locations_by_hash = df[df['hash'] == hashid]

    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8,8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mplleaflet.display()

leaflet_plot_stations(400,'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89')


# In[ ]:


# pd.set_option('display.max_columns', None)
# pd.set_option("display.max_rows", None)


# In[1]:


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# In[2]:


df = pd.read_csv('fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')
df = df.sort_values(by='Date')
df_mask = df['Date']<='2014-12-31'
df_rf = df[df_mask]
df_cp = df[~df_mask]


# In[3]:


df_rf['Date'] = df_rf['Date'].str[5:]
df_rf = df_rf.drop(df_rf[df_rf['Date']=='02-29'].index)
df_cp['Date'] = df_cp['Date'].str[5:]


# In[4]:


df_rf_tmax = df_rf['Data_Value'].groupby(df_rf['Date']).max().reset_index()
df_rf_tmin = df_rf['Data_Value'].groupby(df_rf['Date']).min().reset_index()


# In[5]:


df_cp_tmax = df_cp['Data_Value'].groupby(df_cp['Date']).max().reset_index()
df_cp_tmin = df_cp['Data_Value'].groupby(df_cp['Date']).min().reset_index()
df_cp_tmax['broken'] = np.nan
df_cp_tmin['broken'] = np.nan


# In[6]:


df_cp_tmax['broken'] = [df_cp_tmax['Data_Value'][i] if df_cp_tmax['Data_Value'][i] > df_rf_tmax['Data_Value'][i] else np.nan for i in range(365)]
df_cp_tmin['broken'] = [df_cp_tmin['Data_Value'][i] if df_cp_tmin['Data_Value'][i] < df_rf_tmin['Data_Value'][i] else np.nan for i in range(365)]


# In[7]:


get_ipython().run_line_magic('matplotlib', 'notebook')


# In[8]:


d = np.arange(365)


# In[34]:


plt.plot(d, df_rf_tmin['Data_Value'], d, df_rf_tmax['Data_Value'], d, df_cp_tmin['broken'], '<', d, df_cp_tmax['broken'], '<')
plt.legend(['Min temperature in 2005-2014', 'Max temperature in 2005-2014', 'Extreme low temperature in 2015', 'Extreme high temperature in 2015'])

plt.gca().fill_between(range(365), 
                       df_rf_tmax['Data_Value'], df_rf_tmin['Data_Value'],
                       facecolor='lightgrey', 
                       alpha=0.8)
plt.xticks(np.linspace(0,365,13)[:-1], ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))

plt.xlabel('Month')
plt.ylabel('Max and Min Temperature')
plt.title('Temperature in 2005-2015')


# In[35]:


plt.savefig('temperature.png', dpi=300)


# In[ ]:




