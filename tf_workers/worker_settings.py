"""
Worker Settings

Contains code related to handling data/configuration that is needed by a worker
for it's execution.
"""

from enum import Enum, unique
import logging

log = logging.getLogger(__name__)


class MemberExistsException(Exception):
    "Exception to specify that a setting member already exists"
    pass


class DataTypeMismatchException(Exception):
    "Exception raised when trying to set the value of a property with an unsupported data type"
    pass


@unique
class PropertySources(Enum):
    """
    This class lists the possible population sources for :class:`SettingProperty` objects

    :param user: Specifies that the value of this setting is specified by the user
    :param backend:
        Specifies that the backend should provide the value for this setting. Note that the backend
        will only support a very specific and small set of setting values. These include things like
        last status of plugin execution (last_response_code), last data that the plugin
        submitted (last_response) etc.
    """
    user = 1
    backend = 2


class SettingProperty(object):
    """
    Specifies a single settings property. :class:`WorkerSettings` is a collection
    of :class:`SettingProperty` objects

    :param name: name of the setting
    :param data_type:
        data type for the setting (e.g, int, str, bool, list, dict, date, object,
        CustomClass, etc)
    :param description: Optional description of the property. Helpful for API documentation
    :param default_value:
        The default value to use if a value is not provided. If we want a setting to be always
        required, set this to None.
    :param property_source:
        Describes how the property gets populated. Value must be a member
        of :class:`PropertySources`
    :param value: Current value of the setting
    """

    name = ''
    data_type = None
    default_value = None
    property_source = None
    description = ''
    _value = None

    def __init__(self, name, data_type, description='',  # pylint: disable=R0913
                 default_value=None, current_value=None, property_source=PropertySources.user):
        self.name = name
        self.data_type = data_type
        self.description = description
        self.default_value = default_value
        self._value = current_value

        assert property_source in PropertySources
        self.property_source = property_source

    @property
    def value(self):
        if self._value is not None:
            return self._value
        else:
            return self.default_value

    @value.setter
    def value(self, value):

        if value is not None and not isinstance(value, self.data_type):
            raise DataTypeMismatchException("Invalid data type {} for {} ({})".format(
                type(value), self.name, self.data_type))

        # log.debug("Setting value of %s to %r", self.name, value)
        self._value = value

    def __repr__(self):
        return "<SettingProperty(name={0.name}, data_type={0.data_type}, value={0.value})>".format(
            self
        )

    def __str__(self):
        return self.__repr__()


class WorkerSettings(object):
    "Stores settings specific to each worker plugin"

    def __init__(self):
        self._setting_names = []

    def add(self, sp):
        "Add given SettingProperty object as an attribute of current setting object"

        assert SettingProperty == type(sp)
        if sp.name in dir(self):
            raise MemberExistsException("{} is already a member of {} instance".format(
                sp.name, self.__class__.__name__))

        setattr(self, sp.name, sp)
        self._setting_names.append(sp.name)

    def from_dict(self, dict_in):
        """
        Populate worker settings from given dictionary (dict_in). Mostly used by worker runner to
        create plugin settings from config settings passed via celery.
        """

        for k, v in dict_in.items():
            if k in self._setting_names:
                getattr(self, k).value = v

    def to_dict(self, recursive=True, only_user_settings=False, only_required_settings=False):
        """
        Convert settings to dict and return it

        :param recursive:
            if value objects have a to_dict method, call it to convert them to dicts too
        :param only_user_settings: Return only user settings
        :param only_required_settings: Return only settings that don't have a default value
        """

        d = {}
        for sname in self._setting_names:
            if only_required_settings and getattr(self, sname).default_value is not None:
                continue

            if only_user_settings and getattr(self, sname).property_source != PropertySources.user:
                continue

            if (recursive and hasattr(getattr(self, sname).value, 'to_dict') and
                    callable(getattr(self, sname).value.to_dict)):

                d[sname] = getattr(self, sname).value.to_dict()
            else:
                d[sname] = getattr(self, sname).value

        return d

    def verify(self):
        """
        Checks if any settings are missing their required values, if yes returns a list of
        missing settings
        """

        missing = []
        for setting_name in self._setting_names:
            if getattr(self, setting_name).value is None:
                missing.append(setting_name)

        return missing
