import numpy as np
import datetime as dt
import pandas as pd

import yfinance as yf
import financedatabase as fd

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# App Config


# Page Config
st.set_page_config(
    layout = "wide",
    initial_sidebar_state = "expanded"
)

# App title
st.title("porfolio Analysis")

#import tickerlist
@st.cache_data
def load_data():
    #pulling list of all ETFs and equities from financedatabase
    ticker_list = pd.concat([fd.ETFs().select().reset_index()[['symbol','name']],
                             fd.Equities().select().reset_index()[['symbol', 'name']]])
    ticker_list = ticker_list[ticker_list.symbol.notna()]
    ticker_list['symbol_name'] = ticker_list.symbol + '-' + ticker_list.name
    
    return ticker_list

ticker_list = load_data()

#side bar
with st.sidebar:
    # portfolio builder
    sel_tickers = st.multiselect('Portfolio Builder', placeholder = 'Search tickers', options = ticker_list.symbol_name)
    sel_tickers_list = ticker_list[ticker_list.symbol_name.isin(sel_tickers)].symbol
    
    #display logos
    cols = st.columns(4)
    for i, ticker in enumerate(sel_tickers_list):
        try:
            cols[i % 4].image('https://logo.clearbit.com/' + yf.Ticker(ticker).info['website'].replace('https://www.', ''), width=65)
        except:
            cols[i % 4].subheader(ticker)
            
    # date selector
    cols = st.columns(2)
    sel_dt1 = cols[0].date_input('Start Date', value = dt.datetime(2025,1,1), format = 'YYYY-MM-DD')
    sel_dt2 = cols[1].date_input('End Date', format ='YYYY-MM-DD')
    
    # select tickers data
    if len(sel_tickers) != 0:
        yfdata = yf.download(list(sel_tickers_list), start = sel_dt1, end = sel_dt2)['Close'].reset_index().melt(id_vars=['Date'], var_name = 'ticker', value_name='price')
        yfdata['price_start'] = yfdata.groupby('ticker').price.transform('first')
        yfdata['price_pct_daily'] = yfdata.groupby('ticker').price.pct_change()
        yfdata['price_pct'] = (yfdata.price - yfdata.price_start) / yfdata.price_start
    
# tbas
tab1, tab2 = st.tabs(["Portfolio", "Calculator"])

if len(sel_tickers) == 0:
    st.info('Select tickers to view plots')
else:
    st.empty()
    
    #tab1
    with tab1:
        #all stocks plot
        st.subheader('All Stocks')
        fig = px.line(yfdata, x ='Date', y='price_pct', color='ticker', markers = True)
        fig.add_hline(y=0, line_dash="dash", line_color='white')
        fig.update_layout(xaxis_title=None, yaxis_title=None)
        fig.update_yaxes(tickformat=',.0%')
        st.plotly_chart(fig, use_container_width= True)
        
        # indivudal stock plots
        st.subheader("individual Stock")
        cols = st.columns(3)
        for i,ticker in enumerate(sel_tickers_list):
            #adding logo
            try:
                cols[i % 4].image('https://logo.clearbit.com/' + yf.Ticker(ticker).info['website'].replace('https://wwww.', ''), width=65)
            except:
                cols[i % 4].subheader(ticker)
                
                
            # stock emtrics
            cols2 = cols[i % 3].columns(3)
            ticker = 'Close' if len(sel_tickers_list) == 1 else ticker
            cols2[0].metric(label='50-Day Average', value=round(yfdata[yfdata.ticker==ticker].price.tail(50).mean(),2))
            cols2[1].metric(label='1-Year Low', value=round(yfdata[yfdata.ticker==ticker].price.tail(365).min(),2))
            cols2[2].metric(label='1-Year High', value=round(yfdata[yfdata.ticker==ticker].price.tail(365).max(),2))
            
            
            #stock plot
            fig = px.line(yfdata[yfdata.ticker == ticker], x='Date',y='price', markers = True)
            fig.update_layout(xaxis_title=None, yaxis_title=None)
            cols[i % 3].plotly_chart(fig, use_container_width= True)
            
            
    # Tab2
    with tab2:
        #Amounts input
        cols_tab2 = st.columns((0.2,0.8))
        total_inv = 0
        amounts = {}
        for i, ticker in enumerate(sel_tickers_list):
            cols = cols_tab2[0].columns((0.1, 0.3))
            #adding logo
            try:
                cols[0].image('https://logo.clearbit.com/' + yf.Ticker(ticker).info['website'].replace('https://wwww.', ''), width=65)
            except:
                cols[0].subheader(ticker)
                
            amount = cols[1].number_input('', key=ticker, step=50)
            total_inv = total_inv+amount
            amounts[ticker] = amount
            
        #investment goals
        cols_tab2[1].subheader('Total Investment: ' + str(total_inv))
        cols_goal = cols_tab2[1].columns((0.06, 0.20, 0.7))
        cols_goal[0].text('')
        cols_goal[0].subheader('Goals: ')
        goal = cols_goal[1].number_input('', key='goal', step=50)
        
        # plot
        df = yfdata.copy()
        df['amount'] = df.ticker.map(amounts) * (1 + df.price_pct)
        
        dfsum = df.groupby('Date').amount.sum().reset_index()
        fig = px.area(df, x='Date', y='amount', color = 'ticker')
        fig.add_hline(y=goal, line_color='rgb(57,255,20)', line_dash='dash', line_width=3)
        
        if dfsum[dfsum.amount >= goal].shape[0] == 0:
            cols_tab2[1].warning("The goal can't be reached within this time frame.")
        else:
            fig.add_vline(x=dfsum[dfsum.amount >= goal].Date.iloc[0], line_color='rgb(57,255,20)', line_dash='dash', line_width=3)
            fig.add_trace(go.Scatter(x=[dfsum[dfsum.amount >= goal].Date.iloc[0] + dt.timedelta(days=7)], y=[goal*1.1],
                                     text=[dfsum[dfsum.amount >= goal].Date.dt.date.iloc[0]],
                                     mode='text',
                                     name='Goal',
                                     textfont=dict(color='rgb(57,255,20)',
                                                   size=20)))
            
        fig.update_layout(xaxis_title=None, yaxis_title=None)
        cols_tab2[1].plotly_chart(fig, use_container_width=True)