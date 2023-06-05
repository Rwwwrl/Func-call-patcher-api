from typing import NewType

FuncCallPatherId = NewType('FuncCallPatherId', int)

DecoratorInnerFuncAsStr = NewType('DecoratorInnerFuncAsStr', str)
"""
объявленная функция в виде строки
пример:
decorator_inner_func_as_str = '''
def some(func, func_args, func_kwargs, frame):
    return func(*func_args, **func_kwargs)
'''
"""
