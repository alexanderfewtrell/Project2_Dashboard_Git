import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from st_aggrid import AgGrid, GridOptionsBuilder
import numpy as np
#st.write('Project 2 Dashboard')
import pickle

def pickleGraph(fig, filename):
    with open(str(filename) + ".pkl", 'wb') as f:
        graph = pickle.dump(fig,f)
    #return graph

def openPickleGraph(filename):
    with open(str(filename) + ".pkl", 'rb') as f:
        fig = pickle.load(f)

    return fig


tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Overview", "Data", "Price Comparison over time", "Comparison by Country", "Comparison Each Year", "Variable Comparison per Year", "Scatter Plot"])

data = pd.read_csv('https://github.com/alexanderfewtrell/Data315_Project2/raw/refs/heads/main/completed_data.csv')
UKMap = gpd.read_file("https://github.com/alexanderfewtrell/Data315_Project2/raw/refs/heads/main/CTRY_DEC_2021_UK_BUC.shp")
USMap = gpd.read_file("https://github.com/alexanderfewtrell/Data350/raw/refs/heads/main/tl_2025_us_state/tl_2025_us_state.dbf")
MainlandUSMap = USMap.drop(USMap[(USMap['NAME'] == "Alaska") | (USMap['NAME'] == "Hawaii")| (USMap['NAME'] == "United States Virgin Islands") | (USMap['NAME'] == "American Samoa") | (USMap['NAME'] == "Commonwealth of the Northern Mariana Islands") | (USMap['NAME'] == "Guam") | (USMap['NAME'] == "Puerto Rico")].index)
UKMap = UKMap.set_crs("EPSG:27700")
UKMap = UKMap.to_crs(USMap.crs)

price_options = ['UK Price Diesel ($/Gallon)',
                 'UK Price Diesel (£/Litre)',
                 'UK Price Petrol ($/Gallon)',
                 'UK Price Petrol (£/Litre)',
                 'US Price Petrol ($/Gallon)',
                 'US Price Petrol (£/Litre)',
                 'US Price Diesel ($/Gallon)',
                 'US Price Diesel (£/Litre)']

with tab1:
    st.markdown('''
    # Project 2 Dashboard
    ##### UK vs US fuel Prices since 2003
    ##### By Alexander Fewtrell
    # 
    # 
    ##### Sources
    ''')
    st.write("All Data on Github - https://github.com/alexanderfewtrell/Data315_Project2")
    st.write("UK Fuel - https://www.gov.uk/government/statistics/weekly-road-fuel-prices")
    st.write("US Diesel - https://www.macrotrends.net/4394/us-diesel-fuel-prices")
    st.write("US Petrol - https://www.macrotrends.net/3591/us-gasoline-prices")

with tab2:

    st.markdown('''
    ###### This is the data I will be working with.  It contains fuel prices in the UK and US since 2003.  i will be using this data to explore how fuel prices have changed over time, and how they differ between the two countries.
    ###### It is displayed in both £/Litre as well as $/Gallon
    ###### I used £1 = $1.35 as a conversion rate
    ''')
    #st.dataframe(data)

    editable_data = GridOptionsBuilder.from_dataframe(data)

    editable_data.configure_default_column(filter=True, sortable=True, resizable=True)

    grid_options = editable_data.build()

    AgGrid(data, gridOptions=grid_options, height=300)

with tab3:
    st.header("Variable Comparison over time")

    dropdown_choice1 = st.selectbox("Select a Variable",
                                    price_options,
                                    key = "dropdown_choice1")
    st.markdown(f"You selected {dropdown_choice1}")

    dropdown_choice2 = st.selectbox("Select a Variable",
                                    price_options,
                                    key = "dropdown_choice2")

    st.markdown(f"You selected {dropdown_choice2}")

    fig, ax = plt.subplots()

    ax.plot(data["Year"], data[dropdown_choice1], label=dropdown_choice1)
    ax.plot(data["Year"], data[dropdown_choice2], label=dropdown_choice2)

    ax.set_xlabel("Year")
    ax.set_ylabel("Price")
    ax.legend()

    st.pyplot(fig)

with tab4:
    dropdown_choice_Fuel_Type = st.selectbox("Select a Variable",
                                             ['Diesel ($/Gallon)',
                                              'Diesel (£/Litre)',
                                              'Petrol ($/Gallon)',
                                              'Petrol (£/Litre)'],
                                            key = "dropdown_choice_Fuel_Type")

    st.markdown(f"You selected {dropdown_choice_Fuel_Type}")

    if dropdown_choice_Fuel_Type == "Diesel ($/Gallon)":
         UKVar = "UK Price Diesel ($/Gallon)"
         USVar = "US Price Diesel ($/Gallon)"
    elif dropdown_choice_Fuel_Type == "Diesel (£/Litre)":
         UKVar = "UK Price Diesel (£/Litre)"
         USVar = "US Price Diesel (£/Litre)"
    elif dropdown_choice_Fuel_Type == "Petrol ($/Gallon)":
         UKVar = "UK Price Petrol ($/Gallon)"
         USVar = "US Price Petrol ($/Gallon)"
    elif dropdown_choice_Fuel_Type == "Petrol (£/Litre)":
         UKVar = "UK Price Petrol (£/Litre)"
         USVar = "US Price Petrol (£/Litre)"

    var_data = data[[UKVar, USVar, "Year"]]

    year_slider_map = st.slider(
         "Select Year",
         int(var_data["Year"].min()),
         int(var_data["Year"].max()),
         key="year_slider_map"
    )
    year_data = var_data[var_data["Year"] == year_slider_map]

    UKAverage = year_data[UKVar].mean()
    USAverage = year_data[USVar].mean()

    UKMap["UKAverage"] = UKAverage
    MainlandUSMap["USAverage"] = USAverage

    if data[USVar].max() > data[UKVar].max():
        MAX = data[USVar].max()
    else:
        MAX = data[UKVar].max()

    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots(figsize=(10, 6))
        UKMap.plot(
            column="UKAverage",
            legend=True,
            cmap="Blues",
            vmin=0,
            vmax=MAX,
            ax=ax
        )
        ax.set_axis_off()
        st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots(figsize=(10, 6))
        MainlandUSMap.plot(
            column="USAverage",
            legend=True,
            cmap="Blues",
            vmin=0,
            vmax=MAX,
            ax=ax
        )
        ax.set_axis_off()
        st.pyplot(fig)

with tab5:

    if "dropdown_choice1Year" not in st.session_state:
        st.session_state.dropdown_choice1Year = price_options[0]

    # Set default value for second variable
    if "dropdown_choice2Year" not in st.session_state:
        st.session_state.dropdown_choice2Year = price_options[1]

    with st.form("comparison_form"):
        new_dropdown_choice1Year = st.selectbox(
            "Select a Variable",
            price_options,
            index=price_options.index(st.session_state.dropdown_choice1Year))#,
            #key = "dropdown_choice1Year")

        st.markdown(f"You selected {new_dropdown_choice1Year}")

        new_dropdown_choice2Year = st.selectbox(
            "Select a Variable",
            price_options,
            index=price_options.index(st.session_state.dropdown_choice2Year))#,
            #key = "dropdown_choice2Year")

        st.markdown(f"You selected {new_dropdown_choice2Year}")

        submitted = st.form_submit_button("Update Graph")

    if submitted:
        st.session_state.dropdown_choice1Year = new_dropdown_choice1Year
        st.session_state.dropdown_choice2Year = new_dropdown_choice2Year

    st.header("Variable Comparison over a year")
    year_slider = st.slider(
        "Select Year",
        int(data["Year"].min()),
        int(data["Year"].max()),
        value=int(data["Year"].min()),
        key = "Year_Slider"
    )

    year_data = data[data["Year"] == year_slider]

    fig, ax = plt.subplots()

    ax.plot(year_data["Month"], year_data[new_dropdown_choice1Year], label=new_dropdown_choice1Year)
    ax.plot(year_data["Month"], year_data[new_dropdown_choice2Year], label=new_dropdown_choice2Year)

    ax.set_xlabel("Month")
    ax.set_ylabel("Price")
    ax.legend()

    st.pyplot(fig)

with tab6:
    years = ["2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014",
             "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025", "2026"]
    Year_dropdown = st.selectbox("Select a Variable",
                                    years,
                                    key = "Year_dropdown")

    st.markdown(f"You selected {Year_dropdown}")

    Variable_dropdown = st.selectbox("Select a Variable",
                                    ["£/Litre", "$/Gallon"],
                                    key = "Variable_dropdown")

    st.markdown(f"You selected {Variable_dropdown}")

    year_data = data[data["Year"] == int(Year_dropdown)]

    UKPetrolDolG = year_data["UK Price Petrol ($/Gallon)"].mean()
    USPetrolDolG = year_data["US Price Petrol ($/Gallon)"].mean()
    UKDieselDolG = year_data["UK Price Diesel ($/Gallon)"].mean()
    USDieselDolG = year_data["US Price Diesel ($/Gallon)"].mean()
    UKPetrolPndL = year_data["UK Price Petrol (£/Litre)"].mean()
    USPetrolPndL = year_data["US Price Petrol (£/Litre)"].mean()
    UKDieselPndL = year_data["UK Price Diesel (£/Litre)"].mean()
    USDieselPndL = year_data["US Price Diesel (£/Litre)"].mean()

    if Variable_dropdown == "£/Litre":

        fig, ax = plt.subplots()

        ax.bar(
            ["UK Price Petrol (£/Litre)","US Price Petrol (£/Litre)","UK Price Diesel (£/Litre)","US Price Diesel (£/Litre)"],
            [UKPetrolPndL,USPetrolPndL,UKDieselPndL,USDieselPndL])

        plt.xticks(rotation=90)
        ax.set_title("Bar Chart for all values in " + Variable_dropdown + " for " + Year_dropdown)
        ax.set_xlabel("Variables")
        ax.set_ylabel("Price")

        st.pyplot(fig)

    elif Variable_dropdown == "$/Gallon":

        fig, ax = plt.subplots()

        ax.bar(
            ["UK Price Petrol ($/Gallon)", "US Price Petrol ($/Gallon)", "UK Price Diesel ($/Gallon)", "US Price Diesel ($/Gallon)"],
            [UKPetrolDolG, USPetrolDolG, UKDieselDolG, USDieselDolG,])

        plt.xticks(rotation=90)
        ax.set_title("Bar Chart for all values in " + Variable_dropdown + " for " + Year_dropdown)
        ax.set_xlabel("Variables")
        ax.set_ylabel("Price")

        st.pyplot(fig)

with tab7:

    Var_dropdown = st.selectbox("Select a Variable",
                                    price_options,
                                    key = "Var_dropdown")
    st.markdown(f"You selected {Var_dropdown}")

    #columns_to_plot = price_options

    m, b = np.polyfit(data["Year"], data[Var_dropdown], 1)

    x_line = np.linspace(data["Year"].min(), data["Year"].max(), 100)
    y_line = m * x_line + b

    fig, ax = plt.subplots()

    ax.scatter(data["Year"], data[Var_dropdown], label="Var_dropdown", alpha=0.5)
    ax.plot(x_line, y_line, color="red", label="Best fit line")

    ax.set_title("Scatter Plot to show " + Var_dropdown + " over time")
    ax.set_xlabel("Year")
    ax.set_ylabel("Price")

    st.pyplot(fig)
