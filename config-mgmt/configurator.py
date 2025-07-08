## This code file defines a Configurator class to facilitate config file handling

## Exception class for the Configurator

class ConfigurationException(Exception): 
    __name__ = "ConfigurationException"
    
    def __init__(self, message: str = "Exception raised", lowerexecpt: Exception = None, *args):
        super().__init__(*args)
        self.__message__ = message
        self.__lowerexecpt__ = lowerexecpt
        
    def __str__(self): 
        messg = self.__name__+": "+self.__message__+"\n"+str(self.__lowerexecpt__)
        return messg
    
## The Configurator class for in memory representation of config files

from pathlib import Path
from libs.simplecache import SimpleCache
from typing import Any
from functools import lru_cache
import re

class Configurator: 
    __name__ = "Configurator"
    
    def __init__(self,configFile: str, configDir: str = None, fileTyp: str = "json", sep: str = "."): 
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
        self.__configCache__ = SimpleCache()
        
    def __loadConfig(self, config2Load: Path, fileTyp: str = "json"): 
        pass
    
    def __isValidPrefix(self, key: str) -> bool: 
        prefixParts = key.split(self.__prefixSep__)
        isValid = True
        for part in prefixParts: 
            isValid = isValid and re.fullmatch(r"^\w+$", part) is not None
            if not isValid: 
                break
            
        return isValid
    
    @lru_cache
    def __configPartFor(self, prefix: str, config: dict) -> Any: 
        sepIndx = prefix.find(self.__prefixSep__)
        if sepIndx != -1: 
            key = prefix[:sepIndx]
            nxtConfig = config[key]
            nxtPrefix = prefix[sepIndx+1:]
            return self.__configPartFor(nxtPrefix, nxtConfig)
        else: 
            return config[prefix]
    
