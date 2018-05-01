"""Utilities for the entire app."""


def lock_function(lock, func, *args, **kwargs):
    """Lock a function but always release that lock."""
    try:
        lock.acquire()
        return func(*args, **kwargs)
    except Exception:    # pylint: disable=broad-except
        lock.release()
