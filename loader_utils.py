import importlib.util
import sys
import inspect
from pathlib import Path
import builtins

def import_into_namespace(file_path, target_namespace = None):
    """
    Dynamically loads a Python file and injects its public symbols into
    the specified namespace. Supports relative imports inside the file.

    :param file_path: Path to the .py file (str or Path)
    :param target_namespace: Dictionary (e.g. globals()) where symbols should be loaded.
                             Defaults to caller's global namespace.
    """
    file_path = Path(file_path).resolve(strict = True)
    module_name = file_path.stem
    parent_dir = file_path.parent
    fake_package = f"_dynamic_{module_name}"

    if str(parent_dir) not in sys.path:
        sys.path.insert(0, str(parent_dir))

    spec = importlib.util.spec_from_file_location(fake_package, str(file_path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[fake_package] = module
    spec.loader.exec_module(module)

    if target_namespace is None:
        target_namespace = inspect.currentframe().f_back.f_globals

    for name in dir(module):
        if not name.startswith("_"):
            target_namespace[name] = getattr(module, name)


def exec_and_get(code: str, varname: str, globals_dict = None, locals_dict = None, return_dicts = False):
    """
    Executes a block of Python code and returns the value of a specified variable.

    :param code: The Python code as a string.
    :param varname: The name of the variable to return after execution.
    :param globals_dict: Optional dictionary to use for globals. If None, a fresh one is used.
    :param locals_dict: Optional dictionary to use for locals. If None, globals_dict is reused.
    :param return_dicts: If True, also return the globals and locals dictionaries.
    :return: Value of the variable named `varname`, or a tuple (value, globals_dict, locals_dict) if return_dicts=True.
    """
    if globals_dict is None:
        globals_dict = {}
    if locals_dict is None:
        locals_dict = globals_dict

    exec(code, globals_dict, locals_dict)

    if varname not in locals_dict:
        raise NameError(f"Variable '{varname}' not defined in executed code.")

    result = locals_dict[varname]
    if return_dicts:
        return result, globals_dict, locals_dict
    return result
    
def resolve_dotted_name(name: str, namespace: dict, *, strict: bool = False):
    """
    Resolves a dotted name (e.g. 'math.sqrt') within a given namespace.

    :param name: Dotted name string
    :param namespace: Dictionary where resolution starts
    :return: Final object or None if not found
    """
     
    parts = name.split('.')
    obj = namespace.get(parts[0], None)

    ## Fall back to builtin functions
    if obj is None and len(parts) == 1 and hasattr(builtins, name):
        obj = getattr(builtins, name)
        
    if obj is None:
        if strict:
            raise NameError(f"{parts[0]} not found in namespace")
        return None
    for part in parts[1:]:
        obj = getattr(obj, part, None)
        if obj is None:
            if strict:
                raise AttributeError(f"'{part}' not found in path '{name=}'")
            return None
    return obj

def is_function_anywhere(name: str, namespace = None):
    """
    Checks if a name refers to a function (user-defined or built-in)
    in the given namespace.

    :param name: Dotted or simple name string
    :param namespace: Optional symbol table to use
    :return: True if it's a function, False otherwise
    """
    if namespace is None:
        frame = inspect.currentframe().f_back
        namespace = {**frame.f_globals, **frame.f_locals}

    obj = resolve_dotted_name(name, namespace)
    return inspect.isfunction(obj) or inspect.isbuiltin(obj)

def lookup_function(name: str, namespace = None, strict: bool = False):
    """
    Looks up a function object by name in a given namespace.

    :param name: Function name (can be dotted like 'math.sqrt')
    :param namespace: Optional dict of symbol table to search
    :return: Function object if found and valid, else None
    """
    if namespace is None:
        frame = inspect.currentframe().f_back
        namespace = {**frame.f_globals, **frame.f_locals}

    obj = resolve_dotted_name(name, namespace)
    if inspect.isfunction(obj) or inspect.isbuiltin(obj):
        return obj
    
    if strict:
        raise TypeError(f" '{name}' resolved but is not a function")
    
    return None
    
