## This code file defines a class to implement simple caching functionalities.
## This is a simple implementation of LRU cache with limited capacity.
## When items more than the defined capacity and saved in the cache
## the least recently used items are automatically removed from the cache.
## Each time a preiously added cache entery is accessed it is marked as most recently used.

import time
import collections

class SimpleCache: 
    
    def __init__(self, maxsize=1000, retention=30):
        self.__cache__ = dict()
        self.__key2timestmp__ = dict()
        self.__retention__ = retention
        self.__queue__ = collections.deque([],maxsize)

    def __del__(self):
        self.clearCache()
        del self.__cache__
        del self.__key2timestmp__
        del self.__queue__
        
    def addToCache(self, key, value): 
        self.__cache__[key] = value
        timestmp = time.time()
        self.__queue__.appendleft((key,timestmp))
        self.__key2timestmp__[key] = timestmp
        
    def getFromCache(self, key): 
        value = self.__cache__.get(key, False)
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
                    ## update the timestamp and make the entry most recent
                    now = time.time()
                    self.__queue__.remove((key,timestmp))
                    self.__queue__.appendleft((key,now))
                    self.__key2timestmp__[key] = now
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
    
    def remove(self, key): 
        value = self.__cache__.get(key, False)
        if value: 
            timestmp = self.__key2timestmp__.get(key)
            del self.__cache__[key]
            del self.__key2timestmp__[key]
            try:
                self.__queue__.remove((key,timestmp))
            except ValueError as e: 
                print(e)
                
    def clearCache(self): 
        self.__cache__.clear()
        self.__key2timestmp__.clear()
        self.__queue__.clear()
