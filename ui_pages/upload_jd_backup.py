import streamlit as st
from database.mongodb import jobs_collection
from datetime import datetime
import pandas as pd


def show_upload_jd():

    st.title("Upload Job Description")

    job_title = st.text_input(
        "Job Title"
    )

    experience = st.number_input(
        "Experience Required (Years)",
        min_value=0,
        max_value=30,
        value=0
    )

    skills = st.text_area(
        "Required Skills (Comma Separated)"
    )

    jd_text = st.text_area(
        "Job Description",
        height=250
    )

    if st.button("Save Job Description"):

        if not job_title:

            st.error(
                "Job Title is required"
            )

            return

        document = {

            "job_title": job_title,

            "experience": experience,

            "skills": skills,

            "job_description": jd_text,

            "created_by":
                st.session_state.username,

            "created_on":
                datetime.utcnow()
        }

        jobs_collection.insert_one(
            document
        )

        st.success(
            "Job Description Saved Successfully"
        )

st.divider()

st.subheader("Available Job Descriptions")

jobs = list(
    jobs_collection.find(
        {},
        {
            "_id": 0,
            "job_title": 1,
            "experience": 1,
            "skills": 1,
            "created_by": 1
        }
    )
)

if jobs:

    df = pd.DataFrame(jobs)

    st.dataframe(
        df,
        use_container_width=True
    )

else:

    st.info(
        "No Job Descriptions Available"
    )