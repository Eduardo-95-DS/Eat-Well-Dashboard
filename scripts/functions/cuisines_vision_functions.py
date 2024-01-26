import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster,MousePosition
import plotly.express as px
import plotly.graph_objects as go

def create_cuisine(df):
    df2=df.assign(cuisine=df['cuisines'].str.split(',')).explode('cuisine')
    df2['cuisine']=df2['cuisine'].replace(' ','', regex=True)
    df2=df2.drop_duplicates(ignore_index=True)
    return df2

# plots==================================================================
def avg_cost (df,ordering):
    df2=create_cuisine(df)

    df_aux=df2[df2['average_cost_for_two']>0]

    df_aux=(df_aux[['cuisine','average_cost_for_two']].groupby('cuisine')
                                                   .mean()
                                                   .sort_values('average_cost_for_two',ascending=ordering)
                                                   .reset_index()
                                                   .head(10))
    
    fig=px.bar(df_aux, x='average_cost_for_two', y='cuisine', category_orders={'cuisine': df_aux['cuisine'].tolist()})
    
    fig.update_layout(xaxis=dict(title='Price in dollars ($)',title_font=dict(size=20)),yaxis=dict(title=''),xaxis_tickfont=dict(size=15), 
                      yaxis_tickfont=dict(size=15),height=500,margin=dict(t=0))
    
    st.plotly_chart(fig,use_container_width=True)
    

def rating(df,ordering):
    df2=create_cuisine(df)

    df_aux=df2[df2['votes']>3]
    
    df_aux=(df_aux[['cuisine','aggregate_rating']].groupby('cuisine')
                                               .mean()
                                               .sort_values('aggregate_rating',ascending=ordering)
                                               .reset_index()
                                               .head(10))
    
    fig=px.bar(df_aux, x='aggregate_rating', y='cuisine', category_orders={'cuisine': df_aux['cuisine'].tolist()})
    
    fig.update_layout(xaxis=dict(title='0-5',title_font=dict(size=20)),yaxis=dict(title=''),xaxis_tickfont=dict(size=15), 
                      yaxis_tickfont=dict(size=15),height=500,margin=dict(t=0))
    
    st.plotly_chart(fig,use_container_width=True)
    

def common_cuisines (df):
    df2=create_cuisine(df)
    
    df3=df2[['country','cuisine']].groupby('country').value_counts().reset_index()
    df3.loc[df3.groupby('country')['count'].idxmax()].sort_values('count',ascending=False)
    
    # Calcular a soma total de cada grupo (país)
    total_counts = df3.groupby('country')['count'].sum()
    
    # Adicionar uma nova coluna com a porcentagem
    df3['percentage'] = df3.apply(lambda row: (row['count'] / total_counts[row['country']]) * 100, axis=1)
    df3=df3.loc[df3.groupby('country')['count'].idxmax()].sort_values('percentage',ascending=True)
    
    fig = px.bar(df3, x='percentage', y='country', text='cuisine',category_orders={'percentage': df3['percentage'].tolist()},
                 labels={'percentage': 'Percentage (%)', 'country': 'Country'},
                 height=600)
    
    # Personalizar layout
    fig.update_layout(xaxis=dict(title='Percentage (%)',title_font=dict(size=20)),yaxis=dict(title=''),xaxis_tickfont=dict(size=15), 
                          yaxis_tickfont=dict(size=15),height=500,margin=dict(t=0),showlegend=False)

    st.plotly_chart(fig,use_container_width=True)



