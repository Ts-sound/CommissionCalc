import logging
import os
from datetime import datetime

class Logger:
    _instance = None
    
    @classmethod
    def get_logger(cls, name="CommissionCalc"):
        if cls._instance is None:
            cls._instance = cls._setup_logger(name)
        return cls._instance
    
    @classmethod
    def _setup_logger(cls, name):
        log_dir = "log"
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, f"{datetime.now().strftime('%Y-%m-%d')}.log")
        
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger

def get_logger():
    return Logger.get_logger()