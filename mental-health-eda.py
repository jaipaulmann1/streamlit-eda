import streamlit as st
import pandas as pd
import plost

st.set_page_config(layout='wide', initial_sidebar_state='expanded',
                   page_title='Mental Health Dataset EDA', page_icon=':bar_chart:')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

df = pd.read_csv('Mental_Health_Care_in_the_Last_4_Weeks.csv')
df['date'] = pd.to_datetime(df['Time Period Start Date'])


st.sidebar.header('Mental Health Dataset EDA')

st.sidebar.subheader('Group by parameter')
group = st.sidebar.selectbox('Group by', df['Group'].unique())

subgroup = st.sidebar.selectbox(
    'Select subgroup', df.loc[df['Group'] == group]['Subgroup'].unique())

st.sidebar.subheader('Indicator parameter')
indicator = st.sidebar.selectbox('Select indicator', df['Indicator'].unique())

st.sidebar.subheader('State parameter')
state = st.sidebar.selectbox('Select state', df['State'].unique())

# st.sidebar.subheader('Time Period parameter')
# time_period = st.sidebar.selectbox(
#     'Select time period', df['Time Period Start Date'].unique())


# st.sidebar.subheader('Line chart parameters')
# plot_data = st.sidebar.multiselect(
#     'Select data', ['temp_min', 'temp_max'], ['temp_min', 'temp_max'])
# plot_height = st.sidebar.slider('Specify plot height', 200, 500, 250)


# df with filters applied
df_selection = df.query(
    "Group == @group & Subgroup == @subgroup & Indicator == @indicator & State == @state"
)

# Row A
st.markdown('### Top-level Metrics agged over Time')
col1, col2, col3 = st.columns(3)
col1.metric("Avg (%)", round(df_selection['Value'].mean(), 1))
col2.metric("Min (%)", df_selection['Value'].min())
col3.metric("Max (%)", df_selection['Value'].max())

# Row B

c1, c2 = st.columns((7, 3))
with c1:
    st.markdown('### Values over Time')
    st.line_chart(df_selection, x='date', y='Value')

df_subgroup_visual = df.query(
    "Group == @group & Indicator == @indicator & State == @state"
)

df_subgroup_grouped = pd.DataFrame(df_subgroup_visual.groupby(
    ['Subgroup'])['Value'].mean().sort_values()).reset_index()

with c2:
    st.markdown('### Broken out by Subgroup')
    st.bar_chart(
        data=df_subgroup_grouped,
        x='Subgroup',
        y='Value',
        use_container_width=True)

# # Row C
st.markdown('### Data Frame')
st.dataframe(df_selection[['Indicator', 'Group',
             'State', 'Subgroup', 'Time Period Label', 'Value', 'date']])
