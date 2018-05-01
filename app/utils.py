"""Utilities for the entire app."""

from functools import wraps


def lock_function(lock):
    """Lock a function but always release that lock."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                lock.acquire()
                return func(*args, **kwargs)
            finally:
                lock.release()
        return wrapper
    return decorator
