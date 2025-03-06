import inspect
import json
import contextvars

class Fn:
    def __init__(self, target, *args):
        if not inspect.isfunction(target):
            raise TypeError(f"non-function passed to pg.Fn: {type(target)}")
        if not self._is_valid_return_type(target):
            raise TypeError(f"function does not have an error return value: {target}")
        if len(args) > self._num_expected_args(target):
            raise TypeError(f"too many arguments {len(args)} for function {target}")

        has_namespace_arg = False
        arg_offset = 0
        expected_args_count = self._num_expected_args(target)

        sig = inspect.signature(target)
        parameters = list(sig.parameters.values())

        if parameters and parameters[0].annotation == FnNamespace: # Placeholder, will define FnNamespace later if needed
            has_namespace_arg = True
            arg_offset += 1
            expected_args_count -= 1


        if not parameters or parameters[arg_offset].annotation != contextvars.Context:
            raise TypeError("invalid function, must have contextvars.Context as first or second argument")

        expected_args_count -= 1
        arg_offset += 1


        if len(args) != expected_args_count:
            raise TypeError(f"wrong number of arguments for fn, got {len(args)} for {target}")

        for i, arg in enumerate(args):
            param_index = i + arg_offset
            if param_index < len(parameters): # Check if param_index is within bounds
                param = parameters[param_index]
                if not self._is_supported_arg_type(param.annotation):
                    raise TypeError(f"argument {i} ({param.annotation}), is not a supported argument type")
                if not isinstance(arg, param.annotation):
                    expected_type_name = getattr(param.annotation, '__name__', str(param.annotation)) # Get name or string representation
                    arg_type_name = type(arg).__name__
                    raise TypeError(f"argument {i} expected to be {expected_type_name}, but is {arg_type_name}")
            else:
                # Should not happen due to argument count check above, but for robustness
                raise TypeError(f"Unexpected extra argument at index {i} for function {target}")


        try:
            args_id = json.dumps(args)
        except TypeError as e: # json.dumps can raise TypeError if args are not serializable
            raise TypeError(f"failed to generate JSON name for args: {e}") from e

        self._name = target.__name__
        self._id = f"{self._name}({args_id})"
        self._f = target
        self._call_args = args

    def _num_expected_args(self, func):
        sig = inspect.signature(func)
        params = sig.parameters.values()
        return len(params)

    def _is_valid_return_type(self, func):
        sig = inspect.signature(func)
        return_annotation = sig.return_annotation
        if return_annotation is inspect.Signature.empty:
            return False # No return annotation
        return return_annotation == type(None) or return_annotation == type(None) or return_annotation == type(None) # Placeholder for error type, using None for now.

    def _is_supported_arg_type(self, arg_type):
        supported_types = (int, str, bool) # tuple of supported types
        return arg_type in supported_types

    def id(self):
        return self._id

    def name(self):
        return self._name

    def run(self, ctx):
        call_args = [ctx] + list(self._call_args) # Context as first arg
        try:
            result = self._f(*call_args) # Call the function with context and args
            if result is not None: # Check for non-None return (assuming None means success, error is exception)
                raise Exception(f"Function {self._name} returned non-None value, expected None or raise Exception for error.") # Or handle error return type as needed
            return None # Indicate success (no error)
        except Exception as e: # Catch exceptions as errors
            return e # Return the exception as error


# Placeholder for FnNamespace, define if needed for namespace argument type checking
class FnNamespace:
    pass
