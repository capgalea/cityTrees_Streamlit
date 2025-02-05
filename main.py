from home_page import home_page
from dashbord_page import dashboard_page
import streamlit as st

# Set page configuration
st.set_page_config(layout="wide")

def main():
    st.sidebar.title("Melbourne City Information")
    page = st.sidebar.selectbox("Select Page", ["Home", "Dashboard"])

    # Handle page navigation
    if page == "Home":
        home_page()
    elif page == "Dashboard":
        dashboard_page()

if __name__ == "__main__":
    main()