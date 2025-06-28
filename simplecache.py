## This code file defines a class to implement simple caching functionalities

import time
import collections

class SimpleCache: 
    
    def __init__(self, maxsize=1000, retention=30):
        self.__cache__ = dict()
        self.__key2timestmp__ = dict()
        self.__retention__ = retention
        self.__queue__ = collections.deque([],maxsize)
        
    def addToCache(self, key, value): 
        self.__cache__[key] = value
        timestmp = time.time()
        self.__queue__.appendleft((key,timestmp))
        self.__key2timestmp__[key] = timestmp
        
    def getFromCache(self,key): 
        value = self.__cache__.get(key, default=False)
        if value: 
            timestmp = self.__key2timestmp__.get(key)
            now = time.time()
            timediff = (now - timestmp)
            if timediff <= self.__retention__:
                try: 
                    indx = self.__queue__.index((key,timestmp))
                except ValueError as e:
                    print(e)
                    ## remove cache entry
                    del self.__cache__[key]
                    del self.__key2timestmp__[key]
                else: 
                    print(f"Queue index for ({key}, {timestmp}) is: {indx}")
                    return value
            elif timediff > self.__retention__:
                ## remove cache entry
                del self.__cache__[key]
                del self.__key2timestmp__[key]
                try: 
                    self.__queue__.remove((key,timestmp))
                except ValueError as e:
                    print(e)
        return None 
                