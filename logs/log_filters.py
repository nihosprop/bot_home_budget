import logging


class WarningErrorLogFilter(logging.Filter):
    def filter(self, record):
        return record.levelname in ('WARNING', 'ERROR')


class CriticalLogFilter(logging.Filter):
    def filter(self, record):
        return record.levelname == 'CRITICAL'
