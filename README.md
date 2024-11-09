AI Feedback - AI-Powered Essay Feedback
Overview
This app is a web-based application for providing automated feedback on student essays. The system uses AI to generate personalized teacher feedback and editorial suggestions, streamlining the essay review process while maintaining high educational standards.
Current Status
Version: 0.1.0-alpha
Environment: Ubuntu Server
Prerequisites

Python 3.8+
Virtual Environment
Ubuntu Server
Google Cloud Service Account
OpenAI API Key

Project Structure
CopyHuleEdu/
├── app/
│   ├── auth/          # Authentication blueprint
│   ├── essays/        # Essay processing blueprint
│   ├── main/          # Main routes blueprint
│   ├── models/        # Database models
│   ├── static/        # Static assets
│   ├── templates/     # Jinja2 templates
│   └── utils/         # Utility functions
├── instance/          # Instance-specific files
└── uploads/          # Uploaded files storage
Installation

Clone the repository:

bashCopygit clone [repository-url]
cd huleedu

Create and activate virtual environment:

bashCopypython -m venv venv
source venv/bin/activate  # On Ubuntu

Install dependencies:

bashCopypip install -r requirements.txt

Set up environment variables:
Create a .env file with:

CopyOPENAI_API_KEY=your_openai_key
GOOGLE_CLOUD_PRIVATE_KEY=your_google_cloud_key
INPUT_FOLDER_ID=your_input_folder_id
OUTPUT_FOLDER_ID=your_output_folder_id
Current Features

File upload and processing system
Google Drive integration for file management
OpenAI integration for essay feedback
Language correction using LanguageTool
Resource monitoring and logging
Basic error handling

Usage
Current CLI Usage
bashCopy# Start the monitoring service
python main.py
Server Deployment
Currently runs on Ubuntu server with venv instances for each feature.
Contributing

Fork the repository
Create your feature branch
Commit your changes
Push to the branch
Create a Pull Request

License
[License Type]
Contact
[Contact Information]
Acknowledgments

OpenAI for AI processing
Google Cloud Platform for file management
LanguageTool for text correction
