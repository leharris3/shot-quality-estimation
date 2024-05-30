import pandas as pd
import os
import stat
import csv

import threading
import time


class TimeoutException(Exception):
    """Exception to raise when a timeout occurs"""

    def __init__(self, message="Function execution exceeded the allotted time"):
        self.message = message
        super().__init__(self.message)


def function_with_timeout(func, args=(), kwargs={}, timeout_duration=1):
    """
    Executes a function with a timeout.

    :param func: The function to execute.
    :param args: Tuple of arguments to pass to the function.
    :param kwargs: Dictionary of keyword arguments to pass to the function.
    :param timeout_duration: Maximum time in seconds to allow the function to run.
    :raises TimeoutException: If function execution exceeds the timeout duration.
    """

    # Define a wrapper to execute the function
    def wrapper():
        func(*args, **kwargs)

    # Create a thread to run the function
    thread = threading.Thread(target=wrapper)
    thread.start()

    # Wait for the thread to finish or timeout
    thread.join(timeout_duration)

    # If the thread is still active after the timeout, raise an exception
    if thread.is_alive():
        raise TimeoutException()
