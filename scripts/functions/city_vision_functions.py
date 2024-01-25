import streamlit as st
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster,MousePosition
import plotly.express as px
import plotly.graph_objects as go

# plots==========================================================

def restaurant_variety (df):
    df1=(df[['city','country','restaurant_name']].groupby(['city','country'])
                                                         .count()
                                                         .sort_values('restaurant_name',ascending=False)
                                                         .rename(columns={'restaurant_name':'restaurants'})
                                                         .reset_index()
                                                         .head(12))
    df1['count']=df1['restaurants']

    fig=px.histogram(df1, x='restaurants', y='city',text_auto=True, hover_data='country', color="country",
                                                     category_orders={'city': df1['city'].tolist()})
    
    fig.update_layout(xaxis=dict(title='Count',title_font=dict(size=20)), yaxis=dict(title=''),xaxis_tickfont=dict(size=15), 
                      yaxis_tickfont=dict(size=15),legend=dict(font=dict(size=15)), 
                      legend_title_text='',height=500,margin=dict(t=0))
    
    st.plotly_chart(fig,use_container_width=True)

def cuisine_variety (df):
    df2=df[['cuisines','city','country']]
    df2=df2.assign(cuisine=df2['cuisines'].str.split(',')).explode('cuisine')
    df2['cuisine']= df2['cuisine'].replace(' ','', regex=True)
    df2=df2[['city','country','cuisine']]
    df2=df2.drop_duplicates(ignore_index=True)
    df_aux = (df2.loc[:, ['city','country' ,'cuisine']].groupby(['city','country'])
                                                    .count()
                                                    .sort_values('cuisine',ascending=False)
                                                    .head(10)
                                                    .reset_index())

    fig=px.histogram(df_aux, x='cuisine', y='city', text_auto=True, hover_data='country', color="country",
                                                     category_orders={'city': df_aux['city'].tolist()})
    
    fig.update_layout(xaxis=dict(title='Count',title_font=dict(size=20)), yaxis=dict(title=''),xaxis_tickfont=dict(size=15), 
                      yaxis_tickfont=dict(size=15),legend=dict(font=dict(size=15)), 
                      legend_title_text='',height=500,margin=dict(t=0))
    
    st.plotly_chart(fig,use_container_width=True)

