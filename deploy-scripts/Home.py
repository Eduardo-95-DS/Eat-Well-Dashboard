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
            Dashboard built to accompany the company's main metrics

            ### Ask for help
                - https://www.linkedin.com/in/eduardo-rodrigues-ds/
            """)
