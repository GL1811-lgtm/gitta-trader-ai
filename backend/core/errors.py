import functools
import traceback
from backend.utils.logger import logger

class GittaError(Exception):
    """Base class for all Gitta Trader AI exceptions."""
    pass

class MarketDataError(GittaError):
    """Raised when there are issues fetching or parsing market data."""
    pass

class StrategyError(GittaError):
    """Raised when a strategy fails to execute or validate."""
    pass

class OrderExecutionError(GittaError):
    """Raised when an order fails to be placed or executed."""
    pass

class ConfigurationError(GittaError):
    """Raised when there is a missing or invalid configuration."""
    pass

def global_error_handler(func):
    """Decorator to catch and log unhandled exceptions in functions."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except GittaError as e:
            logger.error(f"Known Error in {func.__name__}: {str(e)}")
            # In a real app, you might want to re-raise or handle specific cases
            raise e
        except Exception as e:
            logger.error(f"Unhandled Exception in {func.__name__}: {str(e)}")
            logger.error(traceback.format_exc())
            raise e # Re-raise to ensure the caller knows something went wrong
    return wrapper
