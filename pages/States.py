
import streamlit as st
from st_files_connection import FilesConnection
import plotly.express as px
import pandas as pd

st.set_page_config(
    page_title=":bar_chart: 2019 General Election - Voter Statistics Tamilnadu",
    page_icon=":bar_chart:",
)

# Create connection object and retrieve file contents.
conn = st.connection('s3', type=FilesConnection)

# Specify input format is a csv and to cache the result for 600 seconds.
df = conn.read("msawsbuckets3/Votes 2019.csv", input_format="csv", ttl=600)

var_State = st.sidebar.selectbox(
  "Select the State:",
  options=df["State_Name"].unique(),
  index=0, 
)

df=df.query(
  "State_Name == @var_State"
)

#st.title('2019 General Election - Voter Statistics @var_State')
st.header('2019 General Election - Voter Statistics @var_State')


# TOP KPI's
total_electors = int(df["Total_Electors"].sum())
total_voters = int(df["Total_Actual_Votes"].sum())

# KPI's COLUMNS
left_column,right_column=st.columns(2)

with left_column:
  st.subheader("Total Electors: :adult:")
  st.subheader(total_electors)
with right_column:
  st.subheader("Total Voters :adult: :hand:")
  st.subheader(total_voters)

st.markdown("---")

# BARCHARTS

# VOTES BY STATE [BAR CHART]

Votes_By_State=(
df.groupby(["State_Name"])[["Total_Electors", "Total_Voters"]].sum()
)

fig_Votes_By_State=px.bar(
    Votes_By_State,
    x=Votes_By_State.index,
    y=["Total_Electors", "Total_Voters"],
    #title="<b>Electors_and_Voters_By_{var_State}</b>",
    title="<b>Electors_and_Voters</b>",
    #color=["#FF0000", "#0000FF"],
    color_discrete_sequence=["#FF0000", "#0000FF"] * len(Votes_By_State),
    template="plotly_white",
)


# Displaying charts
# Displaying charts
st.plotly_chart(fig_Votes_By_State,use_container_width=True)


# HIDE STREAMLIT STYLE
hide_st_style="""
            <style>
            #MainMenu {visibility:hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """

st.markdown(hide_st_style, unsafe_allow_html=True)
