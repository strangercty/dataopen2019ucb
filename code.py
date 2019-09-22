
# coding: utf-8

# In[353]:


import pandas as pd
import numpy as np
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import seaborn  as sns
sns.set() 


# In[354]:


job = pd.read_csv("job_listings.csv")
soc = pd.read_csv("soc_code_legend.csv")


# In[371]:


job.head()


# In[356]:


job.columns


# In[372]:


unit = np.array([1181.0,
 2119.0,                
 2112.0, 
 2111.0, 
 2112.0, 
 2113.0, 
 2114.0,
 1184.0,
 2211.0,
 2212.0,
 2213.0,
 2214.0,
 2215.0,
 2216.0,
 2217.0,
 2218.0,
 2219.0,
 2221.0,
 2222.0,
 2223.0,
 2229.0,
 2231.0,
 2232.0,
 2463,
 3213.0,
 3216.0,
 3217.0,
 3218.0,
 3219.0,
 3561.0,
 3562.0,
 3563.0,
 3564.0,
 3565.0,
 3567.0,
 6121,
 6141.0,
 6142.0,
 6143.0,
 6144.0,
 6145.0,
 6146.0,
 6147.0,
 6148.0])


# In[373]:


soc.rename({'Unit   Group': 'unit'}, axis=1, inplace = True)


# In[378]:


soc_health = soc.loc[soc.unit.isin(unit)]


# In[379]:


job_health = job.loc[job.SOC_occupation_code.isin(unit)]


# In[380]:


job_health = pd.merge(job_health,soc_health,left_on='SOC_occupation_code',right_on='unit').drop('SOC_occupation_code',axis=1)


# In[381]:


# for values w/o delete date, drop it
# job_health = job_health[pd.notnull(job_health['delete_date'])]


# In[382]:


job_health['created'] = pd.to_datetime(job_health.created)
#job_health['last_checked'] = pd.to_datetime(job_health.last_checked)
#job_health['delete_date'] = pd.to_datetime(job_health.delete_date)


# In[390]:


job_health['created_yr'] = job_health.created.dt.year
job_health['created_m'] = job_health.created.dt.month
# job_health['checked_yr'] = job_health.last_checked.dt.year
# job_health['checked_m'] = job_health.last_checked.dt.month
# job_health['deleted_yr'] = job_health.delete_date.dt.year
# job_health['deleted_m'] = job_health.delete_date.dt.month


# In[432]:


# after 2016, the job listings for health care
create = pd.DataFrame(job_health.groupby(['created_yr', 'created_m', 'unit']).count())
create =  create[['title']]
# checked = pd.DataFrame(job_health.groupby(['checked_yr', 'checked_m'])['unit'].count())
# deleted = pd.DataFrame(job_health.groupby(['deleted_yr', 'deleted_m'])['unit'].count())


# In[433]:


create.reset_index(inplace=True)
create.rename(columns = {'title': 'create_count'}, inplace = True)  
# checked.reset_index(inplace=True)
# checked.rename(columns = {'unit': 'check_count'}, inplace = True)
# deleted.reset_index(inplace=True)
# deleted.rename(columns = {'unit': 'delete_count'}, inplace = True)


# In[463]:


len(['0'+str(i) for i in c if len(i) == 1])


# In[471]:


c.values


# In[470]:


create.head()


# In[459]:


create.head()


# In[441]:


create.created_m[0] < 10
'0'+str(0)


# In[411]:


create['time'] = create['created_yr'].map(str) + " "+ create['created_m'].map(str)
# checked['time'] = checked['checked_yr'].map(str) + " "+ checked['checked_m'].map(str)
# deleted['time'] = deleted['deleted_yr'].map(str) + " "+ deleted['deleted_m'].map(str)


# In[413]:


create = create[['time','create_count','unit']] 
# checked = checked[['time','check_count']] 
# deleted = deleted[['time','delete_count']] 


# In[209]:


#job_count = pd.merge(create,checked,how='outer')


# In[210]:


#job_count = pd.merge(job_count,deleted,how='outer')


# In[419]:


create.index[create.time == '2017 11',][0]
job_count = create.iloc[create.index[create.time == '2017 11',][0]:]


# In[495]:


a = job_count.pivot(index = 'time', columns = 'unit', values = 'create_count')


# In[474]:


a.to_csv('job_count')


# In[222]:


# job_count_2016 = job_count.iloc[70:] #starting from 2016


# In[480]:


job_count_2016.info()


# In[483]:


job_count_2016.to_csv("job_count_2016.csv")


# In[482]:



fig,ax = plt.subplots(figsize=(20, 10))
ax.plot(job_count_2016.time, job_count_2016['delete_count'], color = 'b', alpha=0.8)
#ax.plot(job_count_2016.time, job_count_2016['delete_count'], color = 'b', alpha=0.8)
#ax.plot(job_count_2016.time, job_count_2016['check_count'], color = 'g', alpha=0.8)


# In[368]:


n = [[2212, 2213, 2214, 2215, 2221, 2231, 2232, 3217, 3218, 3219],[2111, 2112, 2113, 2114]]


# In[649]:


def job_type(n, job_health):
    type1 = job_health.loc[job_health['unit'].isin(n[0])] 
    type1['created'] = pd.to_datetime(type1.created)
    type1['created_yr'] = type1.created.dt.year
    type1['created_m'] = type1.created.dt.month
    create = pd.DataFrame(type1.groupby(['created_yr', 'created_m'])['unit'].count())
    create.reset_index(inplace=True)
    create.rename(columns = {'unit': 'create_count'}, inplace = True) 
    create['time'] = create['created_yr'].map(str) + " "+ create['created_m'].map(str)
    create = create[['time','create_count']] 
    job_count_2016 = create.iloc[70:]

    type2 = job_health.loc[job_health['unit'].isin(n[1])] 
    type2['created'] = pd.to_datetime(type2.created)
    type2['created_yr'] = type2.created.dt.year
    type2['created_m'] = type2.created.dt.month
    create2 = pd.DataFrame(type2.groupby(['created_yr', 'created_m'])['unit'].count())
    create2.reset_index(inplace=True)
    create2.rename(columns = {'unit': 'create_count'}, inplace = True) 
    create2['time'] = create2['created_yr'].map(str) + " "+ create2['created_m'].map(str)
    create2 = create2[['time','create_count']] 
    job_count_2016_2 = create2.iloc[70:]
    
    fig,ax = plt.subplots(figsize=(20, 10))
    ax.plot(range(job_count_2016.shape[0]), job_count_2016['create_count'],alpha=0.8)
    ax.plot(range(job_count_2016_2.shape[0]), job_count_2016_2['create_count'],alpha=0.8)
    ax.set_ylabel('number of jobs in health care')
    fig.savefig('ex.png')


# In[ ]:


plt.plot(job_count.time,job_count.create_count,job_count.time,job_count.check_count,job_count.time,job_count.delete_count)
plt.gca().legend(('Jobs Created','Jobs checked','Jobs deleted'))
plt.xlabel('Time')
plt.ylabel('Sum of Jobs Listed')
plt.title('Job Listings Statistics(Total) in Healthcare Each Year')
plt.show()


# In[650]:


job_type(n, job_health)


# In[599]:


employ =  pd.read_csv("yearly_data.csv")


# In[600]:


employ


# In[601]:


employ.year = employ.year.map(int)


# In[602]:


employ.year = employ.year+1


# In[603]:


employ.tail()


# In[604]:


a.head()


# In[633]:


a.to_csv('listing.csv')


# In[630]:


employ.year = employ.year.map(str)
c = pd.merge( a, employ, on = 'year', suffixes=['_L','_R'], how='left')


# In[627]:


c.iloc[:, 30:]


# In[607]:


c


# In[608]:


c.columns.values


# In[632]:


c.columns.values[30:]


# In[631]:


c.head()


# In[628]:


cols = c.columns.values


# In[629]:


cols


# In[555]:


int(cols[i]) == 1184


# In[556]:


c


# In[598]:


employ.head()


# In[ ]:


c


# In[538]:


c[1184] = c[1184.0]/c[1184] 


# In[609]:


cols = c.columns.values
for i in range(1, 30):
    for j in range(31, len(cols)):
        if int(cols[i]) == int(cols[j]):
            break
    c[cols[j]] = c[cols[i]]/c[cols[j]] 


# In[610]:


c.columns


# In[611]:


c.columns[30]


# In[612]:


rate = c.iloc[:,31: ]


# In[617]:


rate = rate.iloc[:,1:]


# In[619]:


rate.columns


# In[622]:


rate.head()


# In[624]:


aaa = rate.drop(['6145','6144'],axis=1)


# In[625]:


aaa.to_csv('rate.csv')


# In[523]:


c.head()


# In[496]:


a.reset_index(inplace=True)


# In[498]:


a['year'] = a['time'].str[:4]


# In[499]:




