import logging as customlogging
import os
from datetime import datetime

# Set the log file name using the current datetime
LOG_FILE = f'{datetime.now().strftime("%m_%d_%Y_%H_%M_%S")}.log'

# Define the path to store the logs
log_path = os.path.join(os.getcwd(), "logs")

# Create the log directory if it doesn't exist
os.makedirs(log_path, exist_ok=True)

# Full path to the log file
LOG_FILEPATH = os.path.join(log_path, LOG_FILE)

# Set up the basic configuration for logging
customlogging.basicConfig(
    level=customlogging.INFO, 
    filename=LOG_FILEPATH,
    format="[%(asctime)s] %(lineno)d %(name)s -%(levelname)s - %(message)s"
)

# Create a logger instance
logger = customlogging.getLogger()

# Example log entries
logger.info("This is an info message")
logger.warning("This is a warning message")
