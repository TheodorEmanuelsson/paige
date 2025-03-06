import threading

_once_fns = {}
_mu = threading.Lock() # Mutex for thread-safe access to _once_fns

def run_once(key, fn):
    """
    Ensures that fn runs exactly once for a given key and always returns the result
    (or error) from the initial run.
    """
    with _mu: # Acquire lock for thread-safe access to _once_fns
        once_fn = _once_fns.get(key)
        if once_fn is None:
            once_fn = _make_once_fn(fn)
            _once_fns[key] = once_fn

    return once_fn() # Call the once_fn (outside the lock for performance)


def _make_once_fn(fn):
    """
    Creates a closure that wraps the original fn and uses threading.Lock and a flag
    to ensure fn is executed only once.
    """
    once_lock = threading.Lock() # Lock for the individual once_fn
    already_run = False
    result_or_exception = None # Store result or exception from the first run

    def _inner_once_fn():
        nonlocal already_run, result_or_exception # Allow modification of outer scope variables
        with once_lock: # Acquire lock for the inner once_fn
            if not already_run:
                try:
                    result = fn() # Execute the function
                    result_or_exception = result # Store the result
                except Exception as e:
                    result_or_exception = e # Store the exception
                finally:
                    already_run = True # Mark as run, regardless of success or failure

        if isinstance(result_or_exception, Exception): # If an exception was stored, raise it
            raise result_or_exception
        return result_or_exception # Return the stored result (which could be None if fn returns None)

    return _inner_once_fn
