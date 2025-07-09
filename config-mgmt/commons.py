## Exception class for the Configurator

from pathlib import Path
from types import SimpleNamespace
from typing import Callable

from libs.loader_utils import import_into_namespace

class ConfigurationException(Exception): 
    __name__ = "ConfigurationException"
    
    def __init__(self, message: str = "Exception raised", lowerexecpt: Exception = None, *args):
        super().__init__(*args)
        self.__message__ = message
        self.__lowerexecpt__ = lowerexecpt
        
    def __str__(self): 
        messg = self.__name__+": "+self.__message__+"\n"+str(self.__lowerexecpt__)
        return messg
    
def build_loader_registry():
    _config_loader = dict()

    def register_loader(loader: Callable, config_format: str):
        _config_loader[config_format] = loader

    def load_config_file(config_path, config_format: str = "native"):
        _loader = _config_loader.get(config_format, False)
        name = None
        config = dict()
        try:
            name, config = _loader(config_path)
        except Exception as e:
            raise ConfigurationException(f"Config file {str(config_path)} failed to load",e)
        else:
            return name, config

    return SimpleNamespace(
        register_loader = register_loader,
        load_config_file = load_config_file
    )

config_loader_registry = build_loader_registry()

def __native_config_loader(config_path):
    config2load = Path(config_path).resolve(strict =  True)
    config_name = config2load.stem
    configs = dict()
    import_into_namespace(config_path,configs)
    return config_name, configs

config_loader_registry.register_loader(__native_config_loader, "native")

import json

def __json_config_loader(config_path):
    config2load = Path(config_path).resolve(strict = True)
    config_name = config2load.stem
    configs = dict()
    with open(config2load, "r") as jsonFile:
        configs = json.load(jsonFile)
    return config_name, configs

config_loader_registry.register_loader(__json_config_loader, "json")

