import logging
import logging.handlers

_logger = logging.getLogger('config')

def _setup_logging(config):
    logging.root.setLevel(logging.DEBUG)
    
    basic_formatter = logging.Formatter(
        "%(asctime)s : %(levelname)s : %(name)s : %(message)s"
    )
    debug_formatter = logging.Formatter(
        "%(asctime)s : %(levelname)s : %(name)s:%(lineno)d[%(threadName)s] : %(message)s"
    )
    
    console_config = config.get('console')
    if console_config:
        handler = logging.StreamHandler()
        handler.setLevel(getattr(logging, console_config['level'].upper()))
        if console_config['level'] == 'debug':
            handler.setFormatter(debug_formatter)
        else:
            handler.setFormatter(basic_formatter)
        logging.root.addHandler(handler)
        
    file_config = config.get('file')
    if file_config:
        _logger.info("Configuring {level} file-based logging for {file}...".format(
            level=file_config['level'],
            file=file_config['path'],
        ))
        
        file_logger = logging.handlers.RotatingFileHandler(
            file_config['path'],
            maxBytes=file_config['rotation_size'],
            backupCount=file_config['rotation_count'],
        )
        if logging.root.handlers:
            _logger.info("Configured file-based logging with rotation every {count} bytes and history of {filecount}".format(
                count=file_config['rotation_size'],
                filecount=file_config['rotation_count'],
            ))
        file_logger.setLevel(getattr(logging, file_config['level'].upper()))
        if file_config['level'] == 'debug':
            file_logger.setFormatter(debug_formatter)
        else:
            file_logger.setFormatter(basic_formatter)
        logging.root.addHandler(file_logger)
        _logger.info("File-based logging online")
        
def init(config):
    global _setup_logging
    _setup_logging(config['logging'])
    del _setup_logging
    
    global TASK_DATABASE
    TASK_DATABASE = config['storage']['task_database']
    
    global TASK_FILEPATH
    TASK_FILEPATH = config['storage']['task_filepath']
    