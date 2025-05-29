# utils/logger.py
import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name: str = __name__):
    """Logger kurulumunu yapar"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Log formatı
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Konsol log
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Dosya log (max 5MB, 3 yedek)
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    file_handler = RotatingFileHandler(
        "logs/app.log",
        maxBytes=5*1024*1024,
        backupCount=3
    )
    file_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

# Global logger instance
logger = setup_logger("chatbot")