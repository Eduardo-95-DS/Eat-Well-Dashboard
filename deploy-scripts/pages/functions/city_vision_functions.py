import streamlit as st
import pandas as pd
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


def rating(df, above_threshold, below_threshold):
    df_above = df[df['aggregate_rating'] > above_threshold]
    df_below = df[(df['aggregate_rating'] < below_threshold) & (df['votes'] > 3)]

    df2 = df[['city', 'country', 'restaurant_id']].groupby(['city', 'country']).count().reset_index() 
    df3 = df[['city', 'country', 'restaurant_id']].groupby(['city', 'country']).count().reset_index()

    df_merged1 = pd.merge(df2, df_above[['city', 'country', 'restaurant_id']]
                    .groupby(['city', 'country'])
                    .count()
                    .reset_index(), on=['city', 'country'], how='left', suffixes=('_total', '_rating_above_4_5'))

    df_merged2 = pd.merge(df3, df_below[['city', 'country', 'restaurant_id']]
                    .groupby(['city', 'country'])
                    .count()
                    .reset_index(), on=['city', 'country'], how='left', suffixes=('_total', '_rating_below_4'))

    df_merged1['restaurant_id_rating_above_4_5'] = df_merged1['restaurant_id_rating_above_4_5'].fillna(0).astype(int)  
    df_merged2['restaurant_id_rating_below_4'] = df_merged2['restaurant_id_rating_below_4'].fillna(0).astype(int)  

    df_merged1['proportion_rating_above_4_5'] = df_merged1['restaurant_id_rating_above_4_5'] / df_merged1['restaurant_id_total']
    df_merged2['proportion_rating_below_4'] = df_merged2['restaurant_id_rating_below_4'] / df_merged2['restaurant_id_total']

    df_above = (df_merged1.sort_values('restaurant_id_rating_above_4_5', ascending=False)
                          .rename(columns={'restaurant_id_total':'restaurants',
                                           'restaurant_id_rating_above_4_5':'rating_above_4_5',
                                           'proportion_rating_above_4_5':'proportion'})
                          .reset_index())

    df_below = (df_merged2.sort_values('proportion_rating_below_4', ascending=False)
                          .rename(columns={'restaurant_id_total':'restaurants',
                                     'restaurant_id_rating_below_4':'rating_below_4',
                                     'proportion_rating_below_4':'proportion'})
                          .reset_index())

    df_above['proportion'] = (df_above['proportion'] * 100).round(2)
    df_below['proportion'] = (df_below['proportion'] * 100).round(2)

    df_above=df_above[(df_above['rating_above_4_5']>0) & (df_above['restaurants']>10)]
    df_below=df_below[df_below['restaurants']>10]
    
    df_above=df_above[['city', 'country', 'proportion']]
    df_below=df_below[['city', 'country','proportion']]

    df_above['below 4.5']=(df_above['proportion']-100) *-1
    df_below['above 4.5']=(df_below['proportion']-100) *-1

    df_above=df_above.rename(columns={'proportion':'above 4.5'}).sort_values('above 4.5',ascending=False).head(10)
    df_below=df_below.rename(columns={'proportion':'below 4.5'}).sort_values('below 4.5',ascending=False).head(10)

    fig1 = (px.bar(df_above, x=["above 4.5","below 4.5"], y="city",
                                       color='country',text_auto=True,
                                       category_orders={'city': df_above['city'].tolist()}))
    
    fig1.update_layout(xaxis=dict(title='Percentage (%)',title_font=dict(size=20)), yaxis=dict(title=''),xaxis_tickfont=dict(size=15), 
                      yaxis_tickfont=dict(size=15),legend=dict(font=dict(size=15)), 
                      legend_title_text='',height=500,margin=dict(t=0))
    
    fig1.update_traces(marker_line_color='black', marker_line_width=2, selector=dict(type='bar'))
    
    fig1.update_xaxes(tickvals=[0, 50, 100], ticktext=['0','50','100'])

    fig2 = (px.bar(df_below, x=["below 4.5","above 4.5"], y="city",
                                       color='country',text_auto=True,
                                       category_orders={'city': df_below['city'].tolist()}))
    
    fig2.update_layout(xaxis=dict(title='Percentage (%)',title_font=dict(size=20)), yaxis=dict(title=''),xaxis_tickfont=dict(size=15), 
                      yaxis_tickfont=dict(size=15),legend=dict(font=dict(size=15)), 
                      legend_title_text='',height=500,margin=dict(t=0))
    
    fig2.update_traces(marker_line_color='black', marker_line_width=2, selector=dict(type='bar'))
    
    fig2.update_xaxes(tickvals=[0, 50, 100], ticktext=['0','50','100'])

    return fig1,fig2


def average_cost (df, ordering):
    df1=df[df['average_cost_for_two']>0]
    df1=(df1[['city','country','restaurant_name','average_cost_for_two']]
                 .sort_values('average_cost_for_two',ascending=ordering)
                 .head(10))
    
    custom_order = ['Singapore', 'New York City', 'Chicago', 'Pasay City', 'San Francisco']

    
    fig = px.scatter(df1,x='average_cost_for_two',y='city',color='country',height=400,category_orders={'city': custom_order},
                     hover_data=['country', 'restaurant_name', 'average_cost_for_two'], size='average_cost_for_two')
            
    fig.update_layout(xaxis=dict(title='Price in dollars ($)',title_font=dict(size=20)), yaxis=dict(title=''),xaxis_tickfont=dict(size=15), 
                      yaxis_tickfont=dict(size=15),legend=dict(font=dict(size=15)), 
                      legend_title_text='',height=500,margin=dict(t=0))
    
    st.plotly_chart(fig,use_container_width=True)


