from sandbox_util import (
    create_sandbox,
    get_sandbox_app,
    run_code,
    DRIVER_CODE,
)
from sandbox_code import generate_sandbox_code
import modal

def exec_python(code: str) -> str:
    """
    Executes the given Python code inside a Modal sandbox.
    """
    app = get_sandbox_app()
    sandbox = create_sandbox(app)

    try:
        # Start the sandbox with the driver program running (no stream=True!)
        proc = sandbox.exec("python", "-c", DRIVER_CODE)

        # Send formatted code to the driver
        script = generate_sandbox_code(code)

        # Execute the code and return results
        result = run_code(proc, script, timeout=30.0)
        return result
    finally:
        sandbox.terminate()

