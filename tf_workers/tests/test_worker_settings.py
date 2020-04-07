"Test cases for the :module:`tf_workers.worker` module"

from ..worker.worker_settings import WorkerSettings, SettingProperty, DataTypeMismatchException, PropertySources
import unittest


class TestWorkerSettings(unittest.TestCase):
    "Test cases for WorkerSettings and SettingProperty"

    def setUp(self):
        ws = WorkerSettings()
        self.setting_obj = ws
        self.setting_obj.add(SettingProperty('name', str))
        self.setting_obj.add(SettingProperty('age', int))
        self.setting_obj.add(SettingProperty('race', str, default_value='human'))

    def test_add(self):

        self.setting_obj.add(SettingProperty('address', str))

        for prop in ['name', 'age', 'race', 'address']:
            assert prop in dir(self.setting_obj)
            assert SettingProperty == type(getattr(self.setting_obj, prop))

    def test_default_value(self):
        assert 'human' == self.setting_obj.race.value

    def test_set_value(self):
        self.setting_obj.name.value = 'Ada'
        assert 'Ada' == self.setting_obj.name.value

    def test_invalid_datatype(self):
        with self.assertRaises(DataTypeMismatchException):
            self.setting_obj.age.value = 'hundred years'

    def test_verify_settings_success(self):

        self.setting_obj.name.value = 'Ada'
        self.setting_obj.age.value = 35

        assert [] == self.setting_obj.verify()

    def test_verify_settings_failure(self):

        missing = self.setting_obj.verify()
        assert 'name' in missing
        assert 'age' in missing
        assert 2 == len(missing)

    def test_populate_from_dict(self):
        d = dict(name='XYZ', age=75)
        self.setting_obj.from_dict(d)

        assert self.setting_obj.name.value == 'XYZ'
        assert self.setting_obj.age.value == 75

    def test_valid_property_source(self):
        self.setting_obj.add(SettingProperty('previous_status', str, property_source=PropertySources.backend))
        assert self.setting_obj.previous_status.property_source is PropertySources.backend

    def test_invalid_property_source(self):
        with self.assertRaises(AssertionError):
            self.setting_obj.add(SettingProperty('last_result', str, property_source='some source'))
