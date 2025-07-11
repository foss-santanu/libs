# __Library codes developed by me__
### This is work in progress

## __Tools developed for...__
1. **_Configuration Management_**

    - Found in the package _config-mgmt_
    - Defines a _Configurator_ class 
        - Loades a configuration file from path (currently - _json_ and _.py_ formats supported)
        - New config format supported using _config_loader_registry.register_loader()_
    - Defines a _ConfigurationException_ class to represent any config related error condition
    
2. **_Simple LRU Caching_**

   - Defined in the module _simplecache_ in _libs_ package
   - Defines a class _SimpleCache_ for implementing the **LRU cache**
   - A limited sized cache (_default 1000 entries_), size is specified during instantiating the cache
   - When number of entries exceeds cache size old entries are automatically removed from cache
   
3. **_Dynamic code loading utility_**

   - Defined in the module _loader_utils_ in _libs_ package
   - Function _import_into_namespace()_ imports a python module into target namespace
     - If no target namespace provided it _defaults to callers global namespace_
    - Function _exec_and_get()_ executes python code snippet in a string and returns the variable value
    - Function _lookup_function()_ looks up for a function name in the namespace and returns the function object
    

## __Usages__

For usage details please go through respective the code files, all the name are pretty self explanatory and all the important code segments are appropriately commented.