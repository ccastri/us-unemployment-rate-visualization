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


df.set_index("Code", inplace=True)
st.sidebar.header("Filtrar Datos")


average_unemployment_2022 = df[[col for col in df.columns if "2022" in col]].mean(
    axis=1
)


unemployment_data = pd.DataFrame(
    {
        "code": average_unemployment_2022.index,
        "unemployment_rate": average_unemployment_2022.values,
    }
)


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
    if index > 0 and (isinstance(date, pd.Timestamp) or date.year > 2000)
]

# Crear un selector para elegir el período de estadísticas
start_date = st.sidebar.date_input(
    "Selecciona la fecha de inicio",
    min_value=filtered_dates[0],
    max_value=filtered_dates[-1],
    value=filtered_dates[0],
)
end_date = st.sidebar.date_input(
    "Selecciona la fecha de fin",
    min_value=filtered_dates[0],
    max_value=filtered_dates[-1],
    value=filtered_dates[-1],
)
# print(filtered_dates)

state_names = non_index_df.iloc[0][1:].tolist()


# Set the column names to the values in the first row (index 0)
non_index_df.columns = non_index_df.iloc[0]

# Drop the first row (index 0) since it's now the column names
non_index_df = non_index_df.drop(0)


# Reset the index
non_index_df = non_index_df.reset_index(drop=True)


st.dataframe(non_index_df)


# print(non_index_df)

selected_states = st.sidebar.multiselect("Selecciona estados en USA", state_names[1:])
# print(unemployment_data.index)
fig = px.choropleth(
    unemployment_data,
    locations="code",
    locationmode="USA-states",
    color="unemployment_rate",
    scope="usa",
    title=f"Unemployment Rate in {selected_states} by State",
)

st.sidebar.header("Chose your filter: ")


# Display the choropleth map
st.plotly_chart(fig)

data_dict = {}

for state in selected_states:
    state_data = [
        non_index_df.loc[index, state]
        for index, date in enumerate(filtered_dates)
        if start_date <= date <= end_date
    ]
    data_dict[state] = state_data
    # subset_df = non_index_df[selected_states]


# Plot line charts for each selected state
for state, state_data in data_dict.items():
    st.write(state)
    st.line_chart(state_data, use_container_width=True)
st.subheader("Estadisticas 2021")
st.write(data_dict)
# st.write(subset_df)

# Create a dictionary to store data for selected states
data_dict = {}


# Check the lengths of data lists
for state, state_data in data_dict.items():
    st.write(f"State: {state}, Data Length: {len(state_data)}")

# Ensure the lengths match the length of filtered_dates
st.write(f"Filtered Dates Length: {len(filtered_dates)}")

st.write(filtered_dates)

# state_data_df = pd.DataFrame(data_dict, index=filtered_dates)
# st.dataframe(state_data_df)

# data_2022 = df[["State"] + [col for col in non_index_df.columns if {year} in col]]


# non_index_df.rename(columns={"Dates": "State"}, inplace=True)
non_index_df.set_index(non_index_df.columns[0], inplace=True)
non_index_df.index.name = "Dates"
# non_index_df = non_index_df.iloc[]
st.write(non_index_df)

# px.line(non_index_df)
# Crear una figura con Plotly Express
# Establecer "Dates" como el índice
# non_index_df.set_index(0, inplace=True)

# Crear una figura con Plotly Express
# Crear una figura con Plotly Express
# Filtrar el DataFrame por fecha

start_date_str = start_date.strftime("%Y-%m-%d")
end_date_str = end_date.strftime("%Y-%m-%d")
subset_df = non_index_df[selected_states]
# subset_df.index.name = "Dates"
subset_df = non_index_df[selected_states].loc[start_date:end_date]
st.dataframe(subset_df)
print(subset_df)
filtered_df = non_index_df.loc[
    (non_index_df.index >= start_date) & (non_index_df.index <= end_date)
]

# Filtrar las columnas para seleccionar solo los estados elegidos
# Transponer el DataFrame para tener las fechas en el eje x y los estados en el eje y
# non_index_df.set_index("Dates", inplace=True)
filtered_df = filtered_df.transpose()
# Remove the index name
filtered_df.index.name = None

# Configurar el nombre de la columna de las fechas y el índice
filtered_df.columns = filtered_df.iloc[0]
filtered_df = filtered_df[1:]
# Melt the DataFrame to long format
melted_df = filtered_df.melt(
    var_name="State", value_name="Unemployment Rate", ignore_index=False
)
# Reset the index to use "Dates" as a regular column
melted_df.reset_index(inplace=True)

# Create a line plot with Plotly Express
fig = px.line(
    melted_df,
    x="index",
    y="Unemployment Rate",
    color="State",
    title="Tasa de Desempleo por Estado",
)
st.write(melted_df)
st.plotly_chart(fig, use_container_width=True)
print(data_dict)
col1, col2 = st.columns(2)
with col1:
    st.subheader("Estadisticas 2021")
    # Create the bar charts for each state using subset_df
    for state in selected_states:
        st.write(state)

        # Assuming the 'Dates' are in the index and you want to use the date as the x-axis
        fig = px.bar(
            subset_df,
            x=subset_df.index,  # Use the index (dates) as the x-axis
            y=state,  # Choose the state column for the y-axis
            title=f"Tasa de Desempleo en {state}",
        )

        st.plotly_chart(fig)

# You can put additional content or charts in the second column (col2)
with col2:
    st.subheader("Other Content")
    # Add more content or charts here if needed
    for state in selected_states:
        st.write(state)

        # Assuming the 'Dates' are in the index and you want to use the date as the x-axis
        fig = px.pie(
            subset_df,
            x=subset_df.index,  # Use the index (dates) as the x-axis
            y=state,  # Choose the state column for the y-axis
            title=f"Tasa de Desempleo en {state}",
        )

        st.plotly_chart(fig)
