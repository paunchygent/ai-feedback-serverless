# utils.py

import os
import re

import os
from dotenv import load_dotenv

def get_secret(secret_name: str) -> str:
    """
    Retrieve a secret from environment variables.

    Args:
    secret_name (str): The name of the secret to retrieve.

    Returns:
    str: The secret value.

    Raises:
    ValueError: If the secret is not found.
    """
    value = os.getenv(secret_name)
    if value is not None:
        return value

    raise ValueError(f"Secret {secret_name} not found in environment variables")

def validate_secrets() -> bool:
    required_secrets = ['OPENAI_API_KEY', 'GOOGLE_CLOUD_PRIVATE_KEY']
    for secret in required_secrets:
        try:
            get_secret(secret)
        except ValueError:
            print(f"Secret {secret} not found.")
            return False
    return True

def capitalize_name(name):
    return ' '.join(word.capitalize() for word in name.split())

def extract_student_info(filename: str, content: str):
    print(f"\nProcessing filename: {filename}")
    filename = os.path.splitext(filename)[0]

    lines = content.split('\n')

    # Primary Attempt: Extracting from the first four lines of the document
    student_name = lines[0].strip() if len(lines) > 0 else None
    subject = lines[1].strip() if len(lines) > 1 else None
    student_email = lines[2].strip() if len(lines) > 2 else None
    class_name = lines[3].strip() if len(lines) > 3 else None

    # Capitalize the student name if it was found
    if student_name:
        student_name = capitalize_name(student_name)

    # Clean up class name to remove "Klass:" if it appears
    if class_name and class_name.lower().startswith("klass:"):
        class_name = class_name.split(":", 1)[-1].strip()

    # Fallback 1: Use filename if any information is missing
    if not student_name or not subject or not class_name:
        print("  WARNING: Missing information in the first four lines. Attempting fallback extraction from filename...")

        # Regex pattern to match the filename format "First Last (Subject Class)"
        filename_pattern = r"^(.*?)\s*\((.*?)\s*(SA|NA)\d+[A-Z]\)$"
        match = re.match(filename_pattern, filename)

        if match:
            if not student_name:
                student_name = capitalize_name(match.group(1).strip())
            if not subject:
                subject = match.group(2).strip()
            if not class_name:
                class_name = match.group(3).strip()

    # Fallback 2: Default values if still not found
    if not student_name:
        student_name = "Unknown Student"
        print("  WARNING: Student name not found. Using default value.")
    
    if not subject:
        subject = "Unknown Subject"
        print("  WARNING: Subject not found. Using default value.")
    
    if not student_email:
        student_email = "Unknown Email"
        print("  WARNING: Student email not found. Using default value.")
    
    if not class_name:
        class_name = "Unknown Class"
        print("  WARNING: Class name not found. Using default value.")

    print(f"Extracted info from content - Name: {student_name}, Subject: {subject}, Email: {student_email}, Class: {class_name}")
    return student_name, subject, student_email, class_name, content
