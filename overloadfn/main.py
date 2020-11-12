from inspect import signature, _empty, ismethod, getmro, isbuiltin, isfunction, getmodule
from typing import Any, Union, get_origin, get_args
from typeguard import check_type
from types import FunctionType, BuiltinFunctionType, MethodType, BuiltinMethodType
import pydoc
import logging
import functools

logging.getLogger('overloadfn').addHandler(logging.NullHandler())

def Overload(*types):
    def wrapper(f):
        def self_handler(callingObj, *args, **kwargs):
            if callingObj is None:
                return f(*args, **kwargs)
            else:
                return f(callingObj, *args, **kwargs)
        self_handler.origin = f
        typeHints = OverloadedFunction.inspectTypes(f)
        isClassMethod = len(f.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)) > 1
        if isClassMethod:
            typeHints = typeHints[1:]
        argtypes = tuple((list(types) + typeHints[len(types):])[:len(typeHints)])
        self_handler.types = argtypes
        return OverloadedFunction(self_handler)
    return wrapper
        
class OverloadedFunction(object):
    
    @staticmethod
    def inspectTypes(fnOrArgs):
        if callable(fnOrArgs):
            fn = fnOrArgs
            try:
                s = signature(fn)
            except ValueError:
                return []
            return [Any if value.annotation == _empty else value.annotation for value in s.parameters.values()]
        else:
            args = fnOrArgs
            return [arg.__class__ if hasattr(arg,'__class__') else type(arg) for arg in args]
    
    def __init__(self, func):
        self.owner = None
        self.types = []
        self.methods = []
        self.qualname = (func.origin if hasattr(func,'origin') else func).__qualname__
        self.types.append(func.types if hasattr(func,'types') else OverloadedFunction.inspectTypes(func))
        self.methods.append(func)
        argstr = ', '.join(['Any' if t is Any else t.__str__().replace('typing.','') if t.__module__ == 'typing' else t.__name__ for t in func.types])
        logging.info('Overload set up for \'{}\' with argument types ({})'.format(self.qualname, argstr))
        
    def __get__(self, owner, ownerType=None):
        self.owner = owner or self
        return self
    
    def __call__(self, *args, **kwargs):
        called_args = list(args)
        if len(kwargs.values()) > 0:
            called_args.append(kwargs.values())
        called_argtypes = tuple([arg.__class__ if hasattr(arg,'__class__') else type(arg) for arg in called_args])
        for ind, argTypes in enumerate(self.types):
            if len(called_argtypes) != len(argTypes):
                continue
            allMatch = True
            for i, argType in enumerate(argTypes):
                if argType.__module__ == 'typing':
                    o = get_origin(argType)
                    if o == Union:
                        def originReduce(t):
                            o = get_origin(t)
                            while o is not None:
                                t = o
                                o = get_origin(t)
                            return t
                        ts = tuple(map(originReduce, get_args(argType)))
                        if not issubclass(called_argtypes[i],ts):
                            allMatch = False
                            break
                    elif argType == Any:
                        continue
                    else:
                        error = False
                        try:
                            check_type("arg", called_args[i], argType, None)
                        except TypeError:
                            error = True
                        if error:
                            allMatch = False
                            break
                elif not issubclass(called_argtypes[i],argType) and not isinstance(called_args[i],argType):
                    allMatch = False
                    break
            if allMatch:
                logging.info('Overload of \'{}\' for ({}) agrument types is ({}) implementation'.format(
                    self.qualname,
                    ', '.join(['Any' if t is Any else t.__str__().replace('typing.','') if t.__module__ == 'typing' else t.__name__ for t in called_argtypes]),
                    ', '.join(['Any' if t is Any else t.__str__().replace('typing.','') if t.__module__ == 'typing' else t.__name__ for t in argTypes])
                ))
                return self.methods[ind](self.owner, *args, **kwargs)
        raise TypeError("There is no overload for \'{}\' with ({}) argument types".format(self.qualname, ', '.join(['Any' if t is Any else t.__str__().replace('typing.','') if t.__module__ == 'typing' else t.__name__ for t in called_argtypes])))
    
    def overload(self, *types):
        def wrapper(f):
            def self_handler(callingObj, *args, **kwargs):
                if callingObj is None:
                    return f(*args, **kwargs)
                else:
                    return f(callingObj, *args, **kwargs)
            self_handler.origin = f
            typeHints = OverloadedFunction.inspectTypes(f)
            isClassMethod = len(f.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)) > 1
            if isClassMethod:
                typeHints = typeHints[1:]
            argtypes = tuple((list(types) + typeHints[len(types):])[:len(typeHints)])
            self_handler.types = argtypes
            self.types.append(argtypes)
            self.methods.append(self_handler)
            argstr = ', '.join(['Any' if t is Any else t.__str__().replace('typing.','') if t.__module__ == 'typing' else t.__name__ for t in argtypes])
            logging.info('Overload added for \'{}\' with argument types ({})'.format(self.qualname, argstr))
            return self
        return wrapper