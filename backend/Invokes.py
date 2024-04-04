import requests

SUPPORTED_HTTP_METHODS = {"GET", "OPTIONS", "HEAD", "POST", "PUT", "PATCH", "DELETE"}

def invoke_http(url, method='GET', json=None, headers=None, timeout=10, **kwargs):
    """
    A simple wrapper for making HTTP requests using the 'requests' library.

    Parameters:
    - url (str): The URL of the HTTP service.
    - method (str): The HTTP method to use (e.g., 'GET', 'POST'). Default is 'GET'.
    - json (dict): The JSON payload for methods that send data (e.g., 'POST', 'PUT'). Default is None.
    - headers (dict): Additional HTTP headers to send with the request. Default is None.
    - timeout (int): The request timeout in seconds. Default is 10 seconds.
    - **kwargs: Additional arguments that 'requests.request' accepts.

    Returns:
    A dict containing the response data. If an error occurs, returns a dict with 'code' and 'message'.
    """
    try:
        if method.upper() not in SUPPORTED_HTTP_METHODS:
            raise ValueError("HTTP method {} unsupported.".format(method))
        
        response = requests.request(method, url, json=json, headers=headers, timeout=timeout, **kwargs)
        
        # Check if the response status code indicates success.
        response.raise_for_status()

        # Try to parse the response as JSON. If parsing fails or response is empty, return a default dict.
        try:
            return response.json() if response.content else {}
        except ValueError:
            return {"code": response.status_code, "message": "Non-JSON response received"}
    except requests.exceptions.HTTPError as http_err:
        # Specific HTTP errors (e.g., 404 Not Found, 403 Forbidden)
        return {"code": response.status_code, "message": str(http_err)}
    except requests.exceptions.RequestException as req_err:
        # Broad request exceptions (e.g., connection errors)
        return {"code": 500, "message": "HTTP request failed: " + str(req_err)}
    except ValueError as ve:
        # Handle specific value errors, e.g., unsupported HTTP method.
        return {"code": 400, "message": str(ve)}
