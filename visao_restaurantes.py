# Libraries
import pandas         as pd
import numpy          as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit      as st
import folium
import requests
import reverse_geocode
from streamlit_folium import folium_static
from datetime  import datetime 
from haversine import haversine
from datetime  import time
from PIL       import Image

df=pd.read_csv('../data/train.csv')

df['order_date']=pd.to_datetime(df['order_date'])

# Barra lateral=====================================================================
st.set_page_config(layout='wide')
# st.dataframe(df)

# image_path='logo.png'
# image=Image.open(image_path)
# st.sidebar.image(image,width=120)

st.header('Marketplace - Restaurant Vision')
st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery In Town')
st.sidebar.markdown("""---""")



# Layout central===========================================================

tab1,tab2=st.tabs(['Management Vision',' '])

with tab1:
    with st.container():

        col1,col2,col3,col4,col5,col6=st.columns(6)

        with col1:
            st.markdown('##### Unique deliverymens')
            unique_delivery=len(df["delivery_person_id"].unique())
            col1.metric('',unique_delivery)
            # st.markdown("""---""")
                
        with col2:
            st.markdown('##### Avg delivery distance in km')
            df2 = df[~df.isin([-23.5489]).any(axis=1)].copy()
            cols=['restaurant_latitude','restaurant_longitude','delivery_location_latitude','delivery_location_longitude']
            df2['distance']=df2.loc[:,cols].apply(lambda x: haversine ((x['restaurant_latitude'],        x['restaurant_longitude']),
                                                                      (x['delivery_location_latitude'], x['delivery_location_longitude'])),
                                                                      axis=1)
            mean_dist=df2["distance"].mean().round()
            col2.metric('',mean_dist)
            # st.markdown("""---""")

        with col3:
            st.markdown("##### Avg delivery time w/")
            df1=(df[['festival','time_taken(min)']].groupby(['festival']).agg(mean_=('time_taken(min)','mean'),
                                                                              std_= ('time_taken(min)','std')).reset_index())
            df1=df1.loc[df1['festival']=='yes','mean_']
            col3.metric('',np.round(df1))
            # st.markdown("""---""")

        with col4:
            st.markdown("##### Avg delivery std w/festival")
            df1=(df[['festival','time_taken(min)']].groupby(['festival']).agg(mean_=('time_taken(min)','mean'),
                                                                              std_= ('time_taken(min)','std')).reset_index())
            df1=df1.loc[df1['festival']=='yes','std_']
            col4.metric('',np.round(df1))
            # st.markdown("""---""")
            
        with col5:
            st.markdown("##### Avg delivery time w/o festival")
            df1=(df[['festival','time_taken(min)']].groupby(['festival']).agg(mean_=('time_taken(min)','mean'),
                                                                              std_= ('time_taken(min)','std')).reset_index())
            df1=df1.loc[df1['festival']=='no','mean_']
            col5.metric('',np.round(df1))
            # st.markdown("""---""")
    
        with col6:
            st.markdown('##### Avg delivery std w/o festival')
            df1=(df[['festival','time_taken(min)']].groupby(['festival']).agg(mean_=('time_taken(min)','mean'),
                                                                              std_= ('time_taken(min)','std')).reset_index())
            df1=df1.loc[df1['festival']=='no','std_']
            col6.metric('',np.round(df1))
            # st.markdown("""---""")

    with st.container():
        st.markdown("""---""")
        # st.title('Avg delivery distance by city region')
        st.markdown('<h2 style="text-align: center;">Avg delivery distance by city region</h2>',unsafe_allow_html=True)
        dist=df2[['city_region','distance']].groupby('city_region').mean().reset_index()
        
        # fig=go.Figure(data=[go.Pie (labels=dist['city_region'], values=dist['distance'], pull=[0,0,0.1])])
        fig=px.pie(dist, values='distance', names='city_region', color_discrete_sequence=px.colors.sequential.RdBu)
        fig.update_traces(pull=[0,0.1,0],textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig,use_container_width=True)
        
    with st.container():

        col1,col2=st.columns(2)

        with col1:
            # st.title('Avg delivery time by city region')
            st.markdown("""---""")
            st.markdown('#### Avg delivery time by city region')
            df1=(df[['city_region','time_taken(min)']].groupby(['city_region']).agg(mean_=('time_taken(min)','mean'),
                                                                             std_= ('time_taken(min)','std')).sort_values('mean_',ascending=True).reset_index())
            fig=go.Figure()
            fig.add_trace(go.Bar(name='Control',x=df1['city_region'],y=df1['mean_'],error_y=dict(type='data',array=df1['std_'])))
            fig.update_traces(width=0.5)
            fig.update_layout(bargap=0.1,barmode='group')
            st.plotly_chart(fig,use_container_width=True)

        with col2:
            st.markdown("""---""")
            st.markdown('#### Avg/std delivery time by city region and type of order')
            st.markdown('#####')

            df1=(df[['city_region','type_of_order','time_taken(min)']].groupby(['city_region','type_of_order']).agg(mean_=('time_taken(min)','mean'),
                                                                             delivery_std= ('time_taken(min)','std')).reset_index())
            
            fig=px.sunburst(df1,path=['city_region','type_of_order'],values='mean_', color='delivery_std', color_continuous_scale='Reds',
                                                                             color_continuous_midpoint=np.average(df1['delivery_std']))
            st.plotly_chart(fig,use_container_width=True)
            
    with st.container():
        st.markdown("""---""")

        st.markdown('<h2 style="text-align: center;">Avg/std delivery time by city region and type of traffic</h2>',unsafe_allow_html=True)
        
        df1=(df[['city_region','road_traffic_density','time_taken(min)']].groupby(['city_region','road_traffic_density'])
                                                                     .agg(mean_=('time_taken(min)','mean'),
                                                                      delivery_std= ('time_taken(min)','std')).reset_index())
        
        fig=px.sunburst(df1,path=['city_region','road_traffic_density'],values='mean_', color='delivery_std', color_continuous_scale='Reds',
                                                                         color_continuous_midpoint=np.average(df1['delivery_std']))
        st.plotly_chart(fig,use_container_width=True)

        st.markdown("""---""")



















