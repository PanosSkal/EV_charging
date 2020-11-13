#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from matplotlib import pyplot as plt

plt.style.use("fivethirtyeight")
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


df = pd.read_csv('historical_data.csv')


# In[3]:


#dropping some extreme cases that skew the data
df = df.drop([1, 2950, 3904, 1032, 1926, 2620, 589, 2947, 948, 1031, 1353])


# In[4]:


#cleaning the dates
df[['start_timestamp','stop_timestamp']] = df[['start_timestamp','stop_timestamp']].replace('T', ' ', regex=True)
df[['start_timestamp','stop_timestamp']] = df[['start_timestamp','stop_timestamp']].replace('Z', '', regex=True) 
df[['start_timestamp','stop_timestamp']] = df[['start_timestamp','stop_timestamp']].apply(pd.to_datetime)


# In[5]:


#calculating the time of charge session in minutes
df['tot_minutes_diff'] = (df.stop_timestamp - df.start_timestamp) / pd.Timedelta(minutes=1)


# In[6]:


#Average time of a charging session
df.tot_minutes_diff.mean()


# In[7]:


df['weekday'] = df['start_timestamp'].dt.dayofweek


# In[8]:


#Average time of a charging session per day of the week
df.groupby('weekday',as_index=False)['tot_minutes_diff'].mean()


# In[9]:


#Average time of a charging session per charge station
df_seperated=df.groupby('charge_box_id', as_index=False)['tot_minutes_diff'].mean()
df_tags=df.groupby('charge_box_id', as_index=False)['id_tag'].first()
df_seperated['id_tag']=df_tags['id_tag']
df_seperated


# In[10]:


df['energy transferred(kWh)'] = (df['stop_value'] - df['start_value'])/1000


# In[11]:


df['Power(kW)'] = df['energy transferred(kWh)']/(df['tot_minutes_diff']/60)


# In[12]:


df = df.assign(time_of_Day=pd.cut(df.start_timestamp.dt.hour,[-1, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23],
                           labels=['0-2am', '2-4am', '4-6am', '6-8am', '8-10am', '10-12am', '12-2pm',
                                   '2-4pm', '4-6pm', '6-8pm', '8-10pm', '10-12pm']))


# In[13]:


df


# In[14]:


#histogram for a day(average minutes spent charging)
histogram_df1 = df.groupby('time_of_Day', as_index=False)['tot_minutes_diff'].mean()
histogram_df1


# In[15]:


#histogram for a day(total energy demand)
histogram_df2 = df.groupby('time_of_Day', as_index=False)['energy transferred(kWh)'].sum()
histogram_df2


# In[16]:


charger_power_df = df.groupby('charge_box_id', as_index=False)['Power(kW)'].mean()
charger_power_df['id_tag']=df_tags['id_tag']
charger_power_df.sort_values(by=['Power(kW)'], inplace=True)
charger_power_df

