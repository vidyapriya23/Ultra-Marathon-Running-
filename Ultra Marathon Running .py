#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


import seaborn as sns


# In[3]:


df = pd.read_csv("TWO_CENTURIES_OF_UM_RACES.csv")


# In[4]:


df.head(10)


# In[5]:


df.shape


# In[6]:


df.dtypes


# In[7]:


#clean up data 


# In[15]:


#only want USA Races, 50k or 50 Miles, 2020
#step 1 show 50Miles or 50k
#50km
#50mi


# In[14]:


df[df['Event distance/length'] == '50mi']


# In[16]:


#combine 50k/50mi with isin


# In[17]:


df[df['Event distance/length'].isin(['50km', '50mi'])]  


# In[20]:


df[(df['Event distance/length'].isin(['50km', '50mi'])) & (df['Year of event'] == 2020)]     


# In[32]:


df[df['Event name'] == 'Everglades 50 Mile Ultra Run (USA)']['Event name']


# In[38]:


df[df['Event name'] == 'Everglades 50 Mile Ultra Run (USA)']['Event name'].str.split('(').str.get(1)


# In[42]:


df[df['Event name'].str.split('(').str.get(1).str.split(')').str.get(0) == 'USA']


# In[43]:


df[(df['Event distance/length'].isin(['50km', '50mi'])) & (df['Year of event'] == 2020) & (df['Event name'].str.split('(').str.get(1).str.split(')').str.get(0) == 'USA')]  


# In[52]:


df2 = df[(df['Event distance/length'].isin(['50km', '50mi'])) & (df['Year of event'] == 2020) & (df['Event name'].str.split('(').str.get(1).str.split(')').str.get(0) == 'USA')] 


# In[53]:


df2.head(10)


# In[54]:


df2.shape


# In[55]:


#remove (USA) from event name 


# In[56]:


df2['Event name'].str.split('(').str.get(0)


# In[59]:


df2['Event name'] = df2['Event name'].str.split('(').str.get(0)


# In[61]:


df2.head()


# In[62]:


#cleanup athlete age 


# In[64]:


df2['athlete_age'] = 2020 - df2['Athlete year of birth']


# In[65]:


#remove h athlete performance  


# In[67]:


df2['Athlete performance'] = df2['Athlete performance'].str.split(' ').str.get(0)


# In[68]:


df2.head(5)


# In[69]:


#drop columns: Athlete club, Athlete Country, Athlete year of birth, Athlete age category 


# In[71]:


df2 = df2.drop(['Athlete club', 'Athlete country', 'Athlete year of birth', 'Athlete age category'], axis = 1)


# In[72]:


df2.head()         


# In[73]:


#clean up null values


# In[74]:


df2.isna().sum()


# In[77]:


df2[df2['athlete_age'].isna()== 1]


# In[78]:


df2 = df2.dropna()


# In[79]:


df2.shape


# In[80]:


#check for duplicates 


# In[82]:


df2[df2.duplicated() == True]


# In[83]:


#reset index


# In[85]:


df2.reset_index(drop = True)


# In[86]:


#fix types 


# In[87]:


df2.dtypes


# In[88]:


df2['athlete_age'] = df2['athlete_age'].astype(int)


# In[91]:


df2['Athlete average speed'] = df2['Athlete average speed'].astype(float)


# In[92]:


df2.dtypes


# In[93]:


df2.head()


# In[ ]:


#rename coulumns 


# In[ ]:


#Year of event                  int64
#Event dates                   object
#Event name                    object
#Event distance/length         object
#Event number of finishers      int64
#Athlete performance           object
#Athlete gender                object
#Athlete average speed        float64
#Athlete ID                     int64
#athlete_age                    int64


# In[96]:


df2 = df2.rename(columns = {'Year of event':'year', 
                           'Event dates':'race_day',
                           'Event name':'race_name',
                           'Event distance/length':'race_length',
                           'Event number of finishers':'race_number_of_finishers',
                           'Athlete performance':'athlete_perormance',
                           'Athlete gender':'athlete_gender',
                           'Athlete average speed':'athlete_average_speed',
                           'Athlete ID': 'athlete_id'
                           })


# In[97]:


df2.head()


# In[98]:


#reorder columns 


# df3 = df2[['race_day', 'race_name', 'race_length','race_number_of_finishers','athlete_perormance','athlete_gender', 'athlete_average_speed', 'athlete_id', 'athlete_age']] 

# In[100]:


df3 = df2[['race_day', 'race_name', 'race_length','race_number_of_finishers','athlete_perormance','athlete_gender', 'athlete_average_speed', 'athlete_id', 'athlete_age']]


# In[101]:


df3.head()


# In[102]:


df3[df3['race_name'] == 'Everglades 50 Mile Ultra Run ']


# In[103]:


df3[df3['athlete_id'] == 222509]


# In[104]:


#charts and graphs 


# In[105]:


sns.histplot(df3['race_length'])


# In[106]:


sns.histplot(df3, x = 'race_length', hue = 'athlete_gender')


# In[107]:


sns.displot(df3[df3['race_length'] == '50mi']['athlete_average_speed'])


# In[109]:


sns.violinplot(data = df3, x='race_length', y= 'athlete_average_speed', hue= 'athlete_gender')


# In[110]:


sns.violinplot(data = df3, x='race_length', y= 'athlete_average_speed', hue= 'athlete_gender', split = True, inner = 'quart')


# In[113]:


sns.lmplot(data=df3, x= 'athlete_age', y='athlete_average_speed', hue = 'athlete_gender')


# In[114]:


#questions I want to find out from the data 


# In[115]:


#race_day 
#race_name
#race_length
#race_number_of_finoishers
#athlete_id
#athlete_gender
#athlete_age
#athlete_performance
#athlete_average_speed


# In[ ]:


#Difference in speed for the 50k, 50mi male to female 


# In[116]:


df3.groupby(['race_length', 'athlete_gender'])['athlete_average_speed'].mean()


# In[ ]:


#what age groups are the best in the 50m Race (20 + races min)


# In[172]:


df3.groupby('athlete_age')['athlete_average_speed'].agg(['mean', 'count']).sort_values('mean', ascending = False).query('count>19').head(15)


# In[173]:


df3.groupby('athlete_age')['athlete_average_speed'].agg(['mean', 'count']).sort_values('mean', ascending = True).query('count>19').head(15)


# In[ ]:


#seasons for the data -> slower in summer than winter? 
#spring 3-5
#Summer 6-8
#fall 9-11
#winter 12-2 

#split between two decimals 


# In[164]:


df3['race_month'] = df3['race_day'].str.split('.').str.get(1).astype(int)


# In[167]:


df3['race_season'] = df3['race_month'].apply(lambda x: 'Winter' if x > 11 else 'Fall' if x > 8 else 'summer' if x > 5 else 'Spring' if x > 2 else 'Winter')


# In[168]:


df3.head(25)


# In[169]:


df3.groupby('race_season')['athlete_average_speed'].agg(['mean', 'count']).sort_values('mean', ascending = False)


# In[ ]:


#50 miler only 


# In[174]:


df3.query('race_length == "50mi"').groupby('race_season')['athlete_average_speed'].agg(['mean', 'count']).sort_values('mean', ascending = False)


# In[ ]:



        


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




