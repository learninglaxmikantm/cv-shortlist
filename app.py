import streamlit as st

from auth.login import login

from ui_pages.dashboard import show_dashboard
from ui_pages.upload_jd import show_upload_jd
from ui_pages.upload_resume import show_upload_resume
from ui_pages.results import show_results

import os

os.makedirs("uploads", exist_ok=True)

# Session Initialization

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = None


# Login Check

if not st.session_state.logged_in:

    login()
    st.stop()


# Sidebar

menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Upload JD",
        "Upload Resumes",
        "Results"
    ]
)


# Logout

if st.sidebar.button("Logout"):

    st.session_state.logged_in = False
    st.session_state.username = None
    
    if "selected_job_id" not in st.session_state:
        st.session_state.selected_job_id = None

    if "selected_job_title" not in st.session_state:
        st.session_state.selected_job_title = None
    st.rerun()


# Routing

if menu == "Dashboard":

    show_dashboard()

elif menu == "Upload JD":

    show_upload_jd()

elif menu == "Upload Resumes":

    show_upload_resume()

elif menu == "Results":

    show_results()