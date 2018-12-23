import logging

class Config:
    app_name = "pycite"
    
    log_level = logging.DEBUG
    log_format = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
    log_formatter = logging.Formatter(log_format)

    
    @classmethod
    def getLogger(cls,  name: str):
        logger_name = cls.app_name + "." + name
        logger = logging.getLogger(logger_name)
        logger.setLevel(cls.log_level)
        console = logging.StreamHandler()
        console.setFormatter(cls.log_formatter)
        logger.addHandler(console)
        return logger
        
