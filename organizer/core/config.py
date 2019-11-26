# This file reads the config files
# files need to be relative to the root directory
from yaml import load as ymlload, dump as ymldump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


class Config:
    config = dict

    def __init__(self):
        super().__init__()
        with open("./organizer/core/po_config.yml", "r") as ymlFile:
            self.config = ymlload(ymlFile, Loader=Loader)

    def getAllConfig(self):
        return self.config

    def getConfigKeys(self, section):
        return self.config[section]

    def getConfigValue(self, key, section):
        if section:
            return self.config[section][key]
        else:
            return self.config[key]

    def writeConfig(self, section, key, value):
        self.config[section][key] = value
        with open("po_config.yml", "w") as ymlFile:
            ymldump(self.config, ymlFile, Dumper=Dumper)
