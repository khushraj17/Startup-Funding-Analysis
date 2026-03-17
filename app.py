import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


st.set_page_config(page_title='Startup Funding Analysis', page_icon=':bar_chart:', layout='wide')
df = pd.read_csv('startup_cleaned.csv')

#data cleaning --------------------------------------------------------
df['investors'].fillna('unknown', inplace = True)

#----------------------------------------------------------------------

def load_invesstor_details(investor):
    st.header(investor)

    recnt_df = df[df['investors'].str.contains(investor)].head()[['date', 'startup', 'city', 'investors','amount']]
    st.subheader('Recent Investments')
    st.dataframe(recnt_df)

    big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending = False)
    st.subheader('Biggest Investments')
    st.dataframe(big_series)
    col1 , col2 = st.columns(2)
    with col1:
        st.subheader('Biggest Investments graph')
        fig , ax = plt.subplots()
        ax.bar(big_series.index, big_series.values)
        st.pyplot(fig)


st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('Select an option', ['Overall analysis', 'Startup', 'Investor'])

if option == 'Overall analysis':
    st.title('Overall Analysis')
    st.write('This section provides an overall analysis of startups and investors.')
    
elif option == 'Startup':
    st.sidebar.selectbox('Select a startup', sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Show Analysis')
    if btn1:
        st.title('Startup Analysis')

       
else:
    selected_investor = st.sidebar.selectbox('Select an investor',sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Show Analysis')
    if btn2:
        load_invesstor_details(selected_investor)

        