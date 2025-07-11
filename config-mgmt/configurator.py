## This code file defines a Configurator class to facilitate config file handling
    
## The Configurator class for in memory representation of config files

from pathlib import Path
from functools import lru_cache
from commons import ConfigurationException, config_loader_registry 
from typing import Any
import re

class Configurator: 
    __name__ = "Configurator"
    
    def __init__(self, configFile: str, configDir: str = None, fileTyp: str = "native", sep: str = "."): 
        lookForConfig = Path.cwd()
        if configDir: 
            _dir = Path(configDir)
            if _dir.exists(): 
                lookForConfig = _dir
            else:
                raise ConfigurationException("Folder for config files not found")
        self.__configDir__ = lookForConfig
        config2Load = lookForConfig / configFile
        self.__configs__ = self.__loadConfig(config2Load, fileTyp)
        self.__configName__ = configFile.split(".")[0]
        self.__prefixSep__ = sep

    def __del__(self):
        del self.__configDir__
        del self.__configs__
        del self.__configName__
        del self.__prefixSep__
        
    def __loadConfig(self, config2Load: Path, fileTyp: str = "native"):
        name, config = config_loader_registry.load_config_file(config2Load, fileTyp)
        return config 
    
    def __isValidPrefix(self, key: str) -> bool: 
        prefixParts = key.split(self.__prefixSep__)
        isValid = True
        for part in prefixParts: 
            isValid = isValid and re.fullmatch(r"^\w+$", part) is not None
            if not isValid: 
                break
            
        return isValid

    @lru_cache(maxsize=1000)  ## lru_cache from functools caches config value for a config prefix
    def getConfigValue(self, prefix: str) -> Any:
        if not self.__isValidPrefix(prefix):
            raise ConfigurationException(f"Invalid key path {prefix}")
        configItm = self.__configs__
        prefixes = prefix.split(self.__prefixSep__)
        try:
            for key in prefixes:
                configItm = configItm[key]
        except Exception as e: 
            raise ConfigurationException(f"Key {prefix} is not mapped to any config",e)
        
        return configItm

