import numpy as np
import inflection
import streamlit as st
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster,MousePosition
import plotly.express as px
import plotly.graph_objects as go

# cleaning===========================================================
def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df.columns

def country_name(country_id):
    COUNTRIES = {
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zeland",
    162: "Philippines",
    166: "Qatar",
    184: "Singapore",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America"}
    return COUNTRIES[country_id]

def create_price_tye(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"

def color_name(color_code):
    COLORS = {
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "orange",
    "FFBA00": "red",
    "CBCBC8": "darkred",
    "FF7800": "darkred"}
    return COLORS[color_code]

def dollarize (df):
    df['average_cost_for_two']=np.where(df['currency']=='Botswana Pula(P)',   df['average_cost_for_two'] * 0.074, df['average_cost_for_two'] )
    df['average_cost_for_two']=np.where(df['currency']=='Brazilian Real(R$)', df['average_cost_for_two'] * 0.21, df['average_cost_for_two'] )
    df['average_cost_for_two']=np.where(df['currency']=='Emirati Diram(AED)', df['average_cost_for_two'] * 0.27, df['average_cost_for_two'] )
    df['average_cost_for_two']=np.where(df['currency']=='Indian Rupees(Rs.)', df['average_cost_for_two'] * 0.012, df['average_cost_for_two'] )
    df['average_cost_for_two']=np.where(df['currency']=='Indonesian Rupiah(IDR)', df['average_cost_for_two'] * 0.000065, df['average_cost_for_two'] )
    df['average_cost_for_two']=np.where(df['currency']=='Pounds(£)', df['average_cost_for_two'] * 1.27, df['average_cost_for_two'] )
    df['average_cost_for_two']=np.where(df['currency']=='Qatari Rial(QR)', df['average_cost_for_two'] * 0.27, df['average_cost_for_two'] )
    df['average_cost_for_two']=np.where(df['currency']=='Rand(R)', df['average_cost_for_two'] * 0.054, df['average_cost_for_two'] )
    df['average_cost_for_two']=np.where(df['currency']=='Sri Lankan Rupee(LKR)', df['average_cost_for_two'] * 0.0031, df['average_cost_for_two'] )
    df['average_cost_for_two']=np.where(df['currency']=='Turkish Lira(TL)', df['average_cost_for_two'] * 0.034, df['average_cost_for_two'] )
    return df

def get_country_center_coordinates(country):
    country_coordinates = {
        'World View' : [0, 0],
        'United States of America': [37.0902, -95.7129],
        'Canada': [56.1304, -106.3468],
        'Brazil': [-14.2350, -51.9253],
        'England': [51.5099, -0.1180],
        'Australia': [-25.2744, 133.7751],
        'New Zealand': [-40.9006, 174.8860],
        'Philippines': [12.8797, 121.7740],
        'Indonesia': [-0.7893, 113.9213],
        'India': [20.5937, 78.9629],
        'Sri Lanka': [7.8731, 80.7718],
        'United Arab Emirates': [23.4241, 53.8478],
        'Qatar': [25.2769, 51.5201],
        'Turkey': [38.9637, 35.2433],
        'Singapore': [1.3521, 103.8198]}

    return country_coordinates.get(country, (0, 0))


def cleaning(df_raw):
    df_raw=df_raw.drop_duplicates(keep='first')
    
    df_raw=df_raw.dropna(ignore_index=True)
    
    df_raw.columns=rename_columns(df_raw)
    
    list=[]
    for index, row in df_raw.iterrows():
        codes=country_name(row['country_code'])
        list.append(codes)
    
    df_raw['country']=list
    len(df_raw['country'].unique())
    
    df_raw['price_range']=df_raw['price_range'].apply(create_price_tye)
    df_raw['price_range'].unique()
    
    list=[]
    for index, row in df_raw.iterrows():
        codes=color_name(row['rating_color'])
        list.append(codes)
    
    df_raw['rating_color']=list
    df_raw['rating_color'].unique()
    
    df_raw=dollarize(df_raw)
    
    df_raw=df_raw.drop(columns=['switch_to_order_menu'])
    
    df_raw=df_raw.replace(25000017,25,inplace=False)
    
    df_raw.loc[3981,'latitude']=10.023286
    df_raw.loc[3981,'longitude']=76.311371
    
    df_raw.loc[6625,'latitude']=-25.7449
    df_raw.loc[6625,'longitude']=28.1878
    
    list=df_raw['cuisines'].str.split(',').apply(len)
    df_raw['cuisines_n°']=list
    
    df_raw['has_table_booking']=df_raw['has_table_booking'].apply(lambda x: 'Yes' if x==1 else 'No')
    df_raw['has_online_delivery']=df_raw['has_online_delivery'].apply(lambda x: 'Yes' if x==1 else 'No')
    df_raw['is_delivering_now']=df_raw['is_delivering_now'].apply(lambda x: 'Yes' if x==1 else 'No')
    
    df_raw['cuisines']=df_raw['cuisines'].replace(' ','', regex=True)
    
    return df_raw

def cuisine_filter (df):
    df2=df.assign(cuisine=df['cuisines'].str.split(',')).explode('cuisine')
    df2['cuisine']=df2['cuisine'].replace(' ','', regex=True)
    df2['count'] = df2.groupby('cuisine')['cuisine'].transform('count')
    df2=df2.sort_values('count',ascending=False)
    cuisine=df2['cuisine'].unique()
    cuisine=np.insert(cuisine, 0, 'All')
    return cuisine

# plots========================================================================
def overview_map(df,selected_country):
    center_coordinates = get_country_center_coordinates(selected_country)
        
    if selected_country == 'World View':
        bounds = [[-90, -180], [90, 180]]
    else:
        bounds = None
        
    st.markdown("<h1 style='text-align: Center;'>World Map</h1>", unsafe_allow_html=True)

    # Criar o mapa
    overview_map = folium.Map(location=center_coordinates,zoom_start=4, control_scale=True)
    
    if selected_country == 'World View':
        overview_map.fit_bounds(bounds)
        
    marker_cluster = MarkerCluster().add_to(overview_map)
    
    for i, row in df.iterrows():
  
        popup_text = f'''<div style="font-size: 14px;">
                          Restaurant name: <b>{str(row["restaurant_name"])}</b><br>
                          Price range: <b>{str(row["price_range"])}</b><br>
                          Cuisines: <b>{str(row["cuisines"])}</b><br>
                          Avg cost for two ($): <b>{str(row["average_cost_for_two"])}</b><br>
                          Rating: <b>{str(row["aggregate_rating"])}</b>
                          </div>'''
                
        tooltip_text = f'''<div style="font-size: 14px;">
                          Restaurant name: <b>{str(row["restaurant_name"])}</b><br>
                          Price range: <b>{str(row["price_range"])}</b><br>
                          Cuisines: <b>{str(row["cuisines"])}</b><br>
                          Avg cost for two ($): <b>{str(row["average_cost_for_two"])}</b><br>
                          Rating: <b>{str(row["aggregate_rating"])}</b>
                          </div>'''
    
        folium.CircleMarker([row['latitude'], row['longitude']],
                            tooltip=tooltip_text,
                            color='green',  # Cor da borda
                            fill=True,
                            fill_opacity=0.8).add_to(marker_cluster)
        
    folium_static(overview_map,width=1024,height=600)


def cuisines_map(df):
    center_coordinates = get_country_center_coordinates(selected_country)
    
    if selected_country == 'World View':
        filtered_df = df  
    else:
        filtered_df = df[df['country'] == selected_country] 

    if selected_country == 'World View':
        bounds = [[-90, -180], [90, 180]]
    else:
        bounds = None
        
    st.markdown("<h1 style='text-align: center;'>Cuisines Map</h1>", unsafe_allow_html=True)
        
    # Criar o mapa
    cuisine_map = folium.Map(location=center_coordinates,zoom_start=4, control_scale=True)
    marker_cluster = MarkerCluster().add_to(cuisine_map)
        
    if selected_country == 'World View':
        cuisine_map.fit_bounds(bounds)
        
    for i, row in filtered_df.iterrows():
        cuisines_count = row['cuisines_n°']
        marker_size = int(row['cuisines_n°']) * 5

        if cuisines_count == 1:
            fill_color = 'red'
        elif 2 <= cuisines_count <= 3:
            fill_color = 'orange'
        elif 4 <= cuisines_count <= 6:
            fill_color = 'blue'
        elif cuisines_count == 7:
            fill_color = 'green'
        else:
            fill_color = 'gray'  # valores não mencionados
    
        popup_text = f'''<div style="font-size: 14px;">
                          Restaurant name: <b>{str(row["restaurant_name"])}</b><br>
                          Price range: <b>{str(row["price_range"])}</b><br>
                          Cuisines: <b>{str(row["cuisines"])}</b><br>
                          Avg cost for two ($): <b>{str(row["average_cost_for_two"])}</b><br>
                          Rating: <b>{str(row["aggregate_rating"])}</b>
                          </div>'''
                
        tooltip_text = f'''<div style="font-size: 14px;">
                          Restaurant name: <b>{str(row["restaurant_name"])}</b><br>
                          Price range: <b>{str(row["price_range"])}</b><br>
                          Cuisines: <b>{str(row["cuisines"])}</b><br>
                          Avg cost for two ($): <b>{str(row["average_cost_for_two"])}</b><br>
                          Rating: <b>{str(row["aggregate_rating"])}</b>
                          </div>'''
    
        folium.CircleMarker([row['latitude'], row['longitude']],
                            radius=marker_size,
                            tooltip=tooltip_text,
                            color='black',  # Cor da borda
                            fill=True,
                            fill_color=fill_color,
                            fill_opacity=0.8).add_to(marker_cluster)
    
    legend_html = '''
        <div style="position: fixed; 
                    bottom: 50px; left: 50px; width: 150px; height: 150px; 
                    border:2px solid grey; z-index:9999; font-size:14px;
                    background-color:white; opacity: .85; text-align: left; padding: 5px;">
          <h3 style="font-size: 16px; text-align: center;">Cuisines variety:</h3>
          <span style="color: red; font-size: 20px; vertical-align: middle;">■</span> 1 Cuisine <br>
          <span style="color: orange; font-size: 20px; vertical-align: middle;">■</span> 2-3 Cuisines <br>
          <span style="color: blue; font-size: 20px; vertical-align: middle;">■</span> 4-6 Cuisines <br>
          <span style="color: green; font-size: 20px; vertical-align: middle;">■</span> 7 Cuisines <br>
        </div>
        ''' 
    
    cuisine_map.get_root().html.add_child(folium.Element(legend_html))
    
    folium_static(cuisine_map, width=1024, height=600)

def price_map(df,selected_country):
    center_coordinates = get_country_center_coordinates(selected_country)
    
    if selected_country == 'World View':
        filtered_df = df  
    else:
        filtered_df = df[df['country'] == selected_country] 

    if selected_country == 'World View':
        bounds = [[-90, -180], [90, 180]]
    else:
        bounds = None
        
    st.markdown("<h1 style='text-align: center;'>Price Range Map</h1>", unsafe_allow_html=True)

    price_map = folium.Map(location=center_coordinates,zoom_start=4, control_scale=True)
    marker_cluster = MarkerCluster().add_to(price_map)

    if selected_country == 'World View':
        price_map.fit_bounds(bounds)
        
    price_color = {'gourmet': 'red', 'expensive': 'orange', 'normal': 'blue', 'cheap': 'green'}
    price_size = {'gourmet': 25, 'expensive': 20, 'normal': 15, 'cheap': 10}
        
    for i, row in filtered_df.iterrows():
        
        marker_size = price_size.get(row['price_range'], 8)  # Tamanho padrão é 8 se não estiver nas faixas especificadas
        fill_color = price_color.get(row['price_range'], 'gray')
    
        if fill_color == 'gray' and row['price_range'] == 'expensive':
            fill_color = 'orange'
            
        popup_text = f'''<div style="font-size: 14px;">
                          Restaurant name: <b>{str(row["restaurant_name"])}</b><br>
                          Price range: <b>{str(row["price_range"])}</b><br>
                          Cuisines: <b>{str(row["cuisines"])}</b><br>
                          Avg cost for two ($): <b>{str(row["average_cost_for_two"])}</b><br>
                          Rating: <b>{str(row["aggregate_rating"])}</b>
                          </div>'''
    
        tooltip_text = f'''<div style="font-size: 14px;">
                          Restaurant name: <b>{str(row["restaurant_name"])}</b><br>
                          Price range: <b>{str(row["price_range"])}</b><br>
                          Cuisines: <b>{str(row["cuisines"])}</b><br>
                          Avg cost for two ($): <b>{str(row["average_cost_for_two"])}</b><br>
                          Rating: <b>{str(row["aggregate_rating"])}</b>
                          </div>'''
    
        folium.CircleMarker([row['latitude'], row['longitude']],
                            radius=marker_size,
                            tooltip=tooltip_text,
                            color='black',  # Cor da borda
                            fill=True,
                            fill_color=fill_color,
                            fill_opacity=0.8).add_to(marker_cluster)
    
        legend_html = '''
            <div style="position: fixed; 
                        bottom: 50px; left: 50px; width: 150px; height: 150px; 
                        border:2px solid grey; z-index:9999; font-size:14px;
                        background-color:white; opacity: .85; text-align: left; padding: 5px;">
              <b style="font-size: 16px;">Price range:</b><br>
              <span style="color: red; font-size: 20px; vertical-align: middle;">■</span> Gourmet <br>
              <span style="color: orange; font-size: 20px; vertical-align: middle;">■</span> Expensive <br>
              <span style="color: blue; font-size: 20px; vertical-align: middle;">■</span> Normal <br>
              <span style="color: green; font-size: 20px; vertical-align: middle;">■</span> Cheap<br>
            </div>
            '''
        
    price_map.get_root().html.add_child(folium.Element(legend_html))
    folium_static(price_map,width=1024,height=600)

def agg_map (df):
    center_coordinates = get_country_center_coordinates(selected_country)
    
    if selected_country == 'World View':
        filtered_df = df  
    else:
        filtered_df = df[df['country'] == selected_country] 

    if selected_country == 'World View':
        bounds = [[-90, -180], [90, 180]]
    else:
        bounds = None
        
    st.markdown("<h1 style='text-align: center;'>Aggregate Rating Map</h1>", unsafe_allow_html=True)

    agg_map = folium.Map(location=center_coordinates,zoom_start=4,control_scale=True)
    marker_cluster = MarkerCluster().add_to(agg_map)
    
    rating_size = {'bad': 10, 'regular': 15, 'good': 20, 'excellent': 25}
    
    if selected_country == 'World View':
        agg_map.fit_bounds(bounds)
        
    for i, row in filtered_df.iterrows():
        rating = row['aggregate_rating']
    
        if rating == 0:
            fill_color = 'gray'
            rating_category = 'bad'  # Pode ser qualquer categoria,tamanho será o mesmo dos vermelhos
        elif 2.1 <= rating <= 3.5:
            fill_color = 'red'  
            rating_category = 'bad'
        elif 3.6 <= rating <= 4.0:
            fill_color = 'orange'  
            rating_category = 'regular'
        elif 4.1 <= rating <= 4.5:
            fill_color = 'blue'  
            rating_category = 'good'
        else:
            fill_color = 'green'  
            rating_category = 'excellent'
    
        marker_size = rating_size.get(rating_category, 10)  # Tamanho padrão é 10 se não estiver nas faixas especificadas
    
        popup_text = f'''<div style="font-size: 14px;">
                          Restaurant name: <b>{str(row["restaurant_name"])}</b><br>
                          Price range: <b>{str(row["price_range"])}</b><br>
                          Cuisines: <b>{str(row["cuisines"])}</b><br>
                          Avg cost for two ($): <b>{str(row["average_cost_for_two"])}</b><br>
                          Rating: <b>{str(row["aggregate_rating"])}</b>
                          </div>'''
    
        tooltip_text = f'''<div style="font-size: 14px;">
                          Restaurant name: <b>{str(row["restaurant_name"])}</b><br>
                          Price range: <b>{str(row["price_range"])}</b><br>
                          Cuisines: <b>{str(row["cuisines"])}</b><br>
                          Avg cost for two ($): <b>{str(row["average_cost_for_two"])}</b><br>
                          Rating: <b>{str(row["aggregate_rating"])}</b>
                          </div>'''
    
        folium.CircleMarker([row['latitude'], row['longitude']],
                            radius=marker_size,
                            tooltip=tooltip_text,
                            color='black',  # Cor da borda
                            fill=True,
                            fill_color=fill_color,
                            fill_opacity=0.8).add_to(marker_cluster)
    
        legend_html = '''
            <div style="position: fixed; 
                        bottom: 50px; left: 50px; width: 150px; height: 195px; 
                        border:2px solid grey; z-index:9999; font-size:14px;
                        background-color:white; opacity: .85; text-align: left; padding: 5px;">
              <b style="font-size: 16px;">Aggregate Rating:</b><br>
              <span style="color: gray; font-size: 20px; vertical-align: middle;">■</span> Not Rated (0)<br>
              <span style="color: red; font-size: 20px; vertical-align: middle;">■</span> Bad (2.1 - 3.5) <br>
              <span style="color: orange; font-size: 20px; vertical-align: middle;">■</span> Regular (3.6 - 4.0) <br>
              <span style="color: blue; font-size: 20px; vertical-align: middle;">■</span> Good (4.1 - 4.5) <br>
              <span style="color: green; font-size: 20px; vertical-align: middle;">■</span> Excellent (>4.5)<br>
            </div>
            '''
        
    agg_map.get_root().html.add_child(folium.Element(legend_html))
    
    folium_static(agg_map,width=1024,height=600)

def avg_map(df):
    center_coordinates = get_country_center_coordinates(selected_country)
    
    if selected_country == 'World View':
        filtered_df = df  
    else:
        filtered_df = df[df['country'] == selected_country] 

    if selected_country == 'World View':
        bounds = [[-90, -180], [90, 180]]
    else:
        bounds = None    
    
    st.markdown("<h1 style='text-align: center;'>Average Cost for Two Map</h1>", unsafe_allow_html=True)

    avg_map = folium.Map(location=center_coordinates, zoom_start=4, control_scale=True)
    marker_cluster = MarkerCluster().add_to(avg_map)
    
    cost_size = {'cheap': 10, 'normal': 15, 'expensive': 20, 'gourmet': 25}

    if selected_country == 'World View':
        avg_map.fit_bounds(bounds)
        
    for i, row in filtered_df.iterrows():
        avg_cost = row['average_cost_for_two']
    
        if 0 <= avg_cost <= 20:
            fill_color = 'green'  
            cost_category = 'cheap'
        elif 21 <= avg_cost <= 50:
            fill_color = 'blue'  
            cost_category = 'normal'
        elif 51 <= avg_cost <= 100:
            fill_color = 'orange' 
            cost_category = 'expensive'
        else:
            fill_color = 'red' 
            cost_category = 'gourmet'
    
        popup_text = f'''<div style="font-size: 14px;">
                          Restaurant name: <b>{str(row["restaurant_name"])}</b><br>
                          Price range: <b>{str(row["price_range"])}</b><br>
                          Cuisines: <b>{str(row["cuisines"])}</b><br>
                          Avg cost for two ($): <b>{str(row["average_cost_for_two"])}</b><br>
                          Rating: <b>{str(row["aggregate_rating"])}</b>
                          </div>'''
    
        marker_size = cost_size.get(cost_category, 10)  # Tamanho padrão é 10 se não estiver nas faixas especificadas
    
        tooltip_text = f'''<div style="font-size: 14px;">
                          Restaurant name: <b>{str(row["restaurant_name"])}</b><br>
                          Price range: <b>{str(row["price_range"])}</b><br>
                          Cuisines: <b>{str(row["cuisines"])}</b><br>
                          Avg cost for two ($): <b>{str(row["average_cost_for_two"])}</b><br>
                          Rating: <b>{str(row["aggregate_rating"])}</b>
                          </div>'''
    
        folium.CircleMarker([row['latitude'], row['longitude']],
                            radius=marker_size,
                            tooltip=tooltip_text,
                            color='black',  # Cor da borda
                            fill=True,
                            fill_color=fill_color,
                            fill_opacity=0.8).add_to(marker_cluster)
    
    legend_html = '''
        <div style="position: fixed; 
                    bottom: 50px; left: 50px; width: 150px; height: 195px; 
                    border:2px solid grey; z-index:9999; font-size:14px;
                    background-color:white; opacity: .85; text-align: left; padding: 5px;">
          <b style="font-size: 16px;">Average Cost for Two ($):</b><br>
          <span style="color: green; font-size: 20px; vertical-align: middle;">■</span> Cheap (0 - 20) <br>
          <span style="color: blue; font-size: 20px; vertical-align: middle;">■</span> Normal (21 - 50) <br>
          <span style="color: orange; font-size: 20px; vertical-align: middle;">■</span> Expensive (51 - 100) <br>
          <span style="color: red; font-size: 20px; vertical-align: middle;">■</span> Gourmet (>100)<br>
        </div>
        '''
    
    avg_map.get_root().html.add_child(folium.Element(legend_html))
    folium_static(avg_map,width=1024,height=600)
