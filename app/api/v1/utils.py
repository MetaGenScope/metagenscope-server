"""Utilities for API v1."""

from flask import current_app
from werkzeug.exceptions import BadRequest

def kick_off_middleware(uuid, request, valid_tools, conductor_cls):
    """Use supplied conductor to kick off middleware for all available modules."""
    try:
        post_data = request.get_json()
        module_names = post_data['tools']
    except TypeError:
        module_names = []
    except KeyError:
        module_names = []
    except BadRequest:
        module_names = []

    tool_results = valid_tools
    if module_names:
        tool_results = [tool_cls for tool_cls in valid_tools
                        if tool_cls.name() in module_names]

    good_tools, bad_tools = [], []
    for cls in tool_results:
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
