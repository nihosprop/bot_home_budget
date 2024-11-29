import logging


class InfoWarningLogFilter(logging.Filter):
    def filter(self, record):
        return record.levelname in ('WARNING', 'INFO')


class ErrorCriticalLogFilter(logging.Filter):
    def filter(self, record):
        return record.levelname in ('ERROR', 'CRITICAL')


class DebugLogFilter(logging.Filter):
    def filter(self, record):
        return record.levelname == 'DEBUG'
