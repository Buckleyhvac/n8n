import ast
from src.task_analyzer import TaskAnalyzer
from src.config.security_config import SecurityConfig

security_config = SecurityConfig(
    stdlib_allow=set(),
    external_allow=set(),
    builtins_deny=set("eval,exec,compile,open,input,breakpoint,getattr,object,type,vars,setattr,delattr,hasattr,dir,memoryview,__build_class__,globals,locals,license,help,credits,copyright".split(",")),
    runner_env_deny=True
)

analyzer = TaskAnalyzer(security_config)

code = """
imp = __import__
os = imp.__call__("os")
return os.getpid()
"""

try:
    analyzer.validate(code)
    print("Validation successful")
except Exception as e:
    print(f"Validation failed: {e}")
