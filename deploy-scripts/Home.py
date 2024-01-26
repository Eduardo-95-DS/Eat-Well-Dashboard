import streamlit as st
from PIL import Image

st.set_page_config(page_title='Home',
                  page_icon='📊')

# image_path=''
# image=Image.open(image_path+'logo.jpg')
image=Image.open('image/logo.jpg') # deploy version
# image=Image.open('logo.jpg')
st.sidebar.image(image,width=180)

st.sidebar.markdown('# Eat Well Company')
# st.sidebar.markdown('## Fastest Delivery In Town')
st.sidebar.markdown("""---""")

st.write('# Eat Well Company Dashboard')

st.markdown("""
            Growth Dashboard foi construído para acompanhar as métricas de crescimento dos entregadores e dos restaurantes.
            ### Como utilizá-lo?
            - Visão Empresa: 
                - Visão Gerencial: Métricas gerais de comportamento
                - Visão Tática: Indicadores semanais de crescimento
                - Visao Geográfica: Insights de geolocalização
            - Visão Entregador:
                - Acompanhamento dos indicadores semanais de crescimento 
            - Visão Restaurante:
                - Indicadores semanais de crescimento dos restaurantes
            ### Ask for help
                - https://www.linkedin.com/in/eduardo-rodrigues-ds/
            """)
