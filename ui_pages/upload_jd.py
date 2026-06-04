import streamlit as st
from database.mongodb import jobs_collection
from datetime import datetime
import pandas as pd

print(
    jobs_collection.count_documents({})
)

def show_upload_jd():

    st.title("Upload Job Description")

    job_title = st.text_input("Job Title")

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
            st.error("Job Title is required")
            return

        jobs_collection.insert_one(
            {
                "job_title": job_title,
                "experience": experience,
                "skills": skills,
                "job_description": jd_text,
                "created_by": st.session_state.username,
                "created_on": datetime.utcnow()
            }
        )

        st.success(
            "Job Description Saved Successfully"
        )

        st.rerun()

    # ======================
    # Existing JD List
    # ======================

    st.divider()
    st.subheader("Available Job Descriptions")

    jobs = list(
        jobs_collection.find({})
    )

    if jobs:

        df = pd.DataFrame(jobs)

        if "_id" in df.columns:
            df = df.drop(columns=["_id"])

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            # ======================
            # Delete JD Section
            # ======================

            st.divider()

            st.subheader(
                "Delete Job Description"
            )

            job_map = {
                f"{job['job_title']} ({job.get('experience',0)} yrs)": job["_id"]
                for job in jobs
            }

            selected_job = st.selectbox(
                "Select Job",
                list(job_map.keys())
            )

            if st.button(
                "Delete Selected JD"
            ):

                jobs_collection.delete_one(
                    {
                        "_id": job_map[selected_job]
                    }
                )

                st.success(
                    "Job Description Deleted"
                )

                st.rerun()

        else:

            st.info(
                "No Job Descriptions Available"
            )