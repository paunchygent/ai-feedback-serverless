# main.py
import sys
import json
import logging
import openai
import language_tool_python
import gc
from googleapiclient.discovery import build
from google.oauth2 import service_account

import os
import datetime
import monitoring
from dotenv import load_dotenv
import threading

# Load environment variables from .env file
load_dotenv()

# Importing utility functions from your modules
from utils import validate_secrets, get_secret, extract_student_info, capitalize_name
from drive_utils import download_file, upload_file
from docx_utils import read_docx_content, create_feedback_doc
from openai_utils import get_teacher_feedback, get_editor_revision
from feedback_generator import process_with_openai
from constants import ESSAY_INSTRUCTION, INPUT_FOLDER_ID, OUTPUT_FOLDER_ID

def initialize_services():
    try:
        credentials_json = get_secret('GOOGLE_CLOUD_PRIVATE_KEY')
        credentials_info = json.loads(credentials_json)
        credentials = service_account.Credentials.from_service_account_info(
            credentials_info,
            scopes=['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/documents']
        )
        service_drive = build('drive', 'v3', credentials=credentials)
        service_docs = build('docs', 'v1', credentials=credentials)
        return service_drive, service_docs
    except Exception as e:
        print(f"Error initializing Google Drive API: {e}")
        return None, None

def initialize_and_validate_services():
    if not validate_secrets():
        print("Failed to validate secrets. Exiting.")
        return None, None
    print("Secrets validated successfully.")
    return initialize_services()

def main():
    # Initialize OpenAI API key
    openai.api_key = get_secret('OPENAI_API_KEY')
    if not openai.api_key:
        print("OPENAI API Key is not set. Exiting.")
        return
    # Initialize the LanguageTool object
    try:
        tool = language_tool_python.LanguageTool('sv-SE')
    except Exception as e:
        print(f"Error initializing LanguageTool: {e}")
        tool = None

    try:
        print("\nStep 2: Initializing Google Drive and Docs API services")
        sys.stdout.flush()
        service_drive, service_docs = initialize_and_validate_services()

        if not service_drive or not service_docs:
            print("Service initialization failed. Exiting.")
            return

        results = service_drive.files().list(
            q=f"'{INPUT_FOLDER_ID}' in parents and trashed=false",
            fields="files(id, name)"
        ).execute()
        files = results.get('files', [])

        if not files:
            print("No files found in the input folder.")
            return

        for file in files:
            try:
                print(f"\nProcessing file: {file['name']}")

                # Process single file
                process_single_file(service_drive, file, tool)

            except Exception as e:
                print(f"  ERROR processing file {file['name']}: {str(e)}")
                continue

    except Exception as e:
        print(f"Error in main: {str(e)}")
        raise

def process_single_file(service_drive, file, tool):
    try:
        # Download and read file
        print("  Downloading and reading file...")
        file_io = download_file(service_drive, file['id'])
        essay_text = read_docx_content(file_io)
        print("  ✓ File downloaded and read successfully")

        # Extract student info
        print("  Extracting student information...")
        student_name, subject, student_email, class_name, essay_text = extract_student_info(
            file['name'],
            essay_text
        )

        if not student_name:
            raise ValueError("Failed to extract student information")
        print(f"  ✓ Student information extracted: {student_name}, {subject}, {class_name}, {student_email}")
        file_io = None

        # Apply LanguageTool corrections
        print("  Applying language corrections...")
        essay_text_corrected = spell_check_and_correct(essay_text, tool)
        print("  ✓ Language corrections applied")

        # Process with OpenAI pipeline
        processed_content = process_with_openai(
            student_name=student_name,
            essay_text=essay_text_corrected,
            essay_instruction=ESSAY_INSTRUCTION,
            client=openai.Client(api_key=openai.api_key)
        )

        print("  ✓ OpenAI processing completed")

        # Create and upload feedback document
        print("  Creating feedback document...")
        feedback_doc = create_feedback_doc(
            student_name,
            processed_content,
            essay_text
        )

        # Generate a filename that retains original, appends "_feedback" and a timestamp
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        original_filename = os.path.splitext(file['name'])[0]
        feedback_file_name = f"{original_filename}_feedback_{timestamp}.docx"
        print(f"  Uploading feedback document: {feedback_file_name}")
        upload_file(service_drive, OUTPUT_FOLDER_ID, feedback_doc, feedback_file_name)

        print(f"  ✓ Successfully processed and saved: {feedback_file_name}")
        feedback_doc = None

        gc.collect()

    except Exception as e:
        print(f"\n  ERROR processing file: {str(e)}")
        raise


def spell_check_and_correct(text: str, tool) -> str:
    try:
        if tool is None:
            print("LanguageTool object is not initialized.")
            return text  # Return original text if tool is not available
        matches = tool.check(text)
        corrected_text = language_tool_python.utils.correct(text, matches)
        return corrected_text
    except Exception as e:
        print(f"Error during spell check and correction: {e}")
        return text  # Return original text if correction fails

def start_monitoring():
    monitoring_thread = threading.Thread(target=monitoring.log_resource_usage, daemon=True)
    monitoring_thread.start()

if __name__ == "__main__":
    # Start monitoring resources in a separate background thread
    start_monitoring()
    
    # Run the main function for processing files
    main()