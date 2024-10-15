from home_page import home_page
from dashbord_page import dashbord_page
import streamlit as st


st.sidebar.title("Melbourne City Information")
page = st.sidebar.selectbox("Select Page", ["Home", "Dashboardf"])

# Handle page navigation
if page == "Home":
    home_page()
elif page == "dashbord_page":
    dashbord_page()
