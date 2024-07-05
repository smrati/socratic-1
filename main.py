import os
import streamlit as st

from apps.feed_reader import fetch_feeds

st.set_page_config(layout="wide", page_title=os.path.basename(os.getcwd()))
page_list = []

page_list += ["Fetch Feeds"]


page = st.sidebar.selectbox("Select a page", page_list)

if page == "Fetch Feeds":
    fetch_feeds()


