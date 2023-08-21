import logging
import os
from logging.handlers import RotatingFileHandler

log_folder = 'logs'
os.makedirs(log_folder, exist_ok=True)
log_file = os.path.join(log_folder, "spc.log")

log_level = logging.DEBUG

# Create a rotating file handler
handler = RotatingFileHandler(log_file, maxBytes=20971520, backupCount=3)

# Set the log level for the handler
handler.setLevel(log_level)

# Define the log format
log_format = '%(asctime)s %(levelname)s %(name)s : %(message)s'
formatter = logging.Formatter(log_format)

# Set the formatter for the handler
handler.setFormatter(formatter)

# Get the root logger
logger = logging.getLogger("logs")
logger.setLevel(log_level)

# Add the rotating file handler to the root logger
logger.addHandler(handler)
