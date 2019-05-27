from rest_framework.status import is_success


def get_response_status(response_code):
    """Return the user friendly response text from the code"""
    if is_success(response_code):
        return 'success'
    return 'error'


def get_response_status_info(status_code):
    """
    Constructs and returns the response status information from
    response code
    """
    return {
        'status': get_response_status(status_code),
        'status_code': status_code,
    }
