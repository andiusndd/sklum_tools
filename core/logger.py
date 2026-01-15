import bpy
import tempfile
import logging
import os

class SKLUM_Logger:
    _instance = None
    _logger = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SKLUM_Logger, cls).__new__(cls)
            cls._instance._setup_logger()
        return cls._instance

    def _setup_logger(self):
        self._logger = logging.getLogger("SKLUM")
        self._logger.setLevel(logging.INFO)
        
        # Prevent duplicate handlers if re-initialized
        if self._logger.handlers:
            self._logger.handlers.clear()

        # Formatters
        formatter = logging.Formatter('[SKLUM] [%(levelname)s] %(asctime)s - %(message)s', datefmt='%H:%M:%S')

        # Stream Handler (Blender System Console)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        self._logger.addHandler(stream_handler)

        # File Handler
        try:
            # We place logs in the SYSTEM TEMP directory to avoid file locking issues during updates
            temp_dir = tempfile.gettempdir()
            log_dir = os.path.join(temp_dir, "SKLUM_Logs")
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            
            log_file = os.path.join(log_dir, "sklum_tools.log")
            
            # Rotation or appending? Standard append.
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setFormatter(formatter)
            self._logger.addHandler(file_handler)
            
            # Store it for cleaning later if needed
            self._file_handler = file_handler
        except Exception as e:
            print(f"Failed to setup file logging: {e}")

    def shutdown(self):
        """Closes all file handlers to release file locks."""
        if self._logger:
            handlers = self._logger.handlers[:]
            for handler in handlers:
                handler.close()
                self._logger.removeHandler(handler)

    def info(self, msg):
        self._logger.info(msg)

    def error(self, msg):
        self._logger.error(msg)
        # Also report to Blender's internal system if context is valid
        try:
             # This can be noisy, so we use it sparingly or via a dedicated method
             pass
        except:
            pass

    def warning(self, msg):
        self._logger.warning(msg)

    def debug(self, msg):
        self._logger.debug(msg)

# Global access point
logger = SKLUM_Logger()

def init_logger():
    """Call this on register"""
    return SKLUM_Logger()
