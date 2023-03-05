import logging

def logger(logfile):
    logging.basicConfig(filename=logfile, level=logging.INFO, format='%(asctime)s %(message)s', 
                        datefmt='%m/%d/%Y %I:%M:%S %p')

def get_logger(logfile):
    logger(logfile)
    return logging.getLogger()
