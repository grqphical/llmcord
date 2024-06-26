"""LLMCord"""

import logging
from llmcord import __version__

ASCII_LOGO = f"""

  _____     _____     ____    ____   ______                        __  
 |_   _|   |_   _|   |_   \  /   _|.' ___  |                      |  ] 
   | |       | |       |   \/   | / .'   \_|  .--.   _ .--.   .--.| |  
   | |   _   | |   _   | |\  /| | | |       / .'`\ \[ `/'`\]/ /'`\\' |  
  _| |__/ | _| |__/ | _| |_\/_| |_\ `.___.'\| \__. | | |    | \__/  |  
 |________||________||_____||_____|`.____ .' '.__.' [___]    '.__.;__] 
                                                                       
                        Version {__version__}
                      Made by grqphical
            (https://github.com/grqphical/LLMCord)
"""


RED = "\033[0;31m"
CYAN = "\033[0;36m"
LIGHT_RED = "\033[1;31m"
YELLOW = "\033[1;33m"
END = "\033[0m"


class LoggingFormatter(logging.Formatter):
    """Formatter for LLMCord's logging"""

    FORMATS = {
        logging.INFO: f"{YELLOW}%(asctime)s {CYAN}%(levelname)s:{YELLOW} %(message)s{END}",
        logging.WARNING: f"{YELLOW}%(asctime)s %(levelname)s: %(message)s{END}",
        logging.ERROR: f"{YELLOW}%(asctime)s {LIGHT_RED}%(levelname)s:{YELLOW} %(message)s{END}",
        logging.CRITICAL: f"{YELLOW}%(asctime)s {RED}%(levelname)s:{YELLOW} %(message)s{END}",
    }

    def format(self, record: logging.LogRecord) -> str:
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


logger = logging.getLogger("llmcord")
logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(LoggingFormatter())

logger.addHandler(stream_handler)
print(f"{YELLOW}{ASCII_LOGO}{END}")
