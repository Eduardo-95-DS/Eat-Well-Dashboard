import pandas as pd
import streamlit as st
from PIL import Image
from pages.functions.overview_functions import *

# load dataset
df_raw=pd.read_csv('data/zomato_raw.csv')

st.set_page_config(page_title='Overview',layout='wide')

# cleaning=========================================================================
df_raw=cleaning(df_raw)

df=df_raw.copy()

# Barra lateral=====================================================================

image_path='image/logo.jpg'
image=Image.open(image_path)
st.sidebar.image(image,width=180)

st.sidebar.markdown('# Eat Well Company')
st.sidebar.markdown("""---""")

# filtro de mapas
st.sidebar.markdown('## Choose your Map')
options= st.sidebar.selectbox('',('Cuisines', 'Price', 'Aggregate Rating', 'Avg Cost for Two'),index=None,placeholder="Select map...")
st.sidebar.markdown("""---""")

# filtro de país
countries = ['World View','United States of America', 'Canada', 'Brazil', 'England','Australia', 'New Zealand', 'Philippines', 'Indonesia',
    'India', 'Sri Lanka', 'United Arab Emirates', 'Qatar','Turkey', 'Singapore']
st.sidebar.markdown('## Choose a country')
selected_country = st.sidebar.selectbox('', countries)

# plots================================================================================
# st.markdown("<h1 style='text-align: center;'>Overview</h1>",unsafe_allow_html=True)

with st.container():

    col1,col2,col3,col4,col5=st.columns(5)
    with col1:
        st.markdown('##### Unique restaurants')
        unique_rest=len(df['restaurant_id'].unique())
        col1.metric('',unique_rest)
            
    with col2:
        st.markdown('##### Unique countries')
        unique_countries=len(df['country'].unique())
        col2.metric('',unique_countries)

    with col3:
        st.markdown("##### Unique cities")
        unique_cities=len(df['city'].unique())
        col3.metric('',unique_cities)

    with col4:
        st.markdown("##### Total votes")
        votes=df["votes"].sum()
        col4.metric('',votes)

    with col5:
        st.markdown("##### Unique cuisines")
        
        df2=df.assign(cuisine=df['cuisines'].str.split(',')).explode('cuisine')
        cuisines=len(df2['cuisine'].unique())
        col5.metric('',cuisines)

with st.container():

    if options == 'Cuisines':
        cuisines_map(df)
        
    elif options =='Price':
        price_map(df,selected_country)
        
    elif options =='Aggregate Rating':
        agg_map(df,selected_country)
        
    elif options =='Avg Cost for Two':
        avg_map(df,selected_country)
        
    else:
        overview_map(df,selected_country)






