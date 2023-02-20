# request_handler
Python `requests` wrapper with exception handling  

```
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
```
# Recommendation use  
The returned result object will contain either the response JSON object, an `"errors"` list, or both.

Test the result for `"status_code"` or `"errors"` before using `"json"` data. **Note:** Presence of `"json"` data doesn't guarantee a successful request.

# Python 3 installation and package dependencies
`request_handler` requires Python 3.6 or newer. If you're new to Python, I recommend you install and use the open-source [Anaconda Distribution](https://www.anaconda.com/products/distribution). It's the easiest way I know to get a full Python installation with most of the packages you'll need when just starting out.

`request_handler` also depends on the third-party Python `requests` package. Check your installation to see if you have `requests` installed. If not, use either `% conda install requests` or `% pip install requests` to install `requests` to your Python environment. Anaconda includes `requests` as part of the standard package distribution.
