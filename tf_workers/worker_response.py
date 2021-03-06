"""
Worker Response
++++++++++++++++

Contains code related to handling worker response data
"""

import logging

from .response_codes import ResponseCodes as RC

log = logging.getLogger(__name__)


class WorkerResponse(object):
    """
    Stores responses generated by workers after their execution. Contains responses for both success
    and failures.

    :param response_code: Indicates if the worker succeeded or failed
    :param error_message: Contains the error message or complete traceback in case the worker failed
    :param data:
        contains the result returned from the worker. This might contain data even if
        the worker failed.
    """

    def __init__(self, response_code=None, error_message='', data=None, location=None):

        self.response_code = response_code
        self.error_message = error_message
        self.location = location

        if data:
            self.data = data
        else:
            self.data = {}

        self._post_execute = {}

    def to_dict(self):
        "Convert the response object to a dictionary"
        d = dict(
            response_code=self.response_code,
            error_message=self.error_message,
            location=self.location,
            data=self.data
        )

        # Add post-execute and other enhancements here
        if self._post_execute:
            d['post_execute'] = self._post_execute

        return d

    @classmethod
    def from_dict(cls, d):
        "Create a WorkerResponse object from a dictionary"

        if 'location' not in d:
            d['location'] = None

        obj = cls(response_code=d['response_code'],
                  error_message=d['error_message'],
                  location=d['location'],
                  data=d['data'])

        if 'post_execute' in d:
            obj._post_execute = d['post_execute']


        return obj

    def __repr__(self):
        if self.response_code is not None:
            return ("WorkerResponse("
                    "response_code={}, error_message='{}', location='{}', data={})".format(
                        RC.to_str(self.response_code), self.error_message,
                        self.location, self.data))
        else:
            return "WorkerResponse()"

    def __str__(self):
        return self.__repr__()
