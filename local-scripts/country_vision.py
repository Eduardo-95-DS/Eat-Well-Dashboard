import pandas as pd
import numpy as np
import streamlit as st
from functions.overview_functions import *
from functions.country_vision_functions import *
from PIL import Image

# load dataset
df_raw=pd.read_csv('../data/zomato_raw.csv')

# cleaning
df_raw=cleaning(df_raw)

df=df_raw.copy()
df3=df_raw.copy()

# Barra lateral=====================================================================
st.set_page_config(layout='wide')

image_path='../image/logo.jpg'
image=Image.open(image_path)
st.sidebar.image(image,width=150,use_column_width="always")

st.sidebar.markdown('# Eat Well Company')
st.sidebar.markdown("""---""")

# filtro de preço
st.sidebar.markdown("""
    <div style="margin-bottom: -70px;">
        <span style="font-size:20px; font-weight:bold;">Price range</span>
    </div>
""", unsafe_allow_html=True)

price= st.sidebar.multiselect('',['cheap','normal','expensive','gourmet'],
                               default=['cheap','normal','expensive','gourmet'],key='multiselect')

rows1=df['price_range'].isin(price)
rows2=df3['price_range'].isin(price)

df=df.loc[rows1,:]
df3=df3.loc[rows2,:]

# filtro de booking
st.sidebar.markdown("""
    <div style="margin-bottom: -70px;">
        <span style="font-size:20px; font-weight:bold;">Booking</span>
    </div>
""", unsafe_allow_html=True)

booking= st.sidebar.multiselect('',['Yes','No'],
                               default=['Yes','No'],key='booking')

if not booking:
    rows1 = ~df['has_table_booking'].isna()
    rows2 = ~df3['has_table_booking'].isna()

else:
    rows1 = df['has_table_booking'].isin(booking)
    rows2 = df3['has_table_booking'].isin(booking)

df = df.loc[rows1, :]
df3 = df3.loc[rows2, :]

# filtro de online delivery
st.sidebar.markdown("""
    <div style="margin-bottom: -70px;">
        <span style="font-size:20px; font-weight:bold;">Online delivery</span>
    </div>
""", unsafe_allow_html=True)

online= st.sidebar.multiselect('',['Yes','No'],
                               default=['Yes','No'],key='online')

if not online:
    rows1 = ~df['has_online_delivery'].isna()
    rows2 = ~df3['has_online_delivery'].isna()

else:
    rows1 = df['has_online_delivery'].isin(online)
    rows2 = df3['has_online_delivery'].isin(online)

df = df.loc[rows1, :]
df3 = df3.loc[rows2, :]

# filtro de delivering now
st.sidebar.markdown("""
    <div style="margin-bottom: -70px;">
        <span style="font-size:20px; font-weight:bold;">Delivering now</span>
    </div>
""", unsafe_allow_html=True)

delivery= st.sidebar.multiselect('',['Yes','No'],
                               default=['Yes','No'],key='delivery')

if not delivery:
    rows1 = ~df['is_delivering_now'].isna()
    rows2 = ~df3['is_delivering_now'].isna()

else:
    rows1 = df['is_delivering_now'].isin(delivery)
    rows2 = df3['is_delivering_now'].isin(delivery)

df = df.loc[rows1, :]
df3 = df.loc[rows2, :]

# filtro de culinaria
st.sidebar.markdown("""
    <div style="margin-bottom: -70px;">
        <span style="font-size:20px; font-weight:bold;">Cuisine</span>
    </div>
""", unsafe_allow_html=True)

cuisine=cuisine_filter(df)
cuisines = st.sidebar.selectbox('cuisine', cuisine, label_visibility="hidden")

cuisine1 = cuisines
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

st.markdown("<h1 style='text-align: center;'>Country Vision</h1>",unsafe_allow_html=True)

# plots=======================================================================

if 'All' in cuisines:

    with st.container():
    
        col1,col2=st.columns(2)
        with col1:
            
            st.markdown("<h3 style='text-align: center;'>N° of restaurants</h3>",unsafe_allow_html=True)
    
            restaurants_number(df)
                
        with col2:
            
            st.markdown("<h3 style='text-align: center;'>Unique cuisines</h3>",unsafe_allow_html=True)
    
            unique_cuisines(df)

elif reset_button:

    with st.container():
        col1,col2=st.columns(2)
        
        with col1:
            
            st.markdown("<h3 style='text-align: center;'>N° of restaurants</h3>",unsafe_allow_html=True)
    
            restaurants_number(df)

        with col2:
            
            st.markdown("<h3 style='text-align: center;'>Unique cuisines</h3>",unsafe_allow_html=True)
    
            unique_cuisines(df)

else:

    with st.container():
        
        st.markdown("<h3 style='text-align: center;'>N° of restaurants</h3>",unsafe_allow_html=True)
    
        restaurants_number(df)

with st.container():
    col1,col2=st.columns(2)
    
    with col1:
        
        st.markdown("<h3 style='text-align: center;'>Average rating</h3>",unsafe_allow_html=True)

        average_rating(df)
            
    with col2:
        
        st.markdown("<h3 style='text-align: center;'>Average cost for two</h3>",unsafe_allow_html=True)

        average_cost_for_two(df)

with st.container():
    col1,col2=st.columns(2)
    
    with col1:
        
        st.markdown("<h3 style='text-align: center;'>Price range</h3>",unsafe_allow_html=True)

        price_range(df)
            
    with col2:

        st.markdown("<h3 style='text-align: center;'>Proportion</h3>",unsafe_allow_html=True)

        if 'All' in cuisines or reset_button:
        
            cuisine_country_proportion(df)
            
        else:
            
            selected_cuisine_country_proportion(df3,cuisine1)






