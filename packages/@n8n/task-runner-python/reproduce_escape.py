import multiprocessing
import traceback
import textwrap
import json
import io
import os
import sys
import logging
from typing import cast

from src.config.security_config import SecurityConfig
from src.task_executor import TaskExecutor
from src.constants import EXECUTOR_USER_OUTPUT_KEY
from src.import_validation import validate_module_import

security_config = SecurityConfig(
    stdlib_allow=set(),
    external_allow=set(),
    builtins_deny=set("eval,exec,compile,open,input,breakpoint,getattr,object,type,vars,setattr,delattr,hasattr,dir,memoryview,__build_class__,globals,locals,license,help,credits,copyright".split(",")),
    runner_env_deny=True
)

def _wrap_code(raw_code: str) -> str:
    indented_code = textwrap.indent(raw_code, "    ")
    return f"def _user_function():\n{indented_code}\n\n{EXECUTOR_USER_OUTPUT_KEY} = _user_function()"

def _create_safe_import(security_config: SecurityConfig):
    import builtins
    original_import = builtins.__import__

    def safe_import(name, *args, **kwargs):
        is_allowed, error_msg = validate_module_import(name, security_config)

        if not is_allowed:
            raise Exception(f"Security violation: {error_msg}")

        return original_import(name, *args, **kwargs)

    return safe_import

def filter_builtins(security_config: SecurityConfig):
    import builtins
    b_dict = vars(builtins)
    filtered = {
        k: v
        for k, v in b_dict.items()
        if k not in security_config.builtins_deny
    }
    filtered["__import__"] = _create_safe_import(security_config)
    return filtered

code = """
try:
    imp = __import__
    os = imp("os")
    return os.getpid()
except Exception as e:
    return str(e)
"""

wrapped_code = _wrap_code(code)
compiled_code = compile(wrapped_code, "<all_items_task_execution>", "exec")

globals_dict = {
    "__builtins__": filter_builtins(security_config),
    "_items": [],
    "_query": None,
}

exec(compiled_code, globals_dict)

print(f"User output: {globals_dict[EXECUTOR_USER_OUTPUT_KEY]}")
