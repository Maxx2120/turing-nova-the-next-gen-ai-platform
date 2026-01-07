import logging
import sys
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name: str = "app", log_file: str = "app.log", level: int = logging.INFO) -> logging.Logger:
    """
    Sets up a production-ready logger with both console and file output.
    
    Args:
        name_ (str): Name of the logger
        log_file (str): Path to the log file
        level (int): Logging level (default: logging.INFO)
    
    Returns:
        logging.Logger: Configured logger instance
    """
    
    # Create logs directory if it doesn't exist
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    log_path = os.path.join(log_dir, log_file)

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Prevent duplicate logging if logger is already set up
    if logger.handlers:
        return logger

    # Formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )

    # File Handler (with rotation: 5MB max size, keep last 3 cpus)
    file_handler = RotatingFileHandler(log_path, maxBytes=5*1024*1024, backupCount=3)
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(level)

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(level)

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Create a global logger instance to be imported elsewhere
logger = setup_logger()
