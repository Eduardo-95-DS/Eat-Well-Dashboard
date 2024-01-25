import folium
import streamlit as st
from folium.plugins import MarkerCluster,MousePosition
import plotly.express as px
import plotly.graph_objects as go
from streamlit_folium import folium_static

# plots============================================

def highest_avg (df):
    df1=(df[['restaurant_name','country','city','average_cost_for_two']]
                                                  .groupby(['restaurant_name','country','city'])
                                                  .mean()
                                                  .sort_values('average_cost_for_two',ascending=False)
                                                  .reset_index()
                                                  .head(10))
    
    fig = px.bar(df1, x='average_cost_for_two', y="restaurant_name", 
                      color='country',text='city',text_auto=True,
                      category_orders={'restaurant_name': df1['restaurant_name'].tolist()})
    
    fig.update_layout(xaxis=dict(title='Price in dollars ($)',title_font=dict(size=20)), yaxis=dict(title=''),xaxis_tickfont=dict(size=15), 
                          yaxis_tickfont=dict(size=15),legend=dict(font=dict(size=15),x=10), 
                          legend_title_text='',height=400,width=500,margin=dict(t=0))
    
    fig.update_traces(marker_line_color='black', marker_line_width=2, selector=dict(type='bar'))
    
    st.plotly_chart(fig,use_container_width=True)    

def lowest_avg (df):
    df1=(df[['restaurant_name','country','city','average_cost_for_two']]
                                                  .groupby(['restaurant_name','country','city'])
                                                  .mean()
                                                  .sort_values('average_cost_for_two',ascending=True)
                                                  .reset_index()
                                                  .head(10))
    
    fig = px.bar(df1, x='average_cost_for_two', y="restaurant_name", color='country',text='city',text_auto=True,
                 category_orders={'restaurant_name': df1['restaurant_name'].tolist()})
    
    fig.update_layout(xaxis=dict(title='Price in dollars ($)',title_font=dict(size=20)), yaxis=dict(title=''),xaxis_tickfont=dict(size=15), 
                          yaxis_tickfont=dict(size=15),legend=dict(font=dict(size=15),x=10), 
                          legend_title_text='',height=400,width=500,margin=dict(t=0))
    
    fig.update_traces(marker_line_color='black', marker_line_width=2, selector=dict(type='bar'))
    
    st.plotly_chart(fig,use_container_width=True)    












