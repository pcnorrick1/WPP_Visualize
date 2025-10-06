# WPP_Visualize

A web-app for comparing vital statistics data with projections made by the United Nations in 2022 and 2024 in their **World Population Prospects (WPP)**

**Live App:**
[https://pcnorrick1-wpp-visualize-wpp-visualize-pm0yuk.streamlit.app/](https://pcnorrick1-wpp-visualize-wpp-visualize-pm0yuk.streamlit.app/)

______________________________________________________________________

### About

This repository contains the code and processed dataset used to generate the visualizations in the app above.

Used for comparing the United Nations Population Division's World Population Prospects (WPP)
[2022 Revision](https://population.un.org/wpp/downloads?folder=Archive&group=Standard%20Projections)
with the
[2024 Revision](https://population.un.org/wpp/downloads?folder=Standard%20Projections&group=Most%20used)

______________________________________________________________________

### Structure

app/ -> Streamlit app (`wpp_visualize.py`)\
src/ -> Data cleaning script (`clean_wpp_data.py`)\
data/\
|--raw/ -> Original WPP data (not tracked)\
|--processed/ -> Cleaned data used by the app\
docs/ -> Hand-compiled birth data with sources

______________________________________________________________________

### Data Sources

The file\
[`docs/2023-24-vital-statistics-compiled.xlsx`](docs/2023-24-vital-statistics-compiled.xlsx)\
contains the manually compiled vital statistic birth data for every country I could find it for\
(Last Updated 7/29/2025 by author)\
This file is **not used in the code**, but is included for transparency.

