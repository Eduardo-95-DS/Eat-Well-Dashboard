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
df_raw[['cuisines','cuisines_n°']].head(5)

df=df_raw.copy()

# Barra lateral=====================================================================
st.set_page_config(layout='wide')
# st.dataframe(df)

# image_path='logo.png'
# image=Image.open(image_path)
# st.sidebar.image(image,width=120)

st.header('Country Vision')
st.sidebar.markdown('# Eat Well Company')
st.sidebar.markdown("""---""")


tab1,tab2=st.tabs(['Management Vision',' '])

with tab1:
    with st.container():

        col1,col2=st.columns(2)
        with col1:
            st.markdown("<h3 style='text-align: center;'>Unique cuisines</h3>",unsafe_allow_html=True)
            df2=cuisines(df,'country')
            df_aux = (df2.loc[:, ['country', 'cuisines']].groupby('country')
                                                        .count()
                                                        .sort_values('cuisines',ascending=False)
                                                        .reset_index())
            fig=px.bar(df_aux, x='cuisines', y='country')
            st.plotly_chart(fig,use_container_width=True)
            # st.markdown("""---""")
                
        with col2:
            st.markdown("<h3 style='text-align: center;'>Average cost for two</h3>",unsafe_allow_html=True)
            df_aux = (df.loc[:, ['country', 'average_cost_for_two']].groupby('country')
                                                                    .mean()
                                                                    .sort_values('average_cost_for_two',ascending=False)
                                                                    .reset_index()) 
            fig=px.bar(df_aux, x='average_cost_for_two', y='country')
            st.plotly_chart(fig,use_container_width=True)
            # st.markdown("""---""")

    with st.container():

        col1,col2=st.columns(2)
        with col1:
            st.markdown("<h3 style='text-align: center;'>Aggregate rating</h3>",unsafe_allow_html=True)
            df_aux = (df.loc[:, ['country', 'aggregate_rating']].groupby('country')
                                                              .mean()
                                                              .sort_values('aggregate_rating',ascending=False)
                                                              .reset_index())
            fig=px.bar(df_aux, x='aggregate_rating', y='country')
            st.plotly_chart(fig,use_container_width=True)
            # st.markdown("""---""")
                
        with col2:
            st.markdown("<h3 style='text-align: center;'>N° of restaurants</h3>",unsafe_allow_html=True)
            df_aux = (df.loc[:, ['country', 'restaurant_id']].groupby('country')
                                                          .count()
                                                          .sort_values('restaurant_id',ascending=False)
                                                          .reset_index())
            fig=px.bar(df_aux, x='restaurant_id', y='country')
            st.plotly_chart(fig,use_container_width=True)
            # st.markdown("""---""")

    with st.container():
        st.markdown("<h3 style='text-align: center;'>Price range</h3>",unsafe_allow_html=True)
        df_aux = (df.loc[:, ['country', 'price_range']].groupby('country')
                                                      .value_counts()
                                                      .sort_values(ascending=False)
                                                      .reset_index())
        
        df_aux['percentage'] = df_aux.groupby('country')['count'].transform(lambda x: x / x.sum() * 100)
        df_aux = df_aux.sort_values(by=['percentage'], ascending=False)
        
        ordered_countries = df_aux[df_aux['price_range'] == 'gourmet']['country'].tolist()
        category_order = ['gourmet', 'expensive', 'normal', 'cheap']
        # color_mapping = {'cheap': 'cornflowerblue', 'normal': 'deepskyblue', 'expensive': 'dodgerblue', 'gourmet': 'mediumblue'}
        color_mapping = {'cheap': 'deepskyblue',    'normal': 'dodgerblue', 'expensive': 'mediumblue', 'gourmet': 'darkblue'}

        fig=px.histogram(df_aux, x='country', y='count', hover_data='price_range', color="price_range",
                                                     barnorm='percent',
                                                     category_orders={'price_range': category_order},
                                                     color_discrete_map=color_mapping)
        
        fig.update_xaxes(categoryorder='array', categoryarray=ordered_countries)
        st.plotly_chart(fig,use_container_width=True)
            
with tab2:
    print('a')







