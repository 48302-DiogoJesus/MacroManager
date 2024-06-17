import inspect
from types import NoneType
from typing import Optional, Union, get_origin, get_args
from dataclasses import is_dataclass, fields

class TypeScriptInterfaceGenerator:
    @staticmethod
    def _python_to_typescript_type(py_type):
        if py_type is str:
            return 'string'
        elif py_type is int:
            return 'number'
        elif py_type is bool:
            return 'boolean'
        elif py_type is None:
            return 'void'
        elif py_type is NoneType:
            return 'null'
        elif py_type == list:
            return 'Array<any>'
        elif py_type == dict:
            return 'Record<string, any>'
        elif is_dataclass(py_type):
            return TypeScriptInterfaceGenerator._generate_dataclass_type(py_type)
        elif get_origin(py_type) == list:
            inner_type = get_args(py_type)[0]
            return f'Array<{TypeScriptInterfaceGenerator._python_to_typescript_type(inner_type)}>'
        elif get_origin(py_type) == dict:
            key_type, value_type = get_args(py_type)
            return f'Record<{TypeScriptInterfaceGenerator._python_to_typescript_type(key_type)}, {TypeScriptInterfaceGenerator._python_to_typescript_type(value_type)}>'
        elif get_origin(py_type) in [Optional, Union]:
            args = get_args(py_type)
            ts_types = [TypeScriptInterfaceGenerator._python_to_typescript_type(arg) for arg in args]
            return ' | '.join(ts_types)
        else:
            return 'any'

    @staticmethod
    def _generate_typescript_interface(class_obj):
        interface_str = '{\n'

        for method_name, method in inspect.getmembers(class_obj, predicate=inspect.isfunction):
            if method.__name__ == '__init__':
                continue  # Skip __init__ method if present (if class)

            # Get function signature
            signature = inspect.signature(method)
            params_str = ', '.join(f'{param.name}: {TypeScriptInterfaceGenerator._python_to_typescript_type(param.annotation)}' for param in signature.parameters.values() if param.annotation != inspect.Parameter.empty)
            return_type = TypeScriptInterfaceGenerator._python_to_typescript_type(method.__annotations__.get('return', None))

            # Format method line
            method_line = f'    {method_name}({params_str}): {return_type};\n'
            interface_str += method_line

        interface_str += '}\n'
        return interface_str

    @staticmethod
    def _generate_dataclass_type(dataclass_type):
        type_str = '{\n'

        for field in fields(dataclass_type):
            field_type = TypeScriptInterfaceGenerator._python_to_typescript_type(field.type)
            field_line = f'    {field.name}: {field_type};\n'
            type_str += field_line

        type_str += '}\n'
        return type_str

    @staticmethod
    def generate_typescript_interface_to_file(class_obj, out_file_path: str):
        type_literal: str = TypeScriptInterfaceGenerator._generate_typescript_interface(class_obj)
        type_literal = "export default interface IMacroManager \n" + type_literal
        with open(out_file_path, "w+") as f:
            f.write(type_literal)
        pass
