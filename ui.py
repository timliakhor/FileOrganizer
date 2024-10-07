import streamlit as st
import os
from src.file_organizer.FileOrganizer import FileOrganizer

def main():
    st.title("File Organizer Tool")

    config_path = st.text_input("Config Path", value="config.json")
    path_to_folder = st.text_input("Path to Folder", value="./project")
    output_folder = st.text_input("Output Folder", value="./output")
    loc_limit = st.number_input("LOC Limit", min_value=1, value=3000, step=1)
    file_limit = st.number_input("File Limit", min_value=1, value=10, step=1)
    run_button = st.button("Run File Organizer")

    if run_button:
        if not os.path.exists(config_path):
            st.error("Config file does not exist.")
            return

        organizer = FileOrganizer(config_path, path_to_folder, output_folder, loc_limit, file_limit)
        organizer.organize_files()
        st.success("File organization complete!")

if __name__ == "__main__":
    main()