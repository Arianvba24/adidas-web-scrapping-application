import streamlit as st
from spider import *
from downloader import FileDownloader
import streamlit.components as select_slider
import pandas
import base64
import time
import asyncio
from io import BytesIO
import os
import nest_asyncio

nest_asyncio.apply()
os.system("playwright install")


timestr = time.strftime("%Y%m%d-%H%M%S")

@st.cache_data
def scrapping_data(url):
    spider = Async_spider_functions()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    df = loop.run_until_complete(spider.open_browser(url))
    return df


st.set_page_config(layout="wide")
def main():
    values = ["Scrapping","About"]
    st.sidebar.selectbox("Valores",values)
    st.title("Web scrapping DIA marketplace")
    with st.form(key="scrapping"):
        st.markdown("**Click the button to scrape :)**")
       
        value = st.form_submit_button("Submit request")
    if value:
        
        df = scrapping_data(url=r"https://www.adidas.es/zapatillas-hombre")
        st.dataframe(df)
        tab1,tab2,tab3 = st.tabs(["CSV","Excel","JSON"])

        with tab1:
            download = FileDownloader(df.to_csv(), file_ext=".csv").download()

        with tab2:
            towrite = BytesIO()
            df.to_excel(towrite, index=False, engine='openpyxl')
            towrite.seek(0)
            download = FileDownloader(towrite.read(), file_ext="xlsx").download_xlsx()

        with tab3:
            json_data = df.to_json(orient='records')
            download = FileDownloader(json_data, file_ext="json").download_json()


    
    
                



if __name__=="__main__":
    main()
