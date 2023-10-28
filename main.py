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
    page_icon=":bar_chart:",
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
# print(df)
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
# print(unemployment_data.index)
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
# print(df_dates.index)
# print(type(df_dates.index))
# df_dates[0] = "Dates"
data_years = df[
    ["State"]
    + [col for col in df_dates.index if "2020" in col or "2021" in col or "2022" in col]
]
# print(type(data_years))
# print(data_years)


# data_years = pd.to_datetime(data_years, format="%Y-%m-%d").date
# df_dates.index = pd.to_datetime(df_dates.index, format="%Y-%m-%d").date
# print(data_years)

# year_list
# Convert the index to datetime and find the minimum and maximum dates
# Filter out non-date values and convert the index to datetime
# date_format = "%Y-%m-%d"
# # valid_dates = [date for date in df_dates.index if len(date) == len("YYYY-MM-DD")]
# df_dates.index = pd.to_datetime(df_dates.index, format=date_format, errors="coerce")

# valid_dates = pd.to_datetime(df_dates.index, format=date_format)

# # Find the minimum and maximum dates
# startDate = valid_dates.min()

# endDate = valid_dates.max()
# with col1:
#     date1 = pd.to_datetime(st.date_input("Start Date", startDate), format="%Y-%m-%d")
# with col2:
#     date2 = pd.to_datetime(st.date_input("End Date", endDate), format="%Y-%m-%d")
# filtered_df = df_dates.loc[(df_dates.index >= date1) & (df_dates.index <= date2), :]
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
non_index_df = df.reset_index(drop=True)
# df.rename(columns={"State": ""}, inplace=True)
non_index_df = non_index_df.T
dates_column = non_index_df.index.tolist()
non_index_df = non_index_df.reset_index(drop=True)
non_index_df.insert(0, "Dates", dates_column)
non_index_df["Dates"][0] = ""
# print(non_index_df)
print(non_index_df["Dates"].dtype)
# non_index_df = non_index_df.reset_index()
# datetime_list = [
#     datetime.strptime(date, "%Y-%m-%d %H:%M:%S") if index > 0 else date
#     for index, date in enumerate(non_index_df["Dates"])
# ]
non_index_df["Dates"] = non_index_df["Dates"].apply(
    lambda date: datetime.strptime(date, "%Y-%m-%d %H:%M:%S") if date else ""
)
# state_names = non_index_df.iloc[0].values
# # Filtrar las fechas y años que cumplan con la condición
# selected_state = st.selectbox(
#     "Selecciona un estado en USA", non_index_df[state_names]
# )  # Asume que las columnas desde la tercera son nombres de estado
# print(state_names)
# filtered_dates = [
#     date
#     for index, date in enumerate(non_index_df["Dates"])
#     if index > 0 and date.year > 2021
# ]


# Filtrar las fechas y años que cumplan con la condición
filtered_dates = [
    date
    for index, date in enumerate(non_index_df["Dates"])
    if index > 0 and date.year > 2021
]

# # Crear un selector para elegir un estado
# selected_state = st.selectbox(
#     "Selecciona un estado en USA",
#     non_index_df.columns[
#         2:
#     ],  # Asume que las columnas desde la tercera son nombres de estado
# )

# Crear un selector para elegir el período de estadísticas
start_date = st.date_input(
    "Selecciona la fecha de inicio",
    min_value=filtered_dates[0],
    max_value=filtered_dates[-1],
    value=filtered_dates[0],
)
end_date = st.date_input(
    "Selecciona la fecha de fin",
    min_value=filtered_dates[0],
    max_value=filtered_dates[-1],
    value=filtered_dates[-1],
)
# print(non_index_df.)

state_names = non_index_df.iloc[0][1:].tolist()

# Assuming that df is your DataFrame
# Set the column names to the values in the first row (index 0)
non_index_df.columns = non_index_df.iloc[0]

# Drop the first row (index 0) since it's now the column names
non_index_df = non_index_df.drop(0)


# Reset the index
non_index_df = non_index_df.reset_index(drop=True)
non_index_df = non_index_df.rename(columns={non_index_df.columns[0]: "Dates"})
# print(state_names)
# selected_state = st.selectbox("Selecciona un estado en USA", state_names)

# Crear un selector para elegir el estado
selected_state = st.selectbox("Selecciona un estado en USA", state_names[1:])
print(non_index_df)
# Obtener el porcentaje de desempleo para el estado seleccionado y el período elegido
unemployment_rates = [
    non_index_df.loc[index, selected_state]
    for index, date in enumerate(filtered_dates)
    if start_date <= date <= end_date
]

# Ahora puedes mostrar los resultados en Streamlit
st.write(
    "Porcentaje de desempleo en", selected_state, "desde", start_date, "hasta", end_date
)
st.line_chart(unemployment_rates)
