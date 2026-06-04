import streamlit as st
import os
import hashlib
import pandas as pd

from utils.resume_parser import (
    extract_pdf_text,
    extract_docx_text
)
from utils.candidate_extractor import (
    extract_name,
    extract_email,
    extract_phone
)
from database.mongodb import (
    candidates_collection
)

UPLOAD_FOLDER = "uploads"


def show_upload_resume():

    st.title("Upload Resumes")

    uploaded_files = st.file_uploader(
        "Upload PDF or DOCX Resumes",
        type=["pdf", "docx"],
        accept_multiple_files=True
    )

    if st.button("Upload"):

        if not uploaded_files:

            st.warning(
                "Please select files"
            )

            return

        for file in uploaded_files:

            file_bytes = file.getvalue()

            file_hash = hashlib.md5(
                file_bytes
            ).hexdigest()

            existing = candidates_collection.find_one(
                {
                    "file_hash": file_hash
                }
            )

            if existing:

                st.error(
                    f"{file.name} already exists"
                )

                continue

            save_path = os.path.join(
                UPLOAD_FOLDER,
                file.name
            )

            with open(
                save_path,
                "wb"
            ) as f:

                f.write(file_bytes)

            resume_text = ""

            if file.name.lower().endswith(".pdf"):

                resume_text = extract_pdf_text(
                    save_path
                )

            elif file.name.lower().endswith(".docx"):

                resume_text = extract_docx_text(
                    save_path
                )

            st.subheader(
                "Extracted Resume Text"
            )

            st.text_area(
                "Resume Content",
                resume_text[:3000],
                height=300
            )

            candidate_name = extract_name(
                resume_text
            )

            email = extract_email(
                resume_text
            )

            phone = extract_phone(
                resume_text
            )
            st.write(
                "Extracted Name:",
                candidate_name
            )

            st.write(
                "Extracted Email:",
                email
            )

            st.write(
                "Extracted Phone:",
                phone
            )
            candidates_collection.insert_one(
                {
                    "candidate_name": candidate_name,
                    "email": email,
                    "phone": phone,
                    "file_name": file.name,
                    "file_hash": file_hash,
                    "file_path": save_path,
                    "resume_text": resume_text,
                    "uploaded_by": st.session_state.username
                }
            )

            st.write(f"Name : {candidate_name}")
            st.write(f"Email : {email}")
            st.write(f"Phone : {phone}")

            st.success(
                f"{file.name} uploaded successfully"
            )

    st.divider()

    st.subheader(
        "Uploaded Resumes"
    )

    resumes = list(
        candidates_collection.find({})
    )

    if resumes:
        data = []
        for resume in resumes:

            data.append(
                {
                    "Candidate Name":
                        resume.get("candidate_name",""),

                    "Email":
                        resume.get("email",""),

                    "Phone":
                        resume.get("phone",""),

                    "File Name":
                        resume.get("file_name","")
                }
            )

        df = pd.DataFrame(data)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        st.subheader(
            "Delete Resume"
        )

        resume_map = {
            f"{r.get('candidate_name','')} - {r.get('file_name','')}":
            r["_id"]

            for r in resumes
        }

        selected_resume = st.selectbox(
            "Select Resume",
            list(resume_map.keys())
        )

        if st.button(
            "Delete Resume"
        ):

            candidate = candidates_collection.find_one(
                {
                    "_id":
                    resume_map[selected_resume]
                }
            )

            if candidate:

                file_path = candidate.get(
                    "file_path"
                )

                if file_path and os.path.exists(file_path):

                    os.remove(file_path)

                candidates_collection.delete_one(
                    {
                        "_id":
                        candidate["_id"]
                    }
                )

                st.success(
                    "Resume Deleted Successfully"
                )

                st.rerun()

    else:

        st.info(
            "No Resumes Uploaded"
        )