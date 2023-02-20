# Standard Library imports
from contextlib import suppress
import json
import sys

# third-party imports
import requests


def request_handler_error_object(method, url, exception):
    """ simple helper to build request_handler error object """

    return {
        'method': method,
        'url': url,
        'type': exception.__class__.__name__,
        'exception': str(exception)
    }


def request_handler(method, url, auth, session=None, suppress_errors=(), **kwargs):
    """
    Universal requests interface with exception handling.

    The returned result object will contain either the request's
    response JSON object, an "errors" list, or both.

    Recommended practice: Test the result for "status_code" or "errors"
    before using "json" data. Presence of "json" data doesn't guarantee
    a successful request.

    :param method: request method string, e.g. 'GET', 'PUT'
    :param url: request endpoint URL
    :param auth: API authentication object
    :param session: optional requests.Session object for persisted TCP session
    :param suppress_errors: sequence of status codes to ignore for error logging
    :param kwargs: optional request kwargs
    :return: "result" dict:
                {
                    "errors": list, exception error objects or empty
                    "json": dict, response JSON contents or None
                    "Retry-After": int, seconds delay after response received
                    "status_code": int, response status code or None
                }
    """

    # initialize default return object
    result = {
        'errors': [],
        'json': None,
        'Retry-After': 0,
        'status_code': None,
    }

    try:
        # request may throw exceptions such as ConnectionError, Timeout
        response = (session.request if session else requests.request)(
            method, url, headers=auth, verify=True, timeout=60, **kwargs
        )
    except Exception as e:
        result['errors'].append(request_handler_error_object(method, url, e))

    # get response data, if available
    with suppress(NameError):
        result['status_code'] = response.status_code

        with suppress(KeyError, ValueError):
            result['Retry-After'] = int(response.headers['Retry-After'])

        # check for HTTP error
        try:
            response.raise_for_status()
        except Exception as e:
            result['errors'].append(request_handler_error_object(method, url, e))

        # get JSON content
        try:
            result['json'] = response.json()
        except Exception as e:
            result['errors'].append(request_handler_error_object(method, url, e))

    if result['errors'] and result['status_code'] not in suppress_errors:
        s = json.dumps(result, indent=3)
        print(f'request_handler: {s}', file=sys.stderr)

    return result
