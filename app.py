import os
import glob
import time
import streamlit as st
from crew import YoutubeAnalysisCrew
from agents import LLMChoice


GITHUB_LINK = "https://github.com/emirhansilsupur/youtube-video-analyzer.git"
LINKEDIN_LINK = "https://www.linkedin.com/in/emirhansilsupur/"


def main():
    st.set_page_config(page_title="YouTube Video Inspector", page_icon=":red_circle:")
    st.title(
        ":clipboard: YouTube Video Inspector",
    )
    st.write(
        """This app is a quick and easy tool for analyzing YouTube videos. 
        Enter a video link to get detailed stats, analyze comments, and generate PDF reports."""
    )
    st.divider()

    # Initialize session state variables if they don't exist
    if "result" not in st.session_state:
        st.session_state.result = None
    if "pdf_path" not in st.session_state:
        st.session_state.pdf_path = None
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = None
    if "pdf_generation_time" not in st.session_state:
        st.session_state.pdf_generation_time = None
    if "error_message" not in st.session_state:
        st.session_state.error_message = None

    # User input for YouTube URL
    video_url = st.text_input("Enter YouTube Video URL:")

    if video_url:
        st.video(video_url)

    # LLM model choice
    llm_choice_name = st.selectbox(
        "Choose LLM:", [choice.value for choice in LLMChoice]
    )
    llm_choice = next(choice for choice in LLMChoice if choice.value == llm_choice_name)

    if st.button("Analyze Video"):
        if video_url:
            try:
                with st.spinner("Analyzing video... This may take a few minutes."):

                    start_time = time.time()

                    youtube_analysis_crew = YoutubeAnalysisCrew(video_url, llm_choice)

                    st.session_state.result = youtube_analysis_crew.run()
                    st.session_state.selected_model = llm_choice

                    # Get the most recent PDF file from the 'output' directory
                    list_of_files = glob.glob(
                        "output/*.pdf"
                    )  # Find all .pdf files in the output directory
                    if list_of_files:
                        latest_file = max(list_of_files, key=os.path.getctime)
                        st.session_state.pdf_path = latest_file
                    else:
                        st.session_state.pdf_path = None

                    # Calculate the time taken for the PDF generation
                    st.session_state.pdf_generation_time = time.time() - start_time

                st.success("Analysis complete!")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter a valid YouTube URL.")

    # Display the result if it exists in session state
    st.divider()
    if st.session_state.result:
        st.markdown(st.session_state.result)
        st.divider()
        # Show the time taken to generate the PDF
        if st.session_state.pdf_generation_time is not None:
            st.info(
                f"PDF report generated in {st.session_state.pdf_generation_time:.2f} seconds.",
            )
            st.warning("If the report is missing, try a different LLM.")

        # Offer PDF download
        if st.session_state.pdf_path:
            with open(st.session_state.pdf_path, "rb") as pdf_file:
                pdf_bytes = pdf_file.read()
                st.download_button(
                    label="Download PDF Report",
                    data=pdf_bytes,
                    file_name="Youtube_Video_Analysis_Report.pdf",
                    mime="application/pdf",
                )
    # Retry Option if there was an error
    if st.session_state.error_message:
        if st.button("Retry"):
            # Clear session state to reset the app
            st.session_state.result = None
            st.session_state.pdf_path = None
            st.session_state.selected_model = None
            st.session_state.pdf_generation_time = None
            st.session_state.error_message = None
            st.experimental_rerun()

    st.markdown(
        f"""
        <div style="display: flex; justify-content: flex-end;">
            <a href="{GITHUB_LINK}" target="_blank" style="text-decoration: none;">
                <img src="https://img.icons8.com/ios-glyphs/30/000000/github.png"/>
            </a>
            <a href="{LINKEDIN_LINK}" target="_blank" style="text-decoration: none; margin-left: 15px;">
                <img src="https://img.icons8.com/ios-glyphs/30/000000/linkedin.png"/>
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
