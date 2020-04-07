"""
Test cases for tf_workers.worker.worker_response.WorkerResponse
"""

import unittest
from ..worker import WorkerResponse, ResponseCodes as RC


class TestWorkerSettings(unittest.TestCase):
    "Test cases for WorkerSettings and SettingProperty"

    def test_empty_response(self):  # pylint: disable=R0201
        wr = WorkerResponse()

        assert wr.response_code is None
        assert {} == wr.data
        assert '' == wr.error_message

    def test_success_response(self):  # pylint: disable=R0201
        wr = WorkerResponse(RC.SUCCESS)

        assert RC.SUCCESS == wr.response_code
        assert {} == wr.data
        assert '' == wr.error_message

    def test_failure_response(self):  # pylint: disable=R0201
        wr = WorkerResponse(RC.FAILURE, 'worker failed')

        assert RC.FAILURE == wr.response_code
        assert {} == wr.data
        assert 'worker failed' == wr.error_message

    def test_to_dict(self):  # pylint: disable=R0201
        wr = WorkerResponse(RC.FAILURE, 'worker failed')
        d = wr.to_dict()

        assert RC.FAILURE == d['response_code']
        assert 'data' in d
        assert 'error_message' in d
        assert 'alerts' not in d
        assert 'post_execute' not in d
