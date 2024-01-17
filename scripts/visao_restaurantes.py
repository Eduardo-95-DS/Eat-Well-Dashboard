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
184: "Singapure",
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

def cuisines (df,col):
    df2=df['cuisines'].str.split(',',expand=True)
    df2= df2.replace(',','', regex=True)
    df2= df2.replace(' ','', regex=True)
    df2[col]=df[col]
    df2.fillna('empty', inplace=True)
    df2=df2.drop_duplicates(ignore_index=True)
    
    df2['Combined'] = df2[0].astype(str) +','+ df2[1] +','+df2[2]+','+df2[3]+','+df2[4]+','+df2[5]+','+df2[6]+','+df2[7] 
    
    df2= df2.replace(',empty','', regex=True)
    df2=df2[['Combined',col]]
    df2=df2.assign(var1=df2['Combined'].str.split(',')).explode('var1').rename(columns={'var1':'cuisines'})
    df2=df2.drop(columns=['Combined'])
    df2=df2.drop_duplicates(ignore_index=True)

    return df2

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
# df_raw['count'] = df_raw.groupby('cuisine')['cuisine'].transform('count')
# df_raw['cuisine'] = df_raw['cuisine'] + ' (' + df_raw['count'].astype(str) + ')'
# df_raw=df_raw.drop(columns=['count'])

replace_dict = {'UnitedStatesofAmerica': 'United States of America', 'UnitedArabEmirates': 'United Arab Emirates',
                'NewZeland':'New Zealand','SouthAfrica':'South Africa','Srilanka':'Sri Lanka'}
df_raw['country'] = df_raw['country'].replace(replace_dict)

df=df_raw.copy()

# Barra lateral=====================================================================
st.set_page_config(layout='wide')
# st.dataframe(df)

# image_path='logo.png'
# image=Image.open(image_path)
# st.sidebar.image(image,width=120)

st.markdown("<h1 style='text-align: center;'>Restaurant Vision</h1>",unsafe_allow_html=True)
st.sidebar.markdown('# Eat Well Company')
st.sidebar.markdown("""---""")


# initial_city_options = cities.copy()
# initial_cuisine_options = cuisine.copy()
# initial_price_options = price.copy()
# initial_booking_options = booking.copy()
# initial_delivery_options = online_delivery.copy()
# initial_now_options = delivering.copy()


# filtro de país
st.sidebar.markdown("""
    <div style="margin-bottom: -70px;">
        <span style="font-size:20px; font-weight:bold;">Country</span>
    </div>
""", unsafe_allow_html=True)

countries = ['All','United States of America', 'Canada', 'Brazil', 'England','Australia', 'New Zealand', 'Philippines', 'Indonesia',
    'India', 'Sri Lanka', 'United Arab Emirates', 'Qatar','Turkey', 'Singapure','South Africa']
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

# booking=df['has_table_booking'].unique()
# booking=np.insert(booking, 0, 'All')
# book = st.sidebar.selectbox('table', booking, label_visibility="hidden")

# if book == 'All':
#     df=df.loc[(df['has_table_booking']==df['has_table_booking'])]
# else:
#     df=df.loc[(df['has_table_booking']==book)]
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

# online_delivery=df['has_online_delivery'].unique()
# online_delivery=np.insert(online_delivery, 0, 'All')
# delivery = st.sidebar.selectbox('', online_delivery)

# if delivery == 'All':
#     df=df.loc[(df['has_online_delivery']==df['has_online_delivery'])]
# else:
#     df=df.loc[(df['has_online_delivery']==delivery)]

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

# delivering=df['is_delivering_now'].unique()
# delivering=np.insert(delivering, 0, 'All')
# now = st.sidebar.selectbox('delivering', delivering, label_visibility="hidden")

# if now == 'All':
#     df=df.loc[(df['is_delivering_now']==df['is_delivering_now'])]
# else:
#     df=df.loc[(df['is_delivering_now']==now)]

delivery= st.sidebar.multiselect('',['Yes','No'],
                               default=['Yes','No'],key='delivery')

rows=df['is_delivering_now'].isin(online)
df=df.loc[rows,:]

# filtro de reset
reset_button = st.sidebar.button("Reset Visualizations")

if reset_button:
    df = df_raw.copy()
    country = 'All'
else:
    if country == 'All':
        df=df.loc[(df['country']==df['country'])]
    else:
        df=df.loc[(df['country']==country)]

# plots======================================================================
with st.container():

    col1,col2=st.columns(2)
    with col1:
        
        st.markdown("<h4 style='text-align:center;margin-top: 0px;'>Top rated</h4>",unsafe_allow_html=True)
    
        # df1=df[df['votes']>3]
        df1=df.drop_duplicates(subset=['restaurant_id'])
        df1=(df1[['restaurant_name','aggregate_rating','price_range','cuisines','country','city','votes']]
                .sort_values(by=['aggregate_rating','votes'],ascending=False)
                .rename(columns={'restaurant_name':'restaurant','aggregate_rating':'rating','price_range':'price'})
                .reset_index(drop=True))
    
        st.dataframe(df1)

    with col2:
        
        st.markdown("<h4 style='text-align:center;margin-top: 0px;'>Worst rated</h4>",unsafe_allow_html=True)
    
        df1=df[df['votes']>3]
        df1=df1.drop_duplicates(subset=['restaurant_id'])        
        df1=(df1[['restaurant_name','aggregate_rating','price_range','cuisines','country','city','votes']]
                .sort_values(by=['aggregate_rating','votes'],ascending=True)
                .rename(columns={'restaurant_name':'restaurant','aggregate_rating':'rating','price_range':'price'})
                .reset_index(drop=True))
        
        st.dataframe(df1)

with st.container():
    
    st.markdown("<h4 style='text-align:center;margin-top: 0px;'>Avg cost for two</h4>",unsafe_allow_html=True)

    # df1=df.copy()
    df1=df.drop_duplicates(subset=['restaurant_id'])

    df1=(df1[['restaurant_name','country','city','average_cost_for_two']].groupby(['restaurant_name','country','city'])
                                                  .mean()
                                                  .sort_values('average_cost_for_two',ascending=False)
                                                  .reset_index()
                                                  .head(10))

    fig = px.bar(df1, x='average_cost_for_two', y="restaurant_name", color='country',text='city',text_auto=True,
                 category_orders={'restaurant_name': df1['restaurant_name'].tolist()})
    
    fig.update_layout(xaxis=dict(title=''), yaxis=dict(title=''),xaxis_tickfont=dict(size=15), 
                      yaxis_tickfont=dict(size=15),legend=dict(font=dict(size=15)), 
                      legend_title_text='',height=500,margin=dict(t=0))
    
    fig.update_traces(marker_line_color='black', marker_line_width=2, selector=dict(type='bar'))
    
    st.plotly_chart(fig,use_container_width=True)    












