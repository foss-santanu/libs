from typing import Any, Self 

## ActionException class captures the execution errors

class ActionException(Exception):

    def __init__(self, messg: str = "Error in action", execp: Exception = None, *args: object) -> None:
        self.__messg = messg
        self.__topexecp = execp
        super().__init__(*args)

    def __str__(self) -> str:
        messg = self.__class__.__name__+": "+self.__messg
        if self.__topexecp:
            messg += str(self.__topexecp)
        return messg
    
## Enumeration class defining states of Action execution
## Three states: INIT, INPROGRESS, DONE 

from enum import Enum

class ActionState(Enum):
    INIT = 1, "Action initialized..."
    INPROGRESS = 2, "Action in progress..."
    DONE = 3, "Action completed..."

    def __new__(cls, value, description) -> Self:
        obj = object.__new__(cls)
        obj._value_ = value
        obj.description = description
        return obj

## Action2Exec executes the user action spec
## It stores the execution status, result and any execution error for future reference

class Action2Exec:

    def __init__(self, command: str, args: list) -> None:
        self.__name = command
        ## TODO - retrieve the command object for the command name
        self.__args = args
        self.__state = ActionState.INIT
        self.__exec_status = 0
        self.__exec_result = None
        self.__exec_error = None
        

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.__state = ActionState.INPROGRESS
        print(f"Action2Exec is called\n{self.__state.description}")
