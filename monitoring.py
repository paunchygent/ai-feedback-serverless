#monitoring.py

import logging
import psutil
import time
import os

# Create 'logs' directory if it doesn't exist
if not os.path.exists('./logs'):
    os.makedirs('./logs')

# Set up logging with a FileHandler
logger = logging.getLogger("ResourceLogger")
logger.setLevel(logging.INFO)

# Create a FileHandler to write log messages to a file
file_handler = logging.FileHandler('./logs/resource_usage.log')
file_handler.setLevel(logging.INFO)

# Create a Formatter and set it for the handler
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the FileHandler to the logger
logger.addHandler(file_handler)

def log_resource_usage():
    while True:
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent

        # Use logger to write resource usage to the log file
        logger.info(f"CPU Usage: {cpu_usage}%")
        logger.info(f"Memory Usage: {memory_usage}%")
        logger.info(f"Disk Usage: {disk_usage}%")
        
        # Optional: Print resource usage to the console for real-time view
        print(f"CPU Usage: {cpu_usage}%")
        print(f"Memory Usage: {memory_usage}%")
        print(f"Disk Usage: {disk_usage}%")

        time.sleep(5)  # Log every 5 seconds