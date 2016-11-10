# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 13:37:57 2016

@author: Glenn
"""

import pandas as pd
from datetime import datetime

def get_unemp_data():
    csv = pd.read_csv("TABLECODE7080_Employment_Data.csv")
    groups = csv.groupby('Measure').size()
    #print(groups)
    
    m = pd.DataFrame()
    
    
    for grp in groups.keys():
        print (grp)
        m1 = csv[csv['Measure'] == grp]\
    [['Quarter', 'Value']].copy().rename(columns={'Value':grp})
    
        if m.empty:
            m = m1
        else:
            m = m.merge(m1, on='Quarter', how='outer')
    
    #print(m.head())  
    return m
    
def to_date(dstr, **kwargs):
    months = ['jan','feb','mar','apr','may', 'jun',
              'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    mon = dstr[0:3].lower()
    yr = int(dstr[4:6])
    if yr < 20: 
        yr += 2000
    else:
        yr += 1900
    midx = months.index(mon)+1
    dt = datetime(yr, midx, 1)
    return dt
    
#df = get_unemp_data()
#df.to_pickle("unemp.pickle")
df = pd.read_pickle("unemp.pickle")
df['Date'] = df['Quarter'].apply(to_date, axis=1)
del df['Quarter']
df.set_index('Date', inplace=True)
df.sort_index(inplace=True)
print (df.head()) 

