"""Utilities for API v1."""

from flask import current_app

from app.tool_results import all_tool_results


def kick_off_middleware(uuid, conductor_cls):
    """Use supplied conductor to kick off middleware for all available modules."""
    good_tools, bad_tools = [], []
    for cls in all_tool_results:
        tool_name = cls.name()
        try:
            conductor_cls(uuid, cls).shake_that_baton()
            good_tools.append(tool_name)
        except Exception:  # pylint: disable=broad-except
            current_app.logger.exception('Exception while coordinating display modules.')
            bad_tools.append(tool_name)

    payload = {
        'success': good_tools,
        'failure': bad_tools,
    }

    status = 201
    if bad_tools:
        status = 500

    return payload, status
