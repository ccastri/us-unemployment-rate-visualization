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
# st.write(os.listdir("static"))

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

# # Filtrar las filas por estado
selected_state = st.sidebar.selectbox("Selecciona el estado", df["State"].unique())
# filtered_data = filtered_data[filtered_data["State"] == selected_state]


data_2022 = df[["State"] + [col for col in df.columns if "2022" in col]]
average_unemployment_2022 = df[[col for col in df.columns if "2022" in col]].mean(
    axis=1
)


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

st.sidebar.header("Chose your filter: ")


# Display the choropleth map
st.plotly_chart(fig)


non_index_df = df.reset_index(drop=True)

non_index_df = non_index_df.T
dates_column = non_index_df.index.tolist()
non_index_df = non_index_df.reset_index(drop=True)
non_index_df.insert(0, "Dates", dates_column)
non_index_df["Dates"][0] = ""
# print(non_index_df)
print(non_index_df["Dates"].dtype)

non_index_df["Dates"] = non_index_df["Dates"].apply(
    lambda date: datetime.strptime(date, "%Y-%m-%d %H:%M:%S").date() if date else ""
)


# Filtrar las fechas y años que cumplan con la condición
filtered_dates = [
    date.date() if isinstance(date, pd.Timestamp) else date
    for index, date in enumerate(non_index_df["Dates"])
    if index > 0 and (isinstance(date, pd.Timestamp) or date.year > 2021)
]

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
print(filtered_dates)

state_names = non_index_df.iloc[0][1:].tolist()


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
if selected_state:
    # Access and display the information from the selected column
    state_name = selected_state  # Assuming only one state is selected
    # state_info = non_index_df.loc[selected_state]
    # filtered_df = non_index_df[non_index_df.index == selected_state]
    print(selected_state)
print(non_index_df.T)
non_index_df.rename(columns={"Dates": "State"}, inplace=True)
print(non_index_df.T)
# Obtener el porcentaje de desempleo para el estado seleccionado y el período elegido
unemployment_rates = [
    non_index_df.loc[index, selected_state]
    for index, date in enumerate(filtered_dates)
    if start_date <= date <= end_date
]
print(type(filtered_dates[0]))
print(type(start_date))
print(type(end_date))

# Ahora puedes mostrar los resultados en Streamlit
st.write(
    f"Porcentaje de desempleo en, {selected_state}, desde, {start_date}, hasta, {end_date}"
)
st.line_chart(unemployment_rates)
