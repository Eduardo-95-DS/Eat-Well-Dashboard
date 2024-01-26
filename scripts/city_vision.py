import pandas as pd
import numpy as np
import streamlit as st
from functions.overview_functions import *
from functions.city_vision_functions import *

# load dataset
df_raw=pd.read_csv('../data/zomato_raw.csv')

# cleaning=========================================================================
df_raw=cleaning(df_raw)

df=df_raw.copy()

# Barra lateral=====================================================================
st.set_page_config(layout='wide')
# st.dataframe(df)

# image_path='logo.png'
# image=Image.open(image_path)
# st.sidebar.image(image,width=120)

st.markdown("<h1 style='text-align: center;'>City Vision</h1>",unsafe_allow_html=True)
st.sidebar.markdown('# Eat Well Company')
st.sidebar.markdown("""---""")

# filtro de país
st.sidebar.markdown("""
    <div style="margin-bottom: -70px;">
        <span style="font-size:20px; font-weight:bold;">Country</span>
    </div>
""", unsafe_allow_html=True)

countries = ['All','United States of America', 'Canada', 'Brazil', 'England','Australia', 'New Zealand', 'Philippines', 'Indonesia',
    'India', 'Sri Lanka', 'United Arab Emirates', 'Qatar','Turkey', 'Singapore','South Africa']
country = st.sidebar.selectbox('country', countries,label_visibility="hidden")

if country == 'All':
    df=df.loc[(df['country']==df['country'])]
else:
    df=df.loc[(df['country']==country)]

# filtro de cidade
st.sidebar.markdown("""
    <div style="margin-bottom: -70px;">
        <span style="font-size:20px; font-weight:bold;">City</span>
    </div>
""", unsafe_allow_html=True)

cities=df['city'].unique()
cities=np.insert(cities, 0, 'All')
city = st.sidebar.selectbox('city', cities ,label_visibility="hidden")

if city == 'All':
    df=df.loc[(df['city']==df['city'])]
else:
    df=df.loc[(df['city']==city)]

# filtro de preço
st.sidebar.markdown("""
    <div style="margin-bottom: -70px;">
        <span style="font-size:20px; font-weight:bold;">Price range</span>
    </div>
""", unsafe_allow_html=True)

price= st.sidebar.multiselect('',['cheap','normal','expensive','gourmet'],
                               default=['cheap','normal','expensive','gourmet'],key='multiselect')

rows=df['price_range'].isin(price)
df=df.loc[rows,:]

# filtro de booking
st.sidebar.markdown("""
    <div style="margin-bottom: -70px;">
        <span style="font-size:20px; font-weight:bold;">Booking</span>
    </div>
""", unsafe_allow_html=True)

booking= st.sidebar.multiselect('',['Yes','No'],
                               default=['Yes','No'],key='booking')

rows=df['has_table_booking'].isin(booking)
df=df.loc[rows,:]

# filtro de online delivery
st.sidebar.markdown("""
    <div style="margin-bottom: -70px;">
        <span style="font-size:20px; font-weight:bold;">Online delivery</span>
    </div>
""", unsafe_allow_html=True)

online= st.sidebar.multiselect('',['Yes','No'],
                               default=['Yes','No'],key='online')

rows=df['has_online_delivery'].isin(online)
df=df.loc[rows,:]

# filtro de delivering now
st.sidebar.markdown("""
    <div style="margin-bottom: -70px;">
        <span style="font-size:20px; font-weight:bold;">Delivering now</span>
    </div>
""", unsafe_allow_html=True)

delivery= st.sidebar.multiselect('',['Yes','No'],
                               default=['Yes','No'],key='delivery')

rows=df['is_delivering_now'].isin(delivery)
df=df.loc[rows,:]

# # filtro de culinaria
st.sidebar.markdown("""
    <div style="margin-bottom: -70px;">
        <span style="font-size:20px; font-weight:bold;">Cuisine</span>
    </div>
""", unsafe_allow_html=True)

cuisine=cuisine_filter(df)
cuisines = st.sidebar.selectbox('cuisine', cuisine, label_visibility="hidden")

cuisines = [cuisines]

if 'All' in cuisines:
    df = df
else:
    mascara = df['cuisines'].str.contains('|'.join(cuisines), case=True)
    linhas_desejadas = df[mascara]
    df=linhas_desejadas

# filtro de reset
reset_button = st.sidebar.button("Reset Visualizations")

if reset_button:
    df = df_raw.copy()
else:
    print('')

# plots================================================================================

if 'All' in cuisines or reset_button:
    
    with st.container():
    
        col1,col2=st.columns(2)
        with col1:
            
            st.markdown("<h4 style='text-align: center;'>Variety of restaurants</h4>",unsafe_allow_html=True)

            restaurant_variety(df)
    
        with col2:
            
            st.markdown("<h4 style='text-align: center;'>Variety of cuisines</h4>",unsafe_allow_html=True)

            cuisine_variety(df)

else:
    
    st.markdown("<h4 style='text-align: center;'>Restaurants</h4>",unsafe_allow_html=True)

    restaurant_variety(df)


with st.container():

    col1,col2=st.columns(2)
    with col1:  
        
        st.markdown("<h4 style='text-align:center;margin-top: 0px;'>Average rating > 4.5</h4>",unsafe_allow_html=True)
        
        fig1,fig2=rating(df,4.5,4)
        st.plotly_chart(fig1,use_container_width=True)

    with col2:
        
        st.markdown("<h4 style='text-align:center;margin-top: 0px;'>Average rating < 4</h4>",unsafe_allow_html=True)

        st.plotly_chart(fig2,use_container_width=True)

with st.container():

    col1,col2=st.columns(2)
    with col1:  
        
        st.markdown("<h4 style='text-align:center;margin-top: 0px;'>Highest average cost for two</h4>",unsafe_allow_html=True)

        average_cost(df,False)
            
    with col2:  
        
        st.markdown("<h4 style='text-align:center;margin-top: 0px;'>Lowest average cost for two</h4>",unsafe_allow_html=True)

        average_cost(df,True)















