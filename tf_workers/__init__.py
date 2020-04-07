"""
tf_workers common code.

The main package containing all worker modules. Each worker module resides in
it's own folder. All workers are sub-classed from
:class:`.worker.Worker` class.

All workers must implement the :class:`.iworker.IWorker` interface, since the
:class:`.worker.Worker` class already implements this interface, sub-classing
from this class takes care of that.
"""
import logging
from importlib import import_module

from .response_codes import ResponseCodes  # pylint: disable=E0401
from .worker_response import WorkerResponse  # pylint: disable=E0401
from .worker import Worker  # pylint: disable=E0401
from .worker_settings import WorkerSettings, SettingProperty  # pylint: disable=E0401


log = logging.getLogger(__name__)


def is_valid_worker(worker_object):
    """
    Check if object is valid worker.

    Utility function to verify an object can be used as a worker. We're not
    verifying class because more complex workers might add members to the
    objects dynamically so it's better to verify the object

    :param worker_object: The object that needs to be checked
    """
    obj_attrs = ['name', 'resource_requirements', 'requires', 'os_requires']
    obj_methods = ['_init_settings', 'run']

    obj_dir = dir(worker_object)
    for attr in obj_attrs:
        if attr not in obj_dir:
            return False

    for o_m in obj_methods:
        if o_m not in obj_dir or not callable(getattr(worker_object, o_m)):
            return False

    return True


def get_worker(workername):
    """Return the specified worker class given the worker's name."""
    M = import_module('tfw_' + workername.lower())
    return M.worker_class
