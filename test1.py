import numpy as np 
import pandas as pd

dataPath = 'E:/datathon/'
df = pd.read_csv(dataPath + 'soc_code_legend.csv')
sub_major = [22]
minor_list = [321,356,118,614]
sub_minor = [2463,3567,6121]
df["Minor Group"] = na_to_num(df['Minor Group'].astype(int))

minor_finallist = df.loc[df['Minor Group'].isin(minor_list),:]['Unit   Group'].dropna().drop_duplicates()
final2 = df.loc[df['Sub-Major Group'].isin(sub_major),:]['Unit   Group'].dropna().drop_duplicates()
final = set(list(minor_finallist) + list(final2) + sub_minor)

empl_occ = pd.read_csv(dataPath + 'employment_by_occupation.csv')
health_occ = empl_occ.loc[empl_occ["soc_occupation_code"].isin(final),:]
health_occ_year = health_occ['value'].groupby([health_occ['year'],health_occ['soc_occupation_code']]).sum()

fin1 = health_occ['value'].groupby([health_occ['year']]).sum()
fin2 = health_occ['value'].groupby([health_occ['year'],health_occ['sex']]).sum()


########market cap



female = [2149002.0,2361311.0,2508966.0,2585023.0,2614510.0,2680041.0,2775839.0,2761805.0]
male = [605796.0,701173.0,711290.0,805967.0,770134.0, 816095.0,853669.0,743643.0]

n_groups = 8

# create plot
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.35
opacity = 0.8

rects1 = plt.bar(index, male, bar_width,
alpha=opacity,
color='b',
label='male')

rects2 = plt.bar(index + bar_width, female, bar_width,
alpha=opacity,
color='g',
label='female')

plt.xlabel('Year')
plt.ylabel('Sum of employers')
plt.title('Employment Statistics in Healthcare Each Year')
plt.xticks(index + bar_width, ('2011', '2012', '2013', '2014', '2015', '2016','2017','2018'))
plt.legend()

plt.tight_layout()
plt.show()



dataPath = 'E:/datathon/'
df_cap = pd.read_csv(dataPath + 'lse_historical_data.csv')
df_cap_health = df_cap.loc[df_cap['ice_supersector']=='Health Care',:]