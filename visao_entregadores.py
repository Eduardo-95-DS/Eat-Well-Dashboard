# Libraries
import pandas         as pd
import numpy          as np
import plotly.express as px
import streamlit      as st
import folium
import requests
import reverse_geocode
from streamlit_folium import folium_static
from datetime  import datetime 
from haversine import haversine
from datetime  import time
from PIL       import Image

df=pd.read_csv('../data/train.csv')

df['order_date']=pd.to_datetime(df['order_date'])

# Barra lateral=====================================================================
st.set_page_config(layout='wide')
# st.dataframe(df)

# image_path='logo.png'
# image=Image.open(image_path)
# st.sidebar.image(image,width=120)

st.header('Marketplace - Deliveryman Vision')
st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery In Town')
st.sidebar.markdown("""---""")


st.sidebar.markdown('## Select a date')
date_slider= st.sidebar.slider(label='',
                min_value=datetime(2022,2,11),
                max_value=datetime(2022,4,6),
                value=    datetime(2022,4,6),
                format='DD-MM-YYYY')
st.sidebar.markdown("""---""")

st.sidebar.markdown('## Traffic condition')
traffic= st.sidebar.multiselect('',['low','medium','high','jam'],
                               default=['low','medium','high','jam'])

st.sidebar.markdown('## Weather condition')
weather= st.sidebar.multiselect('',['cloudy','fog','sandstorms','stormy','sunny','windy'],
                               default=['cloudy','fog','sandstorms','stormy','sunny','windy'])

# filtro de data
rows1=df['order_date'] < date_slider
df=df.loc[rows1,:]

# filtro de trânsito
rows2=df['road_traffic_density'].isin(traffic)
df=df.loc[rows2,:]

# filtro de clima
rows3=df['weather_conditions'].isin(weather)
df=df.loc[rows3,:]

# Layout central===========================================================

tab1,tab2=st.tabs(['Management Vision',' '])
with tab1:
    
    with st.container():
        st.title('Overall metrics')
        col1,col2,col3,col4=st.columns(4,gap='large')
        
        with col1:
            # st.subheader('Highest age')
            max_age=df['delivery_person_age'].max()
            col1.metric('Highest age',max_age)
        
        with col2:
            # st.subheader('Lowest age')
            min_age=df['delivery_person_age'].min()
            col2.metric('Lowest age',min_age)
            
        with col3:
            # st.subheader('Best vehicle condition')
            cond1=df['vehicle_condition'].max()
            col3.metric('Best vehicle condition',cond1)

        with col4:
            # st.subheader('Worst vehicle condition')
            cond2=df['vehicle_condition'].min()
            col4.metric('Worst vehicle condition',cond2)
            
    with st.container():
        st.markdown("""---""")
        st.title('Reviews')
        
        col1,col2=st.columns(2,gap='large')

        with col1:
            st.subheader('Average review per deliveryman')
            df1=df.groupby(['delivery_person_id'])['delivery_person_ratings'].mean().reset_index().sort_values(by='delivery_person_ratings',ascending=False)
            st.dataframe(df1)
        
        with col2:
            st.subheader('Average review per traffic condition')
            df2=(df[['delivery_person_ratings','road_traffic_density']].groupby('road_traffic_density')
                                                          .agg(mean_=('delivery_person_ratings','mean'),
                                                              std_= ('delivery_person_ratings','std')).sort_values(by='mean_',ascending=False)
                                                          .reset_index())
            st.dataframe(df2)
            
            st.subheader('Average review per weather condition')
            df3=(df[['delivery_person_ratings','weather_conditions']].groupby('weather_conditions')
                                                         .agg(mean_=('delivery_person_ratings','mean'),
                                                          std_= ('delivery_person_ratings','std')).sort_values(by='mean_',ascending=False)
                                                         .reset_index())
            st.dataframe(df3)

    with st.container():
        st.markdown("""---""")
        st.title('Delivery time')

        col1,col2=st.columns(2,gap='large')

        with col1:
            st.subheader('Fastest deliverymens')       
            df4=df[['delivery_person_id','city','time_taken(min)']].groupby(['city','delivery_person_id']).mean().sort_values(
                                                                             'time_taken(min)').reset_index().drop_duplicates(subset='city',ignore_index=True)
            st.dataframe(df4)

        with col2:
            st.subheader('Slowest deliverymens')
            df5=df[['delivery_person_id','city','time_taken(min)']].groupby(['city','delivery_person_id']).mean().sort_values(
                                                                             'time_taken(min)',ascending=False).reset_index().drop_duplicates(
                                                                                                            subset='city',ignore_index=True)
            st.dataframe(df5)

# with tab2:
    # ''
























