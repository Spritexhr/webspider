from retrying import retry

@retry(stop_max_attempt_number = 3)
def make_trouble():
    print("Trying...")
    raise Exception("Exception!")

try:
    make_trouble()
except Exception:
    print("Failed, even with retrying.")

from retrying import retry

def retry_if_io_error(exception):
    """Return True if we should retry (in this case when it's an IOError), False otherwise"""
    return isinstance(exception, IOError)

@retry(retry_on_exception=retry_if_io_error,stop_max_attempt_number=3, wait_fixed=2000)
def might_io_error():
    print("Trying...")
    raise IOError("IO Error!")

try:
    might_io_error()
except Exception:
    print("Failed, even with retrying.")
