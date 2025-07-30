import pandas as pd
import streamlit as st
from plotnine import ggplot, aes, geom_line, ggtitle, guides, geom_point, annotate

wpp_median_2022 = pd.read_csv('WPP_2022_Median_clean.csv')
wpp_low_2022 = pd.read_csv('WPP_2022_Low_clean.csv')

wpp_median_2024 = pd.read_csv('WPP_2024_Median_clean.csv')
wpp_low_2024 = pd.read_csv('WPP_2024_Low_clean.csv')

vital_statistics = pd.read_csv('vital_statistics.csv',encoding='unicode_escape')

#Main Site Creation
st.title("WPP 2022 vs 2024 Revision")

#Generate a unique list of countries and variables for the dropdown menus
country_filt = (wpp_median_2022["Year"]==2010)
country_list = wpp_median_2022.loc[country_filt,"Country"].values
variable_list = wpp_median_2022.columns[10:-2] #Only want numerical columns as options for display

selected_country = st.selectbox('Country/Region', country_list) #Dropdown list of countries
selected_variable = st.selectbox('Variable', variable_list) #Dropdown list of variables

#Plotting Based on User Selections
location_code = wpp_median_2022.loc[wpp_median_2022["Country"]==selected_country,"Location code"]
location_code = location_code.iloc[0]
wpp_median_2022 = wpp_median_2022.loc[wpp_median_2022["Location code"]==location_code]
wpp_low_2022 = wpp_low_2022.loc[wpp_low_2022["Location code"]==location_code]
wpp_median_2024 = wpp_median_2024.loc[wpp_median_2024["Location code"]==location_code]
wpp_low_2024 = wpp_low_2024.loc[wpp_low_2024["Location code"]==location_code]
vital_statistics = vital_statistics[vital_statistics["Country"]==selected_country]


st.write("Include:")
med_2024_selected = st.checkbox("2024 Revision, Medium Variant",value=True)
med_2022_selected = st.checkbox("2022 Revision, Medium Variant",value=True)
low_2024_selected = st.checkbox("2024 Revision, Low Variant")
low_2022_selected = st.checkbox("2022 Revision, Low Variant")
vital_stats_selected = False
if len(vital_statistics)>0:
    vital_stats_selected = st.checkbox("Vital Statistics",value=True)

#Set Axes
year_limits = st.slider("Select a range for display",1950, 2100, (1950, 2100))

#Only want user-selected variant(s)
wpp_median_2022['selected_variant'] = med_2022_selected
wpp_low_2022['selected_variant'] = low_2022_selected
wpp_median_2024['selected_variant'] = med_2024_selected
wpp_low_2024['selected_variant'] = low_2024_selected
full_df = pd.concat([wpp_median_2022,wpp_low_2022,wpp_median_2024,wpp_low_2024])
full_df = full_df.loc[full_df['selected_variant']==True]

#User Selected Years
year_filter_lb = full_df['Year']>=year_limits[0] 
full_df = full_df.loc[year_filter_lb]
year_filter_ub = full_df['Year']<=year_limits[1]
full_df = full_df.loc[year_filter_ub]

p=ggplot(data = full_df,mapping=aes(x="Year",y=f"{selected_variable}")) + geom_line(aes(color='Variant', linetype = "Projection"))

if vital_stats_selected:
    vital_stats_row = vital_statistics
    if not vital_stats_row.empty:
        vital_stat_row_one = vital_stats_row.iloc[0]
        vital_stat_row_two = vital_stats_row.iloc[1]
        if (not vital_stat_row_one.empty) and (float(vital_stat_row_one[selected_variable])>0):
            p = p + geom_point(aes(x=vital_stat_row_one["Year"],y=float(vital_stat_row_one[f"{selected_variable}"])),color="black")
            if (year_limits[1]-year_limits[0] <= 30) and (year_limits[0]<=2023) and (year_limits[1]>=2024):
                p = p + annotate("text",x=1.5+vital_stat_row_one["Year"],y=float(vital_stat_row_one[f"{selected_variable}"]),label="2023") 
        if (not vital_stat_row_two.empty) and (float(vital_stat_row_two[selected_variable])>0):
            p = p + geom_point(aes(x=vital_stat_row_two["Year"],y=float(vital_stat_row_two[f"{selected_variable}"])),color="black")
            if (year_limits[1]-year_limits[0] <= 30) and (year_limits[0]<=2023) and (year_limits[1]>=2024):
                p = p + annotate("text",x=1.5+vital_stat_row_two["Year"],y=float(vital_stat_row_two[f"{selected_variable}"]),label="2024")


p = p + ggtitle(f"{selected_country}, {selected_variable}") + guides(linetype="none")

st.pyplot(ggplot.draw(p))