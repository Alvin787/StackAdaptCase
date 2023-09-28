import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="StackAdapt Case Dashboard", page_icon=":bar_chart:", layout="wide")

@st.cache_data
def get_data_from_excel():
    df = pd.read_excel(
        io="filteredExcel.xlsx",
        engine="openpyxl",
        sheet_name="Question_caseFiltered",
        nrows=16000,
    )
    return df

df = get_data_from_excel()

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
    st.subheader("Total Conversions:")
    st.subheader(f"{conversions}")
with middle2_column:
    st.subheader("Total Clicks:")
    st.subheader(f"{clicks}")  
with right_column:
    st.subheader("Average CTR:")
    st.subheader(f"{average_CTR}")

st.markdown("""---""")


df_plot = df_selection[df_selection['format'] == 'native'].groupby('month')['conversions'].sum().reset_index()
df_plot['month'] = pd.to_datetime(df_plot['month'], format='%Y %b %d', errors='coerce')
df_plot = df_plot.sort_values(by="month")
fig = px.line(df_plot, x='month', y=['conversions', ], title='Conversions Over Months (Native Format)')


conversionsByCategory = df_selection.groupby(by=["advertiser_category"])[["conversions"]].sum().sort_values(by="conversions")
fig2 = px.bar(
    conversionsByCategory,
    x="conversions",
    y=conversionsByCategory.index,
    orientation="h",
    title="<b>Category vs Conversion</b>",
    labels={
        "conversions": "Conversions",
        "advertiser_category": "Category",
            },
    template="plotly_white",
)

df_plot = df_selection[df_selection['format'] == 'display'].groupby('month')['conversions'].sum().reset_index()
df_plot['month'] = pd.to_datetime(df_plot['month'], format='%Y %b %d', errors='coerce')
df_plot = df_plot.sort_values(by="month")
fig3 = px.line(df_plot, x='month', y=['conversions', ], title='Conversions Over Months (Display Format)')

df_plot = df_selection[df_selection['format'] == 'video'].groupby('month')['conversions'].sum().reset_index()
df_plot['month'] = pd.to_datetime(df_plot['month'], format='%Y %b %d', errors='coerce')
df_plot = df_plot.sort_values(by="month")
fig5 = px.line(df_plot, x='month', y=['conversions', ], title='Conversions Over Months (Video Format)')

# Calculate CTR per month
df_plot = df_selection.groupby('month')['CTR'].mean().reset_index()
df_plot['month'] = pd.to_datetime(df_plot['month'], format='%Y %b %d', errors='coerce')
df_plot = df_plot.sort_values(by="month")

# Create a line graph for CTR
fig_ctr = px.line(df_plot, x='month', y='CTR', title='Average Click-Through Rate (CTR) Over Months')


df_plot = df_selection.groupby('month')['spend'].sum().reset_index()
df_plot['month'] = pd.to_datetime(df_plot['month'], format='%Y %b %d', errors='coerce')
df_plot = df_plot.sort_values(by="month")
spend = px.line(df_plot, x='month', y='spend', title='Spending Over Months')


left_column, right_column= st.columns(2)
left_column.plotly_chart(fig, use_container_width=True)
right_column.plotly_chart(fig2, use_container_width=True)
left_column.plotly_chart(fig3, use_container_width=True)
right_column.plotly_chart(fig_ctr, use_container_width=True)
left_column.plotly_chart(fig5, use_container_width=True)
right_column.plotly_chart(spend, use_container_width=True)


st.dataframe(df_selection)


hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)