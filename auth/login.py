import streamlit as st
from auth.auth_service import authenticate_user

def login():

    st.title("Resume Shortlisting System")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        user = authenticate_user(
            username,
            password
        )

        if user:

            st.session_state.logged_in = True
            st.session_state.username = username

            st.rerun()

        else:

            st.error(
                "Invalid Credentials"
            )
    
