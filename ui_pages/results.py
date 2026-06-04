import streamlit as st
import pandas as pd

from database.mongodb import (
    jobs_collection,
    candidates_collection
)


def show_results():

    st.title(
        "Resume Shortlisting Results"
    )

    jobs = list(
        jobs_collection.find({})
    )

    if not jobs:

        st.warning(
            "No Job Descriptions Available"
        )

        return

    job_map = {
        job["job_title"]: job
        for job in jobs
    }

    selected_job = st.selectbox(
        "Select Job Description",
        list(job_map.keys())
    )

    if st.button(
        "Match Candidates"
    ):

        job = job_map[
            selected_job
        ]

        jd_skills = [
            skill.strip().lower()
            for skill in job.get(
                "skills",
                ""
            ).split(",")
            if skill.strip()
        ]

        candidates = list(
            candidates_collection.find({})
        )

        if not candidates:

            st.warning(
                "No Candidates Available"
            )

            return

        results = []

        for candidate in candidates:

            resume_text = candidate.get(
                "resume_text",
                ""
            ).lower()

            matched_skills = []

            missing_skills = []

            for skill in jd_skills:

                if skill in resume_text:

                    matched_skills.append(
                        skill
                    )

                else:

                    missing_skills.append(
                        skill
                    )

            if len(jd_skills) > 0:

                score = int(
                    (
                        len(
                            matched_skills
                        )
                        /
                        len(
                            jd_skills
                        )
                    ) * 100
                )

            else:

                score = 0

            if score >= 70:

                status = "Shortlisted"

            elif score >= 50:

                status = "Review"

            else:

                status = "Rejected"

            reason = (
                ", ".join(
                    missing_skills
                )
                if missing_skills
                else "Good Match"
            )

            results.append(
                {
                    "Candidate":
                        candidate.get(
                            "candidate_name",
                            ""
                        ),

                    "Email":
                        candidate.get(
                            "email",
                            ""
                        ),

                    "Phone":
                        candidate.get(
                            "phone",
                            ""
                        ),

                    "Match %":
                        score,

                    "Status":
                        status,

                    "Matched Skills":
                        ", ".join(
                            matched_skills
                        ),

                    "Missing Skills":
                        reason
                }
            )

        df = pd.DataFrame(
            results
        )

        df = df.sort_values(
            by="Match %",
            ascending=False
        )

        st.subheader(
            "Candidate Ranking"
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        csv = df.to_csv(
            index=False
        )

        st.download_button(
            label="Download Results CSV",
            data=csv,
            file_name="candidate_shortlisting_results.csv",
            mime="text/csv"
        )