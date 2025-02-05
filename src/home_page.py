import streamlit as st

def home_page():
    st.title("Melbourne City")

    # Inject CSS to justify text on both ends
    st.markdown("""
    <style>
    .justified-text {
        text-align: justify;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    ## Introduction

    <div class="justified-text">
    This application provide useful information pertaining to the city of Melbourne!
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    ## Trees and Landscapes

    <div class="justified-text">
    The Trees and Landscape page provides information about the distribution and types of trees and landmarks in Melbourne.
    </div>
    """, unsafe_allow_html=True)

