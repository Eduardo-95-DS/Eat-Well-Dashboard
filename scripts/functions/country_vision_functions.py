import streamlit as st
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster,MousePosition
import plotly.express as px
import plotly.graph_objects as go

def cuisine (df):
    df2=df.assign(cuisine=df['cuisines'].str.split(',')).explode('cuisine')
    df2=df2.drop_duplicates(ignore_index=True)
    return df2
    
# plots==================================================================
def restaurants_number (df):
    df_aux = (df.loc[:, ['country', 'restaurant_id']].groupby('country')
                                                  .count()
                                                  .sort_values('restaurant_id',ascending=False)
                                                  .reset_index())
    
    fig=px.bar(df_aux, x='restaurant_id', y='country', category_orders={'country': df_aux['country'].tolist()})
    
    fig.update_layout(xaxis=dict(title='Count',title_font=dict(size=20)), yaxis=dict(title=''),xaxis_tickfont=dict(size=15), 
                      yaxis_tickfont=dict(size=15),height=500,margin=dict(t=0))
    
    st.plotly_chart(fig,use_container_width=True)

def unique_cuisines (df):
    df2=cuisine(df)
    df2=df2[['cuisine','country']]
    df2 = (df2.loc[:, ['country', 'cuisine']].groupby('country')
                                                .count()
                                                .sort_values('cuisine',ascending=False)
                                                .reset_index())
    
    fig=px.bar(df2, x='cuisine', y='country',category_orders={'country': df2['country'].tolist()})
    
    fig.update_layout(xaxis=dict(title='Count',title_font=dict(size=20)), yaxis=dict(title=''),xaxis_tickfont=dict(size=15), 
                      yaxis_tickfont=dict(size=15),height=500,margin=dict(t=0))
    
    st.plotly_chart(fig,use_container_width=True)

def average_rating (df):
    df_aux = (df.loc[:, ['country', 'aggregate_rating']].groupby('country')
                                                      .mean()
                                                      .sort_values('aggregate_rating',ascending=False)
                                                      .reset_index())
    
    fig=px.bar(df_aux, x='aggregate_rating', y='country',category_orders={'country': df_aux['country'].tolist()})
    
    fig.update_layout(xaxis=dict(title='0-5',title_font=dict(size=20)), yaxis=dict(title=''),xaxis_tickfont=dict(size=15), 
                      yaxis_tickfont=dict(size=15),height=500,margin=dict(t=0))
    
    st.plotly_chart(fig,use_container_width=True)

def average_cost_for_two (df):
    df_aux = (df.loc[:, ['country', 'average_cost_for_two']].groupby('country')
                                                            .mean()
                                                            .sort_values('average_cost_for_two',ascending=False)
                                                            .reset_index()) 
    
    fig=px.bar(df_aux, x='average_cost_for_two', y='country',category_orders={'country': df_aux['country'].tolist()})
    
    fig.update_layout(xaxis=dict(title='Price in dollars ($)',title_font=dict(size=20)), yaxis=dict(title=''),xaxis_tickfont=dict(size=15), 
                      yaxis_tickfont=dict(size=15),height=500,margin=dict(t=0))
    
    st.plotly_chart(fig,use_container_width=True)

def price_range(df):
    df_aux = (df.loc[:, ['country', 'price_range']].groupby('country')
                                                              .value_counts()
                                                              .sort_values(ascending=False)
                                                              .reset_index())
                    
    df_aux['percentage'] = df_aux.groupby('country')['count'].transform(lambda x: x / x.sum() * 100)
    df_aux = df_aux.sort_values(by=['percentage'], ascending=False)
    
    category_order = ['gourmet', 'expensive', 'normal', 'cheap']
    color_mapping = {'cheap': 'deepskyblue', 'normal': 'dodgerblue', 'expensive': 'mediumblue', 'gourmet': 'darkblue'}

    fig=px.histogram(df_aux, x='count', y='country', hover_data='price_range', color="price_range",
                                                 barnorm='percent',
                                                 category_orders={'price_range': category_order},
                                                 color_discrete_map=color_mapping)

    fig.update_layout(xaxis=dict(title='Percentage (%)',title_font=dict(size=20)),
                      yaxis=dict(title=''),
                      xaxis_tickfont=dict(size=15), yaxis_tickfont=dict(size=15),
                      legend=dict(font=dict(size=15)), legend_title_text='',height=500,margin=dict(t=0))
    
    st.plotly_chart(fig,use_container_width=True)

def cuisine_country_proportion (df):
    df2=cuisine(df)
    df3=df2[['country','cuisine']].groupby('country').value_counts().reset_index()
    
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

def selected_cuisine_country_proportion (df3,cuisine1):
    df4=cuisine(df3)
    df5=df4[['country','cuisine']].groupby('country').value_counts().reset_index()
    df5['sum'] = df5.groupby('country')['count'].transform('sum')
    df5=df5[df5['cuisine']==cuisine1]
    df5['percentage'] = df5.apply(lambda row: (row['count'] *100) / row['sum'], axis=1)
    df5=df5.sort_values('percentage',ascending=False)
    
    fig = px.bar(df5, x='percentage', y='country',category_orders={'country': df5['country'].tolist()},
                 labels={'percentage': 'Percentage (%)', 'country': 'Country'},
                 height=600)
    
    # Personalizar layout
    fig.update_layout(xaxis=dict(title='Percentage (%)',title_font=dict(size=20)),yaxis=dict(title=''),xaxis_tickfont=dict(size=15), 
                          yaxis_tickfont=dict(size=15),height=500,margin=dict(t=0),showlegend=False)

    st.plotly_chart(fig,use_container_width=True)





