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
from datetime import datetime

warnings.filterwarnings("ignore")


st.set_page_config(
    page_title="Desempleo en los estados unidos durante los ultimos 3 años",
    page_icon=":bar-chart:",
    layout="wide",
)
# Set the path to the "static" folder
# st.set_option("server.staticPath", "static")

# Print the contents of the "static" folder
st.write(os.listdir("static"))

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
    default_file_path = os.path.join("static", "new_unemployment_df.csv")
    df = pd.read_csv(default_file_path, encoding="ISO-8859-1")

col1, col2 = st.columns((2))
# df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d", errors="coerce")
print(df)
# data_2022 = df[(df['Date'] >= '2022-01-01') & (df['Date'] <= '2022-12-31')]
df.set_index("Code", inplace=True)
# print(df)


date_columns = [col for col in df.columns if col != "State" and col != "Code"]
# print(date_columns)
st.sidebar.header("Filtrar Datos")


# filtered_data = df[
#     (df[selected_year] == selected_month) & (df[selected_year] == selected_day)
# ]

# # Filtrar las filas por estado
selected_state = st.sidebar.selectbox("Selecciona el estado", df["State"].unique())
# filtered_data = filtered_data[filtered_data["State"] == selected_state]


data_2022 = df[["State"] + [col for col in df.columns if "2022" in col]]
average_unemployment_2022 = df[[col for col in df.columns if "2022" in col]].mean(
    axis=1
)

# # Select columns for the years 2020, 2021, and 2022
# data_years = df[
#     ["State"]
#     + [col for col in df.columns if "2020" in col or "2021" in col or "2022" in col]
# ]

# # Calculate the average unemployment rate for each year
# average_unemployment_2020 = (
#     data_years[[col for col in data_years.columns if "2020" in col]]
#     .mean(axis=1)
#     .round(2)
# )
# average_unemployment_2021 = (
#     data_years[[col for col in data_years.columns if "2021" in col]]
#     .mean(axis=1)
#     .round(2)
# )
# average_unemployment_2022 = (
#     data_years[[col for col in data_years.columns if "2022" in col]]
#     .mean(axis=1)
#     .round(2)
# )

# Now you have the average unemployment rates for each year
# print(type(average_unemployment_2020))
# print(average_unemployment_2021)
# print(average_unemployment_2022)


# data = pd.concat(
#     [average_unemployment_2020, average_unemployment_2021, average_unemployment_2022],
#     axis=1,
# )
# data.columns = ["Unemployment 2020", "Unemployment 2021", "Unemployment 2022"]
# print(data.T.shape[0])
# unemployment
# print(data_2022)
# average_unemployment_2023 = data_2022.mean(axis=0)
# print(data_2022)
# print(unemployment_by_state)
unemployment_data = pd.DataFrame(
    {
        "code": average_unemployment_2022.index,
        "unemployment_rate": average_unemployment_2022.values,
    }
)
print(unemployment_data.index)
fig = px.choropleth(
    unemployment_data,
    locations="code",
    locationmode="USA-states",
    color="unemployment_rate",
    scope="usa",
    title=f"Unemployment Rate in {selected_state} by State",
)

# fig.show()
df_dates = df.copy()
# df_dates.reset_index(drop=True, inplace=True)
# df_dates = df_dates.rename_axis("Dates")  # Rename the index
df_dates = df_dates.rename(columns={df_dates.columns[0]: "Dates"})
df_dates = df_dates.T  # Transpose the DataFrame
# df_dates.columns = df_dates.iloc[0]  # Set the first row as the column headers
df_dates = df_dates.iloc[1:]  # Remove the first row
print(df_dates.index)
print(type(df_dates.index))
# df_dates[0] = "Dates"
data_years = df[
    ["State"]
    + [col for col in df_dates.index if "2020" in col or "2021" in col or "2022" in col]
]
print(type(data_years))
# print(data_years)


# data_years = pd.to_datetime(data_years, format="%Y-%m-%d").date
# df_dates.index = pd.to_datetime(df_dates.index, format="%Y-%m-%d").date
# print(data_years)

# year_list
# Convert the index to datetime and find the minimum and maximum dates
# Filter out non-date values and convert the index to datetime
date_format = "%Y-%m-%d"
# valid_dates = [date for date in df_dates.index if len(date) == len("YYYY-MM-DD")]
df_dates.index = pd.to_datetime(df_dates.index, format=date_format, errors="coerce")

valid_dates = pd.to_datetime(df_dates.index, format=date_format)

# Find the minimum and maximum dates
startDate = valid_dates.min()

endDate = valid_dates.max()
with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate), format="%Y-%m-%d")
with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate), format="%Y-%m-%d")
filtered_df = df_dates.loc[(df_dates.index >= date1) & (df_dates.index <= date2), :]
st.sidebar.header("Chose your filter: ")


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
st.plotly_chart(fig)

# if selected_state:
#     # Access and display the information from the selected column
#     state_name = selected_state  # Assuming only one state is selected
#     state_info = df.loc[selected_state]
#     filtered_df = df[df.index == selected_state]
#     print(df)
# non_index_df = df.reset_index(drop=True)
non_index_df = df.set_index("State").T
print(non_index_df.reset_index().index)
timestamps = [
    datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").timestamp()
    for date_str in non_index_df.index
]
timestamps = [datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d") for ts in timestamps]
non_index_df["Timestamps"] = timestamps
non_index_df = non_index_df.set_index("Timestamps")
print(non_index_df)

# filtered_df = filtered_df.reset_index()


# # Define colors for the selected state and others
# colors = [selected_state] + ["lightgrey"] * (len(column_names) - 1)
# fig.update_traces(marker=dict(colors=colors))
# # Display the choropleth map

# Filtra tus datos según el estado seleccionado
# if selected_state:
#     state_data = df[df["State"] == selected_state["points"][0]["location"]]
#     st.write(state_data)
