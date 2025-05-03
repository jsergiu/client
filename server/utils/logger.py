import logging
import sys

def setup_logging(log_file="logs/server.log", log_level=logging.INFO):
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Return logger but typically you'd use module-level loggers
    return logging.getLogger()