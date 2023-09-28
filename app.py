import pandas as pd
import plotly.express as px
import streamlit as st

MONTHS = ( "2019-09-01",
    "2019-10-01",
    "2019-11-01",
    "2019-12-01",
    "2020-01-01",
    "2020-02-01")

st.set_page_config(page_title="StackAdapt Case Dashboard", page_icon=":bar_chart:", layout="wide")

df = pd.read_excel(
    io="filteredExcel.xlsx",
    engine="openpyxl",
    sheet_name="Question_caseFiltered",
    nrows=16000,
)


# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
month = st.sidebar.multiselect(
    "Select the Month:",
    options=df["month"].unique(),
    default=df["month"].unique()
)


format = st.sidebar.multiselect(
    "Select the Format Type:",
    options=df["format"].unique(),
    default=df["format"].unique(),
)

device = st.sidebar.multiselect(
    "Select the Device Type:",
    options=df["device_type"].unique(),
    default=df["device_type"].unique(),
)

df_selection = df.query(
    "month == @month & format == @format & device_type ==@device"
)


# ---- MAINPAGE ----
st.title(":bar_chart: Alvin's Dashboard")
st.markdown("##")
# TOP KPI's
totalSpent = int(df_selection["spend"].sum())
conversions = int(df_selection["conversions"].sum())
clicks = int(df_selection["clicks"].sum())
df_selection["CTR"] = df_selection["clicks"] / df_selection["impressions"]
average_CTR = round(df_selection["CTR"].mean() * 100, 2)  # Multiply by 100 to get percentage

left_column, middle_column, middle2_column, right_column = st.columns(4)
with left_column:
    st.subheader("Total Spent:")
    st.subheader(f"$ {totalSpent:,}")
with middle_column:
    st.subheader("Conversions:")
    st.subheader(f"{conversions}")
with middle2_column:
    st.subheader("Clicks:")
    st.subheader(f"{clicks}")  
with right_column:
    st.subheader("CTR:")
    st.subheader(f"{average_CTR}")

st.markdown("""---""")


custom_month_order = [
    "2019 Sep 01",
    "2019 Oct 01",
    "2019 Nov 01",
    "2019 Dec 01",
    "2020 Jan 01",
    "2020 Feb 01"
]
# df_display = df_selection[df_selection['format'] == 'display']

# df_plot = df_display.groupby('month')['conversions'].sum()


df_plot = df_selection[df_selection['format'] == 'display'].groupby('month')['conversions'].sum().reset_index()


fig = px.line(df_plot, x='month', y='conversions', title='Conversions Over Months (Display Format)')
# fig.update_xaxes(categoryorder='array', categoryarray = [
#     "2019 Sep 01",
#     "2019 Oct 01",
#     "2019 Nov 01",
#     "2019 Dec 01",
#     "2020 Jan 01",
#     "2020 Feb 01"
# ])

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig, use_container_width=True)
right_column.plotly_chart(fig, use_container_width=True)






# print(df)
st.dataframe(df_selection)