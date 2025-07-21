import logging
import os
from datetime import datetime
from colorama import init, Fore, Style

# Initialize Colorama
init(autoreset=True)

class CustomFormatter(logging.Formatter):
    def format(self, record):
        msg = record.getMessage()

        # Colorize "Starting..." steps
        if "Starting" in msg:
            msg = f"{Fore.MAGENTA + Style.BRIGHT}{msg}"
        elif record.levelno == logging.ERROR:
            msg = f"{Fore.RED}{msg}"
        elif record.levelno == logging.WARNING:
            msg = f"{Fore.YELLOW}{msg}"
        else:
            msg = f"{Fore.WHITE}{msg}"

        return msg

def setup_logger(name, level=logging.INFO):
    if not os.path.exists('logs'):
        os.makedirs('logs')

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = f'logs/recon_{timestamp}.log'

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        # Console handler with custom formatter
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(CustomFormatter())

        # File handler with standard formatter (no color in logs)
        fh = logging.FileHandler(log_file)
        fh.setLevel(level)
        fh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

        logger.addHandler(ch)
        logger.addHandler(fh)

    return logger
