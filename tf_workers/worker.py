"""
Worker.

The Base class and related code for creating workers resides here
"""

from .worker_settings import WorkerSettings  # pylint: disable=E0402
from .worker_response import WorkerResponse  # pylint: disable=E0402


class IncompleteConfigException(Exception):
    """Exception indicating worker object's config settings are incomplete."""

    pass


class Worker(object):
    """
    The Base worker class.

    Implements :class:`.iworker.IWorker` interface and provides base
    functionality common to all workers.
    """

    name = 'Worker'
    resource_requirements = None
    requires = []

    def _init_settings(self):
        self.settings = WorkerSettings()

    def _create_settings(self, kwargs):
        """
        Create worker settings.

        Populate the supported settings from given args (normally passed to
        init). This is done by matching keyword name with setting names, if
        there is a match, it's value is set as the setting's value. Makes
        writing sub-classes easier as they don't have to worry about this
        implementation and can just pass the config as kwargs to __init__ of
        the worker.
        """
        for k, v in kwargs.items():
            if k in self.settings._setting_names:
                getattr(self.settings, k).value = v

    def __init__(self, kwargs):
        """Note that we won't use args, just keyword args."""
        self.response = WorkerResponse()

        self._init_settings()

        # handle back-end properties here . These are special cases as their
        # result is returned from the server-end so instead of the proper
        # class, it's serialized normally as dict. We need to convert it to
        # proper class here.
        if 'last_response' in kwargs:
            if kwargs['last_response']:
                kwargs['last_response'] = WorkerResponse.from_dict(
                    kwargs['last_response'])

        self._create_settings(kwargs)

    def run(self):
        """Run the worker."""
        missing = self.settings.verify()
        if missing:
            raise IncompleteConfigException(
                "Cannot run worker because values for these required settings"
                " are missing: {}".format(missing))
