import pandas as pd
import numpy as np
import inflection
import folium
import streamlit as st
from folium.plugins import MarkerCluster,MousePosition
import plotly.express as px
import plotly.graph_objects as go
from streamlit_folium import folium_static

# functions=============================================
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

COLORS = {
"3F7E00": "darkgreen",
"5BA829": "green",
"9ACD32": "lightgreen",
"CDD614": "orange",
"FFBA00": "red",
"CBCBC8": "darkred",
"FF7800": "darkred"}

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

#==================================================================================================

# load dataset
df_raw=pd.read_csv('../data/zomato_raw.csv')

# cleaning==============================================
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

# df_raw[df_raw['restaurant_id']==95314]
df_raw.loc[3981,'latitude']=10.023286
df_raw.loc[3981,'longitude']=76.311371

# df_raw[df_raw['restaurant_id']==18445965]
df_raw.loc[6625,'latitude']=-25.7449
df_raw.loc[6625,'longitude']=28.1878

list=df_raw['cuisines'].str.split(',').apply(len)
df_raw['cuisines_n°']=list

df_raw['has_table_booking']=df_raw['has_table_booking'].apply(lambda x: 'Yes' if x==1 else 'No')
df_raw['has_online_delivery']=df_raw['has_online_delivery'].apply(lambda x: 'Yes' if x==1 else 'No')
df_raw['is_delivering_now']=df_raw['is_delivering_now'].apply(lambda x: 'Yes' if x==1 else 'No')

df_raw=df_raw.assign(var1=df_raw['cuisines'].str.split(',')).explode('var1').rename(columns={'var1':'cuisine'})
df_raw=df_raw.replace(' ','', regex=True).drop_duplicates(ignore_index=True)

replace_dict = {'UnitedStatesofAmerica': 'United States of America', 'UnitedArabEmirates': 'United Arab Emirates',
                'NewZeland':'New Zealand','SouthAfrica':'South Africa','SriLanka':'Sri Lanka'}
df_raw['country'] = df_raw['country'].replace(replace_dict)

df=df_raw.copy()

# Barra lateral=====================================================================
st.set_page_config(layout='wide')
# st.dataframe(df)

# image_path='logo.png'
# image=Image.open(image_path)
# st.sidebar.image(image,width=120)

st.markdown("<h1 style='text-align: center;'>Country Vision</h1>",unsafe_allow_html=True)
st.sidebar.markdown('# Eat Well Company')
st.sidebar.markdown("""---""")


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
# rows2=df2['price_range'].isin(price)
# df2=df2.loc[rows2,:]

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

rows=df['is_delivering_now'].isin(online)
df=df.loc[rows,:]

# filtro de culinaria
st.sidebar.markdown("""
    <div style="margin-bottom: -70px;">
        <span style="font-size:20px; font-weight:bold;">Cuisine</span>
    </div>
""", unsafe_allow_html=True)

df['count'] = df.groupby('cuisine')['cuisine'].transform('count')
df=df.sort_values('count',ascending=False)
df['cuisine'] = df['cuisine'] + ' (' + df['count'].astype(str) + ')'
df=df.drop(columns=['count'])
cuisine=df['cuisine'].unique()
cuisine=np.insert(cuisine, 0, 'All')
cuisines = st.sidebar.selectbox('cuisine', cuisine, label_visibility="hidden")

if cuisines == 'All':
    df=df.loc[(df['cuisine']==df['cuisine'])]
else:
    df=df.loc[(df['cuisine']==cuisines)]

# filtro de reset
reset_button = st.sidebar.button("Reset Visualizations")

if reset_button:
    df = df_raw.copy()
else:
    print('')

# plots===================================================================================
# with tab1:
with st.container():

    col1,col2=st.columns(2)
    with col1:
        st.markdown("<h3 style='text-align: center;'>N° of restaurants</h3>",unsafe_allow_html=True)

        df_aux=df.drop_duplicates(subset=['restaurant_id'])
        df_aux = (df_aux.loc[:, ['country', 'restaurant_id']].groupby('country')
                                                      .count()
                                                      .sort_values('restaurant_id',ascending=False)
                                                      .reset_index())
        
        fig=px.bar(df_aux, x='restaurant_id', y='country', category_orders={'country': df_aux['country'].tolist()})
        
        fig.update_layout(xaxis=dict(title=''), yaxis=dict(title=''),xaxis_tickfont=dict(size=15), 
                          yaxis_tickfont=dict(size=15),height=500,margin=dict(t=0))
        
        st.plotly_chart(fig,use_container_width=True)
            
    with col2:
        st.markdown("<h3 style='text-align: center;'>Cuisines</h3>",unsafe_allow_html=True)
        
        df2=df[['cuisines','country']]
        df2=df2.assign(var1=df2['cuisines'].str.split(',')).explode('var1').rename(columns={'var1':'all'})
        df2= df2.replace(' ','', regex=True)
        df2=df2.drop(columns=['cuisines'])
        df2=df2[['country','all']]
        df2=df2.drop_duplicates(ignore_index=True)
        df2 = (df2.loc[:, ['country', 'all']].groupby('country')
                                                    .count()
                                                    .sort_values('all',ascending=False)
                                                    .reset_index())
        
        fig=px.bar(df2, x='all', y='country',category_orders={'country': df2['country'].tolist()})
        
        fig.update_layout(xaxis=dict(title=''), yaxis=dict(title=''),xaxis_tickfont=dict(size=15), 
                          yaxis_tickfont=dict(size=15),height=500,margin=dict(t=0))
        
        st.plotly_chart(fig,use_container_width=True)

with st.container():

    col1,col2=st.columns(2)
    with col1:
        st.markdown("<h3 style='text-align: center;'>Average rating</h3>",unsafe_allow_html=True)
        df_aux=df.drop_duplicates(subset=['restaurant_id'])
        df_aux = (df_aux.loc[:, ['country', 'aggregate_rating']].groupby('country')
                                                          .mean()
                                                          .sort_values('aggregate_rating',ascending=False)
                                                          .reset_index())
        
        fig=px.bar(df_aux, x='aggregate_rating', y='country',category_orders={'country': df_aux['country'].tolist()})
        
        fig.update_layout(xaxis=dict(title=''), yaxis=dict(title=''),xaxis_tickfont=dict(size=15), 
                          yaxis_tickfont=dict(size=15),height=500,margin=dict(t=0))
        
        st.plotly_chart(fig,use_container_width=True)
            
    with col2:
        st.markdown("<h3 style='text-align: center;'>Average cost for two ($)</h3>",unsafe_allow_html=True)
        df_aux=df.drop_duplicates(subset=['restaurant_id'])
        df_aux = (df_aux.loc[:, ['country', 'average_cost_for_two']].groupby('country')
                                                                .mean()
                                                                .sort_values('average_cost_for_two',ascending=False)
                                                                .reset_index()) 
        
        fig=px.bar(df_aux, x='average_cost_for_two', y='country',category_orders={'country': df_aux['country'].tolist()})
        
        fig.update_layout(xaxis=dict(title=''), yaxis=dict(title=''),xaxis_tickfont=dict(size=15), 
                          yaxis_tickfont=dict(size=15),height=500,margin=dict(t=0))
        
        st.plotly_chart(fig,use_container_width=True)

with st.container():
    st.markdown("<h3 style='text-align: center;'>Price range (%)</h3>",unsafe_allow_html=True)
    df_aux=df.drop_duplicates(subset=['restaurant_id'])
    df_aux = (df_aux.loc[:, ['country', 'price_range']].groupby('country')
                                                  .value_counts()
                                                  .sort_values(ascending=False)
                                                  .reset_index())
    
    df_aux['percentage'] = df_aux.groupby('country')['count'].transform(lambda x: x / x.sum() * 100)
    df_aux = df_aux.sort_values(by=['percentage'], ascending=True)
    
    ordered_countries = df_aux[df_aux['price_range'] == 'gourmet']['country'].tolist()
    category_order = ['gourmet', 'expensive', 'normal', 'cheap']
    color_mapping = {'cheap': 'deepskyblue', 'normal': 'dodgerblue', 'expensive': 'mediumblue', 'gourmet': 'darkblue'}

    fig=px.histogram(df_aux, x='count', y='country', hover_data='price_range', color="price_range",
                                                 barnorm='percent',
                                                 category_orders={'price_range': category_order},
                                                 color_discrete_map=color_mapping)
    
    fig.update_xaxes(categoryorder='array', categoryarray=ordered_countries)
    
    fig.update_layout(xaxis=dict(title=''), yaxis=dict(title=''),xaxis_tickfont=dict(size=15), yaxis_tickfont=dict(size=15),
                      legend=dict(font=dict(size=15)), legend_title_text='', height=500)
    
    st.plotly_chart(fig,use_container_width=True)
                







