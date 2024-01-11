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

df_raw=pd.read_csv('../data/train_raw.csv')

# Cleaning==============================================================
df_raw.columns= df_raw.columns.str.lower()

df_raw=df_raw.rename(columns={'id':'delivery_id'})
df_raw=df_raw.rename(columns={'weatherconditions':'weather_conditions'})
df_raw=df_raw.rename(columns={'city':'city_region'})

df_raw = df_raw[~df_raw.isin(['NaN ']).any(axis=1)]

df_raw['delivery_person_id']=df_raw['delivery_person_id'].replace(' ', '', regex=True).str.lower()

df_raw['delivery_person_age']=df_raw['delivery_person_age'].astype(int)

df_raw['delivery_person_ratings']=df_raw['delivery_person_ratings'].astype(float).replace({'  ':0})

df_raw['restaurant_latitude']=df_raw['restaurant_latitude'].astype(str)
df_raw['restaurant_latitude']=df_raw['restaurant_latitude'].replace('-','',regex=True)
df_raw['restaurant_longitude']=df_raw['restaurant_longitude'].astype(str)
df_raw['restaurant_latitude']=df_raw['restaurant_latitude']  .apply(lambda x: '-23.5489'  if x == '0.0' else x)
df_raw['restaurant_longitude']=df_raw['restaurant_longitude'].apply(lambda x: '-46.6388'  if x == '0.0' else x)

coords = tuple(zip(df_raw['restaurant_latitude'], df_raw['restaurant_longitude']))
location = reverse_geocode.search(coords)
city = [x.get('city') for x in location]
df_raw['city'] = city
df_raw['city']=df_raw['city'].apply(lambda x: 'Unknown'  if x == 'São Paulo' else x).str.lower()

df_raw['order_date']=pd.to_datetime(df_raw['order_date'],format='%d-%m-%Y')

df_raw['weather_conditions']=df_raw['weather_conditions'].replace(' ', '_', regex=True).str.lower()
df_raw['weather_conditions']=df_raw['weather_conditions'].replace('conditions_', '', regex=True)

df_raw['road_traffic_density']=df_raw['road_traffic_density'].replace(' ', '', regex=True).str.lower()

df_raw['type_of_order']=df_raw['type_of_order'].replace(' ', '', regex=True).str.lower()

df_raw['type_of_vehicle']=df_raw['type_of_vehicle'].replace(' ', '', regex=True)

df_raw['multiple_deliveries']=df_raw['multiple_deliveries'].astype(int)

df_raw['festival']=df_raw['festival'].replace(' ', '', regex=True).str.lower()

df_raw['city_region']=df_raw['city_region'].replace(' ', '', regex=True).str.lower()

df_raw['time_taken(min)']=df_raw['time_taken(min)'].replace('(min)', '', regex=True)
df_raw['time_taken(min)']=df_raw['time_taken(min)'].replace('\(\)', '', regex=True)
df_raw['time_taken(min)']=df_raw['time_taken(min)'].astype(int)

df=df_raw.copy()

# Barra lateral=====================================================================
st.set_page_config(layout='wide')
# st.dataframe(df)

# image_path='logo.png'
# image=Image.open(image_path)
# st.sidebar.image(image,width=120)

st.header('Marketplace - Client Vision')
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

# filtro de data
rows=df['order_date'] < date_slider
df=df.loc[rows,:]

# filtro de trânsito
rows=df['road_traffic_density'].isin(traffic)
df=df.loc[rows,:]

# Layout central===========================================================

tab1,tab2,tab3=st.tabs(['Management Vision','Tactical Vision','Geographic Vision'])

with tab1:
    with st.container():
        # Quantidade de pedidos por dia.
        st.markdown("<h1 style='text-align: center;'>N° of orders per day </h1>", unsafe_allow_html=True)
        
        df_aux = df.loc[:, ['delivery_id', 'order_date']].groupby('order_date').count().reset_index()
        df_aux.columns = ['order_date', 'order_qtt']
    
        fig=px.bar(df_aux, x='order_date', y='order_qtt',labels={"order_date": "Order date","order_qtt": "N° of orders"})
        st.plotly_chart(fig,use_container_width=True)

    with st.container():        
        col1,col2=st.columns(2)
        
        with col1:
            # Distribuição dos pedidos por tipo de tráfego.
            st.markdown("<h1 style='text-align: center;'>Orders by traffic type </h1>", unsafe_allow_html=True)
            # st.markdown("<h1 style='padding-bottom:5px';'></h1>", unsafe_allow_html=True)

            df_aux = df[['delivery_id', 'road_traffic_density']].groupby('road_traffic_density').count().reset_index()
            df_aux['perc_delivery_id'] = 100 * (df_aux['delivery_id'] / df_aux['delivery_id'].sum())
            
            fig=px.pie(df_aux, values='perc_delivery_id', names='road_traffic_density')
            st.plotly_chart(fig,use_container_width=True)

        with col2:
            # Comparação do volume de pedidos por tipo de cidade e tipo de tráfego.
            st.markdown("<h1 style='text-align: center;'>Orders by region/traffic</h1>", unsafe_allow_html=True)

            df_aux = df[[ 'delivery_id', 'city_region', 'road_traffic_density']].groupby(['city_region', 'road_traffic_density']).count().reset_index()
            df_aux['perc_delivery_id'] = 100 * (df_aux['delivery_id'] / df_aux['delivery_id'].sum())
            df_aux=df_aux.sort_values(by='perc_delivery_id',ascending=False)
            
            fig=px.bar(df_aux, x='city_region', y='delivery_id', color='road_traffic_density', barmode='group', 
                                                        labels={'delivery_id':'N° of orders','city_region':'Region','road_traffic_density':'Traffic density'})
            st.plotly_chart(fig,use_container_width=True)

with tab2:
    col1,col2=st.columns(2)

    with col1:
        # Quantidade de pedidos por Semana
        st.markdown("<h1 style='text-align: center;'>N° of orders per week</h1>", unsafe_allow_html=True)
        st.markdown("<h1 style='padding-bottom:35px';'></h1>", unsafe_allow_html=True)

        df['week_of_year'] = df['order_date'].dt.strftime("%U")
        df_aux = df.loc[:, ['delivery_id', 'week_of_year']].groupby('week_of_year').count().reset_index()
        
        # gráfico
        fig=px.bar(df_aux, x='week_of_year', y='delivery_id',labels={'week_of_year':'Week of the year','delivery_id':'N° of orders'})
        st.plotly_chart(fig,use_container_width=True)

    with col2:
        # A quantidade de pedidos por entregador por semana.
        
        st.markdown("<h1 style='text-align: center;'>N° of orders per deliveryman and week</h1>", unsafe_allow_html=True)
        # Quantidade de pedidos por entregador por Semana
        df_aux1 = df.loc[:, ['delivery_id', 'week_of_year']].groupby('week_of_year').count().reset_index()
        df_aux2 = df.loc[:, ['delivery_person_id', 'week_of_year']].groupby('week_of_year').nunique().reset_index()
        df_aux = pd.merge(df_aux1, df_aux2, how='inner')
        
        # Quantas entregas na semana / Quantos entregadores únicos por semana
        df_aux['order_by_delivery'] = df_aux['delivery_id'] / df_aux['delivery_person_id']
        
        # # gráfico
        fig=px.line(df_aux, x='week_of_year', y='order_by_delivery',labels={'week_of_year':'Week of the year','order_by_delivery':'Orders / rDeliverymans'})
        st.plotly_chart(fig,use_container_width=True)

with tab3:
    # A localização central de cada cidade por tipo de tráfego
    st.markdown("<h1 style='text-align: center;'>City location by traffic</h1>", unsafe_allow_html=True)
    columns = ['city_region', 'road_traffic_density', 'delivery_location_latitude','delivery_location_longitude']
    
    columns_groupby = ['city_region', 'road_traffic_density']
    
    data_plot = df.loc[:, columns].groupby(columns_groupby).median().reset_index()
    data_plot = data_plot[data_plot['city_region'] != 'NaN']
    data_plot = data_plot[data_plot['road_traffic_density'] != 'NaN']
    
    # Desenhar o mapa
    map_ = folium.Map(zoom_start=11)
    for index, location_info in data_plot.iterrows():
        folium.Marker([location_info['delivery_location_latitude'],
        location_info['delivery_location_latitude']],
        popup=location_info[['city_region', 'road_traffic_density']]).add_to(map_)
    folium_static(map_,width=1024,height=600)
# st.dataframe(df.head())





























