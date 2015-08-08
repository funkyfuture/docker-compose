from compose.config import load as config_load
from compose.config import ConfigDetails
from compose.config.errors import ConfigurationError
from os import listdir, path
import yaml


class TestConfigValidation:
    def test_valid_service_dicts(self):
        basepath = path.abspath(path.join(path.dirname(__file__), '..', 'fixtures', 'valid_config'))
        dictsfile = path.join(basepath, 'valid_service_dicts.yml')
        with open(dictsfile, 'rt') as f:
            dicts = yaml.load(f)
        test = config_load
        for name, config in dicts.items():
            test.description = name
            config_details = ConfigDetails({name: config}, basepath, path.basename(dictsfile))
            yield test, config_details

    def test_invalid_config_files(self):
        basepath = path.abspath(path.join(path.dirname(__file__), '..', 'fixtures', 'invalid_config'))
        for file in [x for x in listdir(basepath) if x.endswith('.yml')]:
            with open(path.join(basepath, file), 'rt') as f:
                config_details = ConfigDetails(yaml.load(f), basepath, file)
            test = invalid_config
            test.description = file
            yield test, config_details

    def test_invalid_service_dicts(self):
        basepath = path.abspath(path.join(path.dirname(__file__), '..', 'fixtures', 'invalid_config'))
        dictsfile = path.join(basepath, 'invalid_service_dicts.yml')
        with open(dictsfile, 'rt') as f:
            dicts = yaml.load(f)
        test = invalid_config
        for name, config in dicts.items():
            test.description = name
            config_details = ConfigDetails({name: config}, basepath, path.basename(dictsfile))
            yield test, config_details


def invalid_config(config_details):
    try:
        config_load(config_details)
    except ConfigurationError:
        pass
    else:
        raise AssertionError("Malicious configuration validated: %s" % config_details.config)
