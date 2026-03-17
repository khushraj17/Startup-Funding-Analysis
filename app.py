import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


st.set_page_config(page_title='Startup Funding Analysis', page_icon=':bar_chart:', layout='wide')
df = pd.read_csv('startup_cleaned.csv')

#data cleaning --------------------------------------------------------
df['investors'].fillna('unknown', inplace = True)
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month

#----------------------------------------------------------------------

def load_invesstor_details(investor):
    st.header(investor)

    recnt_df = df[df['investors'].str.contains(investor)].head()[['date', 'startup', 'city', 'investors','amount']]
    st.subheader('Recent Investments')
    st.dataframe(recnt_df)

    big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending = False).head(10)
    st.subheader('Biggest Investments')
    st.dataframe(big_series)
    col1 , col2 = st.columns(2)
    with col1:
        st.subheader('Biggest Investments graph')
        fig , ax = plt.subplots()
        ax.bar(big_series.index, big_series.values)
        st.pyplot(fig)

        st.subheader('round wise distribution')
        stage = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()
        fig0 , ax0 = plt.subplots()
        ax0.pie(stage.values, labels = stage.index, autopct='%1.1f%%')
        st.pyplot(fig0)
        
    with col2:
        st.subheader('invested in sectors')
        sector = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
        fig1 , ax1 = plt.subplots()
        ax1.pie(sector.values, labels = sector.index, autopct='%1.1f%%')
        st.pyplot(fig1)

        st.subheader('Invested in cities')
        city = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum().sort_values(ascending = False).head(10)
        fig2 , ax2 = plt.subplots()
        ax2.pie(city.values, labels = city.index, autopct='%1.1f%%')
        st.pyplot(fig2)

    st.header('Investment over time')
    time_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
    fig3 , ax3 = plt.subplots()
    ax3.plot(time_series.index, time_series.values)
    ax3.set_xlabel('Year')
    ax3.set_ylabel('Investment Amount')
    ax3.grid(True)
    st.pyplot(fig3)


st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('Select an option', ['Overall analysis', 'Startup', 'Investor'])

if option == 'Overall analysis':
    btn0 = st.sidebar.button('Show Analysis')
    if btn0:
        st.title('Overall Analysis')
        total = df['amount'].sum()
        max_funding = df.groupby('startup')['amount'].sum().max()
        avg_funding = df.groupby('startup')['amount'].sum().mean()
        top_startup = df.groupby('startup')['amount'].sum().sort_values(ascending=False).head(1).index[0]
        col1 , col2, col3 , col4 = st.columns(4)
        with col2:
            st.metric(label='Total Funding', value=f'{round(total)} Cr')

        with col1: 
            st.metric(label='Max Funding', value=f'{round(max_funding)} Cr')
            st.metric(label='Top Funded Startup', value=top_startup)
            
        with col3:
            st.metric(label='Average Funding', value=f'{round(avg_funding)} Cr')

        with col4:
            st.metric(label='Total Startups', value=df['startup'].nunique())
        



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

        