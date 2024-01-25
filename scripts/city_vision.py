import pandas as pd
import numpy as np
import streamlit as st
from functions.overview_functions import *
from functions.city_vision_functions import *

# load dataset
df_raw=pd.read_csv('../data/zomato_raw.csv')

# cleaning==============================================
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

# elif reset_button:

#     with st.container():
    
#         col1,col2=st.columns(2)
#         with col1:
            
#             st.markdown("<h4 style='text-align: center;'>Variety of restaurants</h4>",unsafe_allow_html=True)
            
#             df1=(df[['city','country','restaurant_name']].groupby(['city','country'])
#                                                          .count()
#                                                          .sort_values('restaurant_name',ascending=False)
#                                                          .rename(columns={'restaurant_name':'restaurants'})
#                                                          .reset_index()
#                                                          .head(12))
#             df1['count']=df1['restaurants']
    
#             fig=px.histogram(df1, x='restaurants', y='city',text_auto=True, hover_data='country', color="country",
#                                                              category_orders={'city': df1['city'].tolist()})
            
#             fig.update_layout(xaxis=dict(title='Count',title_font=dict(size=20)), yaxis=dict(title=''),xaxis_tickfont=dict(size=15), 
#                               yaxis_tickfont=dict(size=15),legend=dict(font=dict(size=15)), 
#                               legend_title_text='',height=500,margin=dict(t=0))
            
#             st.plotly_chart(fig,use_container_width=True)
    
#         with col2:
            
#             st.markdown("<h4 style='text-align: center;'>Variety of cuisines</h4>",unsafe_allow_html=True)
#             df2=df[['cuisines','city','country']]
#             df2=df2.assign(cuisine=df2['cuisines'].str.split(',')).explode('cuisine')
#             df2['cuisine']= df2['cuisine'].replace(' ','', regex=True)
#             df2=df2[['city','country','cuisine']]
#             df2=df2.drop_duplicates(ignore_index=True)
#             df_aux = (df2.loc[:, ['city','country' ,'cuisine']].groupby(['city','country'])
#                                                             .count()
#                                                             .sort_values('cuisine',ascending=False)
#                                                             .head(10)
#                                                             .reset_index())
    
#             fig=px.histogram(df_aux, x='cuisine', y='city', text_auto=True, hover_data='country', color="country",
#                                                              category_orders={'city': df_aux['city'].tolist()})
            
#             fig.update_layout(xaxis=dict(title='Count',title_font=dict(size=20)), yaxis=dict(title=''),xaxis_tickfont=dict(size=15), 
#                               yaxis_tickfont=dict(size=15),legend=dict(font=dict(size=15)), 
#                               legend_title_text='',height=500,margin=dict(t=0))
            
#             st.plotly_chart(fig,use_container_width=True)

else:
    
    st.markdown("<h4 style='text-align: center;'>Restaurants</h4>",unsafe_allow_html=True)

    restaurant_variety(df)


with st.container():

    col1,col2=st.columns(2)
    with col1:  
        
        st.markdown("<h4 style='text-align:center;margin-top: 0px;'>Average rating > 4.5</h4>",unsafe_allow_html=True)
        
        df1=df[df['aggregate_rating']>4.5]
        df2 = df[['city', 'country', 'restaurant_id']].groupby(['city', 'country']).count().reset_index()  # total de restaurantes por cidade
        
        df_merged = pd.merge(df2, df1[['city', 'country', 'restaurant_id']]
                            .groupby(['city', 'country'])
                             .count()
                             .reset_index(), on=['city', 'country'], how='left', suffixes=('_total', '_rating_above_4_5'))
        
        # cidades sem restaurantes com nota abaixo de 4 
        df_merged['restaurant_id_rating_above_4_5'] = df_merged['restaurant_id_rating_above_4_5'].fillna(0).astype(int)  
        
        df_merged['proportion_rating_above_4_5'] = df_merged['restaurant_id_rating_above_4_5'] / df_merged['restaurant_id_total']
        
        df1 = (df_merged.sort_values('restaurant_id_rating_above_4_5', ascending=False)
                        .rename(columns={'restaurant_id_total':'restaurants',
                                         'restaurant_id_rating_above_4_5':'rating_above_4_5',
                                         'proportion_rating_above_4_5':'proportion'})
                        .reset_index())
        
        df1['proportion'] = (df1['proportion'] * 100).round(2)
        df1=df1[(df1['rating_above_4_5']>0) & (df1['restaurants']>10)]
        df1=df1[['city', 'country', 'proportion']]
        
        df1['below 4.5']=(df1['proportion']-100) *-1
        df1=df1.rename(columns={'proportion':'above 4.5'}).sort_values('above 4.5',ascending=False).head(10)

        fig = px.bar(df1, x=["above 4.5", "below 4.5"], y="city", color='country',text_auto=True,
                     category_orders={'city': df1['city'].tolist()},
                     labels={'above 4.5': 'Above 4.5%', 'below 4.5': 'Below 4.5%'})
        
        fig.update_layout(xaxis=dict(title='Percentage (%)',title_font=dict(size=20)), yaxis=dict(title=''),xaxis_tickfont=dict(size=15), 
                          yaxis_tickfont=dict(size=15),legend=dict(font=dict(size=15)), 
                          legend_title_text='',height=500,margin=dict(t=0))
        
        fig.update_traces(marker_line_color='black', marker_line_width=2, selector=dict(type='bar'))
        
        fig.update_xaxes(tickvals=[0, 50, 100], ticktext=['0','50','100'])

        st.plotly_chart(fig,use_container_width=True)
            
    with col2:
        
        st.markdown("<h4 style='text-align:center;margin-top: 0px;'>Average rating < 4</h4>",unsafe_allow_html=True)
        
        df1 = df[(df['aggregate_rating']<4.0) & (df['votes']>3)]
        df2 = df[['city', 'country', 'restaurant_id']].groupby(['city', 'country']).count().reset_index()  # total de restaurantes por cidade
        
        df_merged = pd.merge(df2, df1[['city', 'country', 'restaurant_id']]
                            .groupby(['city', 'country'])
                             .count()
                             .reset_index(), on=['city', 'country'], how='left', suffixes=('_total', '_rating_below_4'))
        
        # cidades sem restaurantes com nota abaixo de 4 
        df_merged['restaurant_id_rating_below_4'] = df_merged['restaurant_id_rating_below_4'].fillna(0).astype(int)  
        
        df_merged['proportion_rating_below_4'] = df_merged['restaurant_id_rating_below_4'] / df_merged['restaurant_id_total']
        
        df1 = (df_merged.sort_values('proportion_rating_below_4', ascending=False)
                        .rename(columns={'restaurant_id_total':'restaurants',
                                         'restaurant_id_rating_below_4':'rating_below_4',
                                         'proportion_rating_below_4':'proportion'})
                        .reset_index())
        
        df1['proportion'] = (df1['proportion'] * 100).round(2)
        df1=df1[df1['restaurants']>10]
        df1=df1[['city', 'country','proportion']]
        
        df1['above 4.5']=(df1['proportion']-100) *-1
        df1=df1.rename(columns={'proportion':'below 4.5'}).sort_values('below 4.5',ascending=False).head(10)

        fig = (px.bar(df1, x=["below 4.5","above 4.5"], y="city",
                                           color='country',text_auto=True,
                                           category_orders={'city': df1['city'].tolist()}))
        
        fig.update_layout(xaxis=dict(title='Percentage (%)',title_font=dict(size=20)), yaxis=dict(title=''),xaxis_tickfont=dict(size=15), 
                          yaxis_tickfont=dict(size=15),legend=dict(font=dict(size=15)), 
                          legend_title_text='',height=500,margin=dict(t=0))
        
        fig.update_traces(marker_line_color='black', marker_line_width=2, selector=dict(type='bar'))
        
        fig.update_xaxes(tickvals=[0, 50, 100], ticktext=['0','50','100'])

        st.plotly_chart(fig,use_container_width=True)

with st.container():

    col1,col2=st.columns(2)
    with col1:  
        
        st.markdown("<h4 style='text-align:center;margin-top: 0px;'>Highest average cost for two</h4>",unsafe_allow_html=True)
        
        df1=(df[['city','country','restaurant_name','average_cost_for_two']]
                 .sort_values('average_cost_for_two',ascending=False)
                 .head(10))
        
        custom_order = ['Singapore', 'New York City', 'Chicago', 'Pasay City', 'San Francisco']
    
        
        fig = px.scatter(df1,x='average_cost_for_two',y='city',color='country',height=400,category_orders={'city': custom_order},
                         hover_data=['country', 'restaurant_name', 'average_cost_for_two'], size='average_cost_for_two')
                
        fig.update_layout(xaxis=dict(title='Price in dollars ($)',title_font=dict(size=20)), yaxis=dict(title=''),xaxis_tickfont=dict(size=15), 
                          yaxis_tickfont=dict(size=15),legend=dict(font=dict(size=15)), 
                          legend_title_text='',height=500,margin=dict(t=0))
        
        st.plotly_chart(fig,use_container_width=True)
            
    with col2:  
        
        st.markdown("<h4 style='text-align:center;margin-top: 0px;'>Lowest average cost for two</h4>",unsafe_allow_html=True)
        
        df1=df[df['average_cost_for_two']>0]
        df1=(df1[['city','country','restaurant_name','average_cost_for_two']]
                 .sort_values('average_cost_for_two',ascending=True)
                 .head(10))
        
        custom_order = ['Singapore', 'New York City', 'Chicago', 'Pasay City', 'San Francisco']
    
        
        fig = px.scatter(df1,x='average_cost_for_two',y='city',color='country',height=400,category_orders={'city': custom_order},
                         hover_data=['country', 'restaurant_name', 'average_cost_for_two'], size='average_cost_for_two')
        
        
        fig.update_layout(xaxis=dict(title='Price in dollars ($)',title_font=dict(size=20)), yaxis=dict(title=''),xaxis_tickfont=dict(size=15), 
                          yaxis_tickfont=dict(size=15),legend=dict(font=dict(size=15)), 
                          legend_title_text='',height=500,margin=dict(t=0))
        
        st.plotly_chart(fig,use_container_width=True)
       















