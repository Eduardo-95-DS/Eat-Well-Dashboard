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

df_raw['cuisines']=df_raw['cuisines'].replace(' ','', regex=True)

df=df_raw.copy()
df3=df_raw.copy()
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

rows1=df['price_range'].isin(price)
rows2=df3['price_range'].isin(price)

df=df.loc[rows1,:]
df3=df3.loc[rows2,:]

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

# rows=df['has_table_booking'].isin(booking)
# df=df.loc[rows,:]

if not booking:
    rows1 = ~df['has_table_booking'].isna()
    rows2 = ~df3['has_table_booking'].isna()

else:
    rows1 = df['has_table_booking'].isin(booking)
    rows2 = df3['has_table_booking'].isin(booking)

df = df.loc[rows1, :]
df3 = df3.loc[rows2, :]

# filtro de online delivery
st.sidebar.markdown("""
    <div style="margin-bottom: -70px;">
        <span style="font-size:20px; font-weight:bold;">Online delivery</span>
    </div>
""", unsafe_allow_html=True)

online= st.sidebar.multiselect('',['Yes','No'],
                               default=['Yes','No'],key='online')

# rows=df['has_online_delivery'].isin(online)
# df=df.loc[rows,:]

if not online:
    rows1 = ~df['has_online_delivery'].isna()
    rows2 = ~df3['has_online_delivery'].isna()

else:
    rows1 = df['has_online_delivery'].isin(online)
    rows2 = df3['has_online_delivery'].isin(online)

df = df.loc[rows1, :]
df3 = df3.loc[rows2, :]


# filtro de delivering now
st.sidebar.markdown("""
    <div style="margin-bottom: -70px;">
        <span style="font-size:20px; font-weight:bold;">Delivering now</span>
    </div>
""", unsafe_allow_html=True)

delivery= st.sidebar.multiselect('',['Yes','No'],
                               default=['Yes','No'],key='delivery')

# rows=df['is_delivering_now'].isin(delivery)
# df=df.loc[rows,:]

if not delivery:
    rows1 = ~df['is_delivering_now'].isna()
    rows2 = ~df3['is_delivering_now'].isna()

else:
    rows1 = df['is_delivering_now'].isin(delivery)
    rows2 = df3['is_delivering_now'].isin(delivery)

df = df.loc[rows1, :]
df3 = df.loc[rows2, :]

# filtro de culinaria
st.sidebar.markdown("""
    <div style="margin-bottom: -70px;">
        <span style="font-size:20px; font-weight:bold;">Cuisine</span>
    </div>
""", unsafe_allow_html=True)

df2=df.assign(cuisine=df['cuisines'].str.split(',')).explode('cuisine')
df2['cuisine']=df2['cuisine'].replace(' ','', regex=True)
df2['count'] = df2.groupby('cuisine')['cuisine'].transform('count')
df2=df2.sort_values('count',ascending=False)
cuisine=df2['cuisine'].unique()
cuisine=np.insert(cuisine, 0, 'All')
cuisines = st.sidebar.selectbox('cuisine', cuisine, label_visibility="hidden")
cuisine1=cuisines
cuisines = [cuisines]

if 'All' in cuisines:
    df = df
else:
    mascara = df['cuisines'].str.contains('|'.join(cuisines), case=True)
    linhas_desejadas = df[mascara]
    df=linhas_desejadas
    
# filtro de reset
# # Defina a função para criar um objeto de estado da sessão
# class SessionState:
#     def __init__(self, **kwargs):
#         self.__dict__.update(kwargs)

# # Inicialize o objeto de estado da sessão
# session_state = SessionState(price_reset=False, booking_reset=False, online_reset=False, delivery_reset=False, cuisine_reset=False)

reset_button = st.sidebar.button("Reset Visualizations")

if reset_button:
    df = df_raw.copy()
    # session_state.price_reset = False
    # session_state.booking_reset = False
    # session_state.online_reset = False
    # session_state.delivery_reset = False
    # session_state.cuisine_reset = False
else:
    print('')

# plots===================================================================================
# with tab1:

if 'All' in cuisines:

    with st.container():
    
        col1,col2=st.columns(2)
        with col1:
            st.markdown("<h3 style='text-align: center;'>N° of restaurants</h3>",unsafe_allow_html=True)
    
            df_aux=df.drop_duplicates(subset=['restaurant_id'])
            df_aux = (df.loc[:, ['country', 'restaurant_id']].groupby('country')
                                                          .count()
                                                          .sort_values('restaurant_id',ascending=False)
                                                          .reset_index())
            
            fig=px.bar(df_aux, x='restaurant_id', y='country', category_orders={'country': df_aux['country'].tolist()})
            
            fig.update_layout(xaxis=dict(title='Count',title_font=dict(size=20)), yaxis=dict(title=''),xaxis_tickfont=dict(size=15), 
                              yaxis_tickfont=dict(size=15),height=500,margin=dict(t=0))
            
            st.plotly_chart(fig,use_container_width=True)
                
        with col2:
            # if 'All' in cuisines:
            st.markdown("<h3 style='text-align: center;'>Unique cuisines</h3>",unsafe_allow_html=True)
            # else:
                # st.markdown("<h3 style='text-align: center;'>Cuisine total</h3>",unsafe_allow_html=True)
    
            df2=df[['cuisines','country']]
            df2=df2.assign(all=df2['cuisines'].str.split(',')).explode('all')
            df2['all']= df2['all'].replace(' ','', regex=True)
            df2=df2.drop(columns=['cuisines'])
            df2=df2[['country','all']]
            df2=df2.drop_duplicates(ignore_index=True)
            df2 = (df2.loc[:, ['country', 'all']].groupby('country')
                                                        .count()
                                                        .sort_values('all',ascending=False)
                                                        .reset_index())
            
            fig=px.bar(df2, x='all', y='country',category_orders={'country': df2['country'].tolist()})
            
            fig.update_layout(xaxis=dict(title='Count',title_font=dict(size=20)), yaxis=dict(title=''),xaxis_tickfont=dict(size=15), 
                              yaxis_tickfont=dict(size=15),height=500,margin=dict(t=0))
            
            st.plotly_chart(fig,use_container_width=True)

elif reset_button:

    with st.container():
    
        col1,col2=st.columns(2)
        with col1:
            st.markdown("<h3 style='text-align: center;'>N° of restaurants</h3>",unsafe_allow_html=True)
    
            df_aux=df.drop_duplicates(subset=['restaurant_id'])
            df_aux = (df.loc[:, ['country', 'restaurant_id']].groupby('country')
                                                          .count()
                                                          .sort_values('restaurant_id',ascending=False)
                                                          .reset_index())
            
            fig=px.bar(df_aux, x='restaurant_id', y='country', category_orders={'country': df_aux['country'].tolist()})
            
            fig.update_layout(xaxis=dict(title='Count',title_font=dict(size=20)), yaxis=dict(title=''),xaxis_tickfont=dict(size=15), 
                              yaxis_tickfont=dict(size=15),height=500,margin=dict(t=0))
            
            st.plotly_chart(fig,use_container_width=True)
                
        with col2:
            # if 'All' in cuisines:
            st.markdown("<h3 style='text-align: center;'>Unique cuisines</h3>",unsafe_allow_html=True)
            # else:
                # st.markdown("<h3 style='text-align: center;'>Cuisine total</h3>",unsafe_allow_html=True)
    
            df2=df[['cuisines','country']]
            df2=df2.assign(all=df2['cuisines'].str.split(',')).explode('all')
            df2['all']=df2['all'].replace(' ','', regex=True)
            df2=df2.drop(columns=['cuisines'])
            df2=df2[['country','all']]
            df2=df2.drop_duplicates(ignore_index=True)
            df2 = (df2.loc[:, ['country', 'all']].groupby('country')
                                                        .count()
                                                        .sort_values('all',ascending=False)
                                                        .reset_index())
            
            fig=px.bar(df2, x='all', y='country',category_orders={'country': df2['country'].tolist()})
            
            fig.update_layout(xaxis=dict(title='Count',title_font=dict(size=20)), yaxis=dict(title=''),xaxis_tickfont=dict(size=15), 
                              yaxis_tickfont=dict(size=15),height=500,margin=dict(t=0))
            
            st.plotly_chart(fig,use_container_width=True)
else:

    with st.container():
        # col1,col2=st.columns(2)
        # with col1:
        st.markdown("<h3 style='text-align: center;'>N° of restaurants</h3>",unsafe_allow_html=True)
    
        df_aux=df.drop_duplicates(subset=['restaurant_id'])
        df_aux = (df.loc[:, ['country', 'restaurant_id']].groupby('country')
                                                      .count()
                                                      .sort_values('restaurant_id',ascending=False)
                                                      .reset_index())
        
        fig=px.bar(df_aux, x='restaurant_id', y='country', category_orders={'country': df_aux['country'].tolist()})
        
        fig.update_layout(xaxis=dict(title='Count',title_font=dict(size=20)), yaxis=dict(title=''),xaxis_tickfont=dict(size=15), 
                          yaxis_tickfont=dict(size=15),height=500,margin=dict(t=0))
        
        st.plotly_chart(fig,use_container_width=True)

        # with col2:
        #     # if 'All' in cuisines:
        #     st.markdown("<h3 style='text-align: center;'>Unique cuisines</h3>",unsafe_allow_html=True)
        #     # else:
        #         # st.markdown("<h3 style='text-align: center;'>Cuisine total</h3>",unsafe_allow_html=True)
    
        #     df2=df[['cuisines','country']]
        #     df2=df2.assign(all=df2['cuisines'].str.split(',')).explode('all')
        #     df2['all']= df2['all'].replace(' ','', regex=True)
        #     df2=df2.drop(columns=['cuisines'])
        #     df2=df2[['country','all']]
        #     df2=df2.drop_duplicates(ignore_index=True)
        #     df2 = (df2.loc[:, ['country', 'all']].groupby('country')
        #                                                 .count()
        #                                                 .sort_values('all',ascending=False)
        #                                                 .reset_index())
            
        #     fig=px.bar(df2, x='all', y='country',category_orders={'country': df2['country'].tolist()})
            
        #     fig.update_layout(xaxis=dict(title='Count',title_font=dict(size=20)), yaxis=dict(title=''),xaxis_tickfont=dict(size=15), 
        #                       yaxis_tickfont=dict(size=15),height=500,margin=dict(t=0))
            
        #     st.plotly_chart(fig,use_container_width=True)


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
        
        fig.update_layout(xaxis=dict(title='0-5',title_font=dict(size=20)), yaxis=dict(title=''),xaxis_tickfont=dict(size=15), 
                          yaxis_tickfont=dict(size=15),height=500,margin=dict(t=0))
        
        st.plotly_chart(fig,use_container_width=True)
            
    with col2:
        st.markdown("<h3 style='text-align: center;'>Average cost for two</h3>",unsafe_allow_html=True)
        df_aux=df.drop_duplicates(subset=['restaurant_id'])
        df_aux = (df_aux.loc[:, ['country', 'average_cost_for_two']].groupby('country')
                                                                .mean()
                                                                .sort_values('average_cost_for_two',ascending=False)
                                                                .reset_index()) 
        
        fig=px.bar(df_aux, x='average_cost_for_two', y='country',category_orders={'country': df_aux['country'].tolist()})
        
        fig.update_layout(xaxis=dict(title='Price in dollars ($)',title_font=dict(size=20)), yaxis=dict(title=''),xaxis_tickfont=dict(size=15), 
                          yaxis_tickfont=dict(size=15),height=500,margin=dict(t=0))
        
        st.plotly_chart(fig,use_container_width=True)

with st.container():

    col1,col2=st.columns(2)
    with col1:
        
        st.markdown("<h3 style='text-align: center;'>Price range</h3>",unsafe_allow_html=True)

        if 'All' in cuisines:

            # df_aux=df.drop_duplicates(subset=['restaurant_id'])
            df_aux = (df.loc[:, ['country', 'price_range']].groupby('country')
                                                          .value_counts()
                                                          .sort_values(ascending=False)
                                                          .reset_index())
            
            df_aux['percentage'] = df_aux.groupby('country')['count'].transform(lambda x: x / x.sum() * 100)
            df_aux = df_aux.sort_values(by=['percentage'], ascending=False)
            
            # ordered_countries = df_aux[df_aux['price_range'] == 'gourmet']['country'].tolist()
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

        else:

            df_aux = (df.loc[:, ['country', 'price_range']].groupby('country')
                                              .value_counts()
                                              .sort_values(ascending=False)
                                              .reset_index())
            
            df_aux['percentage'] = df_aux.groupby('country')['count'].transform(lambda x: x / x.sum() * 100)
            df_aux = df_aux.sort_values(by=['percentage','price_range'], ascending=False)
            
            df_sorted_gourmet = df_aux[df_aux['price_range'] == 'gourmet'].sort_values(by='percentage', ascending=False)
            df_sorted_other = df_aux[df_aux['price_range'] != 'gourmet']
            df_sorted = pd.concat([df_sorted_gourmet, df_sorted_other])
            
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
            
    with col2:

        st.markdown("<h3 style='text-align: center;'>Proportion</h3>",unsafe_allow_html=True)

        if 'All' in cuisines:
        
            # df2=df.copy()
            df2=df.assign(cuisine=df['cuisines'].str.split(',')).explode('cuisine')
            df2=df2.drop_duplicates(ignore_index=True)
            
            df3=df2[['country','cuisine']].groupby('country').value_counts().reset_index()
            # df3=df3.loc[df3.groupby('country')['count'].idxmax()].sort_values('count',ascending=False)
            
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

        elif reset_button:

            # df2=df.copy()
            df2=df.assign(cuisine=df['cuisines'].str.split(',')).explode('cuisine')
            df2=df2.drop_duplicates(ignore_index=True)
            
            df3=df2[['country','cuisine']].groupby('country').value_counts().reset_index()
            # df3=df3.loc[df3.groupby('country')['count'].idxmax()].sort_values('count',ascending=False)
            
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
            
        else:
            
            df2=df3.assign(cuisine=df3['cuisines'].str.split(',')).explode('cuisine')
            df2=df2.drop_duplicates(ignore_index=True)
            
            df3=df2[['country','cuisine']].groupby('country').value_counts().reset_index()
            df3['sum'] = df3.groupby('country')['count'].transform('sum')
            df3=df3[df3['cuisine']==cuisine1]
            df3['percentage'] = df3.apply(lambda row: (row['count'] *100) / row['sum'], axis=1)
            df3=df3.sort_values('percentage',ascending=False)
            
            fig = px.bar(df3, x='percentage', y='country',category_orders={'country': df3['country'].tolist()},
                         labels={'percentage': 'Percentage (%)', 'country': 'Country'},
                         height=600)
            
            # Personalizar layout
            fig.update_layout(xaxis=dict(title='Percentage (%)',title_font=dict(size=20)),yaxis=dict(title=''),xaxis_tickfont=dict(size=15), 
                                  yaxis_tickfont=dict(size=15),height=500,margin=dict(t=0),showlegend=False)
        
            st.plotly_chart(fig,use_container_width=True)






