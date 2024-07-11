#Cleans the Raw WPP data from the UNPD Website to make plotting easier (https://population.un.org/wpp/Download/Standard/MostUsed/)
#Rafactoring into separate script for application speed
import pandas as pd

wpp_estimates_2022 = pd.read_csv('WPP_2022_Estimates_raw.csv',encoding='latin-1',low_memory=False)
wpp_median_2022 = pd.read_csv('WPP_2022_Median_raw.csv',encoding='latin-1',low_memory=False)
wpp_low_2022 = pd.read_csv('WPP_2022_Low_raw.csv',encoding='latin-1',low_memory=False)

wpp_median_2022 = pd.concat([wpp_estimates_2022,wpp_median_2022])
wpp_low_2022 = pd.concat([wpp_estimates_2022,wpp_low_2022])

#Add indicator variable for which variant is used
wpp_median_2022['Variant'] = '2022 Median'
wpp_low_2022['Variant'] = '2022 Low'

#Indicator variable for projection vs estimate
wpp_median_2022['Projection'] = wpp_median_2022['Year']>2021
wpp_low_2022['Projection'] = wpp_low_2022['Year']>2021

#Rename Columns
wpp_median_2022.rename(columns={'Region, subregion, country or area *':'Country'}, inplace=True)
wpp_low_2022.rename(columns={'Region, subregion, country or area *':'Country'}, inplace=True)

#Clean Data: Convert strings to numeric and drop NaNs
cols = wpp_median_2022.columns.drop(['Index','Variant','Country','Notes','Location code','ISO3 Alpha-code','ISO2 Alpha-code','SDMX code**','Type','Parent code','Year','Variant'])

wpp_median_2022.replace('...',0, inplace=True)
wpp_median_2022[cols] = wpp_median_2022[cols].apply(pd.to_numeric)

wpp_low_2022.replace('...',0, inplace=True)
wpp_low_2022[cols] = wpp_low_2022[cols].apply(pd.to_numeric)

#Drop Notes column
wpp_median_2022 = wpp_median_2022.drop('Notes', axis='columns')
wpp_low_2022 = wpp_low_2022.drop('Notes', axis='columns')

wpp_median_2022.to_csv('WPP_2022_Median_clean.csv',index=False)
wpp_low_2022.to_csv('WPP_2022_Low_clean.csv',index=False)
