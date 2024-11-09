import os
from pathlib import Path
from datetime import datetime

# Set your project directory path
project_path = Path("/home/paunchygent/projects/ai_feedback_svenska")

# Remote output folder
remote_output_folder = Path("/home/paunchygent/projects/ai_feedback_svenska/ai_context")

# Create remote output folder if it doesn't exist
os.makedirs(remote_output_folder, exist_ok=True)

# Generate filename with timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"ai_feedback_svenska_code_base_{timestamp}.txt"

# Full path for output file
output_file = remote_output_folder / filename

# Define folders and files to exclude
excluded_folders = {"__pycache__", "venv", "instance", "migrations", "tests", "combine_all_app_files"}
excluded_files = {"Readme", "Roadmap"}
allowed_extensions = {".py", ".html", ".css", ".js"}

# Open the output file for writing
with open(output_file, "w", encoding="utf-8") as outfile:
    # Write a header with basic info
    outfile.write("# Combined Project Files\n")
    outfile.write("# This file contains all relevant source code from the project\n\n")
    
    # Traverse the directory tree
    for root, dirs, files in os.walk(project_path):
        # Skip excluded folders
        dirs[:] = [d for d in dirs if d not in excluded_folders]
        
        # Sort files for consistent output
        files.sort()
        
        for file_name in files:
            # Filter files based on extension and exclude specific files
            if any(file_name.endswith(ext) for ext in allowed_extensions) and file_name not in excluded_files:
                file_path = Path(root) / file_name
                rel_path = file_path.relative_to(project_path)
                
                # Add progress indicator
                print(f"Processing: {rel_path}")
                
                # Add file header with clear separation and relative path
                outfile.write(f"\n{'='*80}\n")
                outfile.write(f"# File: {rel_path}\n")
                outfile.write(f"{'='*80}\n\n")
                
                # Read and write the content of each file
                try:
                    with open(file_path, "r", encoding="utf-8") as infile:
                        outfile.write(infile.read())
                        outfile.write("\n")  # Add newline between files
                except UnicodeDecodeError:
                    outfile.write(f"# Warning: Could not read {file_name} - encoding error\n")
                except IOError:
                    outfile.write(f"# Warning: Could not read {file_name} - IO error\n")
                except PermissionError:
                    outfile.write(f"# Warning: Could not read {file_name} - permission denied\n")
                except Exception as e:
                    outfile.write(f"# Warning: Could not read {file_name} - {str(e)}\n")

print(f"File generated at: {output_file}")