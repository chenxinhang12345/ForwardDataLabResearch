import pandas as pd
from math import sin, cos, acos, radians,sqrt,atan2
import numpy as np
df_addresses = pd.read_csv('zip_addresses.csv', sep = ";",header = None)
df_crimes = pd.read_csv('crime_data.csv',sep = ";", header = None)
#Each intersted zip contain zip code as a key and maxLat, minLat, maxLong, minLong as filter
interested_zip = {
    '60603':[41.882346,41.877981,-87.620488,-87.634367], 
    '60623':[41.867463,41.822105,-87.693089,-87.742227], 
    '60624':[41.896188,41.865003,-87.704546,-87.742398], 
    '60604':[41.880534,41.875294,-87.619984,-87.634618], 
    '60621':[41.795109,41.754967,-87.623804,-87.656171], 
    '60643':[41.737339,41.654613,-87.638203,-87.687782]}

['60603','60623','60624','60604','60621','60643']
def filt_with_zip(zip_code_list):
    df_all = pd.DataFrame()
    for zipcode in zip_code_list:
        df_f = pd.DataFrame()
        if zipcode in interested_zip:
            r = interested_zip[zipcode]
            max_lat = r[0]
            min_lat = r[1]
            max_long = r[2]
            min_long = r[3]
            df_f = df_crimes[df_crimes[14]< max_lat]
            df_f = df_f[df_f[14]> min_lat]
            df_f = df_f[df_f[15]< max_long]
            df_f = df_f[df_f[15]> min_long]
        df_all = df_all.append(df_f)
    return df_all
def distanceWithin(lat1,long1,lat2,long2, d):
    R = 6373.0
    lat1 = radians(lat1)
    lon1 = radians(long1)
    lat2 = radians(lat2)
    lon2 = radians(long2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance < d

def add_crime_occurrence(R,start,end):
    df_addresses['#crimes'] = 0 #initialize #crimes for each address as 0
    df_add_ll = df_addresses[[0,1]].values
    df_crimes_ll = df_crimes[[14,15]].values
    df_a = df_addresses.values
    s = {}
    for i in range(start,end):
        zipcode = df_a[i][6]
        if zipcode not in s and len(zipcode) == 5:
            s[zipcode] = filt_with_zip([zipcode])[[14,15]].values
        elif len(zipcode)!= 5:
            #dirty data
            continue
        df_range = s[zipcode]
        # print(df_range)
        count = 0
        for j in range( len(df_range)):
            if np.isnan(df_crimes_ll[j][0]):
                continue
            if distanceWithin(df_range[j][0],df_range[j][1],df_add_ll[i][1],df_add_ll[i][0],R):
                count+=1
        print(count)
        df_addresses['#crimes'][i] = count
df_crimes = filt_with_zip(['60603','60623','60624','60604','60621','60643'])
add_crime_occurrence(0.1,0,len(df_addresses.values))
df_addresses.to_csv('zip_addresses_crime.csv')
