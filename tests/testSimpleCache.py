## This file contains unit tests for SimpleCache class

import unittest
from libs.simplecache import SimpleCache
from collections import deque

class TestSimpleCache(unittest.TestCase): 
    
    def setUp(self):
        return super().setUp()
    
    def tearDown(self):
        return super().tearDown()
    
    def test_createCache(self): 
        scache = SimpleCache()
        self.assertIsInstance(scache.__cache__, dict, "From test_createCache: cache not a dictionary")
        self.assertEqual(len(scache.__cache__), 0, "From test_createCache: On creation cache size > 0")
        self.assertIsInstance(scache.__key2timestmp__, dict, "From test_createCache: key to timestamp mapping not a dictionary")
        self.assertEqual(len(scache.__key2timestmp__), 0, "From test_createCache: key to timestamp map size > 0")
        self.assertIsInstance(scache.__queue__, deque, "From test_createCache: Queue object not a collections.deque")
        self.assertEqual(scache.__queue__.maxlen, 1000, "From test_createCache: Dequeue size default is not 1000")
        
    def test_getForUnknownCacheKey(self): 
        scache = SimpleCache()
        self.assertIsNone(scache.getFromCache("AnyKey"), "From test_getForUnknownCacheKey: Value for an unkown key!!")
    
if __name__ == "__main__":
    unittest.main()
