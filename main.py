# import re

# """
# Documentation for the regex challenge I'm about the deal
# with hopping I can get more comfortable in searching and
# extracting data from medical reports

# """


# # !FIrst challenge: Email validator:
# pattern = r"([a-zA-Z0-9_.+-]+)@([a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"


# def check_email_valid_regex(email: str) -> bool:
#     """_summary_Function has to perform an email check validation using RegEx as the main goal from this challenge
#     So we both can get ourselves better in this sort of thing
#     """
#     print("|-------------------------------------------|")
#     print("|--------Email regEx validator--------------|")
#     print("|-------------------------------------------|")
#     if re.match(pattern, email):
#         print("|-------------------------------------------|")
#         print("|---------------User's Email----------------|")
#         print("|-------------------------------------------|")
#         return f"{email} valid"
#     # except:
#     return f"{email} not valid"


# email_to_check = "localhost@admin.com"
# result = check_email_valid_regex(email_to_check)
# print(result)
import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings

warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="Desempleo en los estados unidos durante los ultimos 3 años",
    page_icon=":bar-chart:",
    layout="wide",
)

st.title(
    ":bar_chart: Niveles de desempleo en Estados Unidos",
)
st.markdown(
    "<style>div.block-container{padding-top:1rem;}</style>", unsafe_allow_html=True
)

fl = st.file_uploader(
    ":file_folder: Upload a file", type=(["csv", "txt", "xlsx", "xls"])
)
if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(filename, encoding="ISO-8859-1")
else:
    os.chdir(r"D:\S-P-500-")
    df = pd.read_csv("participation_states.csv", encoding="ISO-8859-1")

col1, col2 = st.columns((2))
df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d", errors="coerce")
# print(df["Date"])

# print(dates)
startDate = pd.to_datetime(df["Date"], format="%Y-%m-%d").min()
endDate = pd.to_datetime(df["Date"], format="%Y-%m-%d").max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))
with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))
filtered_df = df[(df["Date"] >= date1) & (df["Date"] <= date2)].copy()
st.sidebar.header("Chose your filter: ")
column_names = df.columns
selected_state = st.sidebar.multiselect("Pick up your state", column_names)

# Create a choropleth map
# fig = px.choropleth(
#     filtered_df,
#     locations="Date",  # X-axis variable
#     locationmode="USA-states",
#     color=selected_state,  # Y-axis variable (color represents unemployment rate)
#     scope="usa",  # Set the map scope to USA
#     title=f"Unemployment Rate in {selected_state} by State",
# )

# # Display the choropleth map
# st.plotly_chart(fig)
print(df)
if selected_state:
    # Access and display the information from the selected column
    state_name = selected_state[0]  # Assuming only one state is selected
    state_column = filtered_df[state_name]
    filtered_df = filtered_df.reset_index()
    # Create a choropleth map without the "Date" column
    fig = px.choropleth(
        filtered_df,
        color=state_column,  # Y-axis variable is the selected state's unemployment rate
        locationmode="USA-states",
        locations=filtered_df.index,  # You need a unique identifier for each state
        scope="usa",  # Set the map scope to USA
        title=f"Unemployment Rate in {state_name} by State",
        hover_data=[selected_state],
    )

    # Define colors for the selected state and others
    colors = [selected_state] + ["lightgrey"] * (len(column_names) - 1)
    fig.update_traces(marker=dict(colors=colors))
    # Display the choropleth map
    st.plotly_chart(fig)
# Filtra tus datos según el estado seleccionado
if selected_state:
    state_data = df[df["State"] == selected_state["points"][0]["location"]]
    st.write(state_data)
