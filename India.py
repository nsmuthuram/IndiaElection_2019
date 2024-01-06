import streamlit as st
from st_files_connection import FilesConnection
import plotly.express as px
import pandas as pd

st.set_page_config(
    page_title=":bar_chart: 2019 General Election - Voter Statistics India",
    page_icon=":bar_chart:",
)

st.title('2019 General Election - Voter Statistics India')

# Create connection object and retrieve file contents.
conn = st.connection('s3', type=FilesConnection)

# Specify input format is a csv and to cache the result for 600 seconds.
df = conn.read("msawsbuckets3/Votes 2019.csv", input_format="csv", ttl=600)

# TOP KPI's
total_population = int(df["Total Electors"].sum())
total_voters = int(df["Total Actual Votes"].sum())


# KPI's COLUMNS
left_column,right_column=st.columns(2)

with left_column:
  st.subheader("Total Population:")
  st.subheader(total_population)
with right_column:
  st.subheader("Total Voters")
  st.subheader(total_voters)

st.markdown("---")

# BARCHARTS

# VOTES BY GENDER [BAR CHART]

Votes_By_Gender=(
  df.groupby(["State Name"])[["Total Electors"]].sum()
)

fig_Votes_By_Gender = px.bar(
    Votes_By_Gender,
    x="Total Electors",
    y=Votes_By_Gender.index,
    orientation="h",
    title="<b>Votes_By_Gender</b>",
    color_discrete_sequence=["#c27ba0"] * len(Votes_By_Gender),
    #Colour of Chart
    template="plotly_white",
)

fig_Votes_By_Gender.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)


# VOTES BY TYPE [BAR CHART]

Votes_By_Type=(
df.groupby(["State Name"])[["Total Electors"]].sum()
)

fig_Votes_By_Type=px.bar(
    Votes_By_Type,
    x=Votes_By_Type.index,
    y="Total Electors",
    title="<b>Votes_By_Type</b>",
    color_discrete_sequence=["#c27ba0"] * len(Votes_By_Type),
    template="plotly_white",
)


# Displaying charts
left_column,right_column=st.columns(2)
left_column.plotly_chart(fig_Votes_By_Gender,use_container_width=True)
right_column.plotly_chart(fig_Votes_By_Type,use_container_width=True)


# HIDE STREAMLIT STYLE
hide_st_style="""
            <style>
            #MainMenu {visibility:hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """

st.markdown(hide_st_style, unsafe_allow_html=True)
