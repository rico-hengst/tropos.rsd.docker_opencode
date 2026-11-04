import os
import json
import time
import functools
import logging
from logging.handlers import TimedRotatingFileHandler

# helper to get loglevel from ENV
def _resolve_level(default=logging.INFO):
    raw = os.getenv(default, "").strip().upper()
    if not raw:
        return default
    # Handles both "DEBUG" and "10"
    level = logging.getLevelName(raw)
    return level if isinstance(level, int) else default


def setup_logger() -> logging.Logger:
    """
    Configures and returns a logger instance with:
    - STDOUT Handler (Format: Datetime, Level, Message)
    - File Handler (lucky.log) (Format: Datetime, Level, Message, Module, Function, Line number)
    """
    
    # 0 logfile
    APP_CONFIG_PATH_CONTENT = get_APP_CONFIG_PATH()
    
    # 1. Create the logger
    logger = logging.getLogger()
    
    # Avoid adding handlers if the logger was already configured
    if logger.handlers:
        return logger

    # 2. Set the global log level
    logger.setLevel(logging.DEBUG)

    # 3. FORMATTER FOR FILE (Detailed: Datetime, Level, Message, Module, Line)
    file_formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(message)s | %(module)s | %(funcName)s:%(lineno)d",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 4. FORMATTER FOR STDOUT (Simple: Datetime, Level, Message)
    stdout_formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(message)s | %(module)s | %(funcName)s:%(lineno)d",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    

    # 5. Create STDOUT Handler
    stdout_handler = logging.StreamHandler()
    #stdout_handler.setLevel(logging.DEBUG)  # Show INFO and above on console
    stdout_handler.setLevel(_resolve_level( APP_CONFIG_PATH_CONTENT["loglevel_STDOUT"]) )  # Show INFO and above on console
    stdout_handler.setFormatter(stdout_formatter)  # Apply the simple formatter
    logger.addHandler(stdout_handler)

    # 6. Create File Handler (Rotates daily, keeps 7 days)
    file_handler = TimedRotatingFileHandler(
        filename=APP_CONFIG_PATH_CONTENT["logfile"],
        when="midnight",
        interval=1,
        backupCount=7,
        encoding="utf-8"
    )
    file_handler.setLevel(APP_CONFIG_PATH_CONTENT["loglevel_LOGFILE"])  # Save everything to file
    file_handler.setFormatter(file_formatter)  # Apply the detailed formatter
    logger.addHandler(file_handler)


    return logger
    

def get_APP_CONFIG_PATH():
    try:
        myfile= os.path.dirname(os.path.abspath(__file__)) + "/../config/app.conf"
        if not os.path.isfile(myfile):
            print("file not exists " + myfile)

            
        with open(myfile, 'r') as file:
            APP_CONFIG_PATH_CONTENT = json.load(file)
        if "logfile" not in APP_CONFIG_PATH_CONTENT:
            print("logfile not exists: " + APP_CONFIG_PATH_CONTENT["logfile"] )
            exit()
        elif not os.path.isfile(APP_CONFIG_PATH_CONTENT["logfile"]):
            with open(APP_CONFIG_PATH_CONTENT["logfile"], mode='w') as f:
                f.write("")
            
        return APP_CONFIG_PATH_CONTENT
        
    except json.JSONDecodeError:
        exit()
    
    
    
    
# time function wrap function to get execution time
# Usage with options:
# ```python
# @timer(level=logging.DEBUG)
# def my_function():
    # ...
def timer(func=None, *, level=logging.INFO):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = f(*args, **kwargs)
            duration = time.perf_counter() - start
            logger = setup_logger()
            logger.log(level, f"### - execution time of {f.__module__}.{f.__name__} : {duration:.4f}s")
            return result
        return wrapper
    
    if func is None:
        return decorator
    return decorator(func)


# Async version
def async_timer(func=None, *, level=logging.INFO):
    def decorator(f):
        @functools.wraps(f)
        async def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = await f(*args, **kwargs)
            duration = time.perf_counter() - start
            logger = setup_logger()
            logger.log(level, f"### - execution time of {f.__module__}.{f.__name__} : {duration:.4f}s")
            return result
        return wrapper
    
    if func is None:
        return decorator
    return decorator(func)
