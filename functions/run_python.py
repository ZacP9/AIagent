
def run_python_file(working_directory, file_path, args=[]):
    """
    Run a Python file in the specified directory with given arguments.

    Args:
        working_directory (str): The base directory to run the Python file in.
        file_path (str): The path to the Python file relative to the working directory.
        args (list): A list of arguments to pass to the Python script.

    Returns:
        str: The output of the script or an error message if the script cannot be run.
    """
    import os
    import subprocess

    full_path = os.path.join(working_directory, file_path)

    abs_full_path = os.path.abspath(full_path)
    abs_working_dir = os.path.abspath(working_directory)

    if not abs_full_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(full_path):
        return f'Error: File "{file_path}" not found.'

    if not full_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        result = subprocess.run(
            ['python', file_path] + args,
            capture_output=True,
            text=True,
            check=False,
            cwd=working_directory,
            timeout=30
        )

         # If the process exits with a non-zero code"
        if result.returncode != 0:
            error_msg = f"Error: Process exited with code {result.returncode}"
            if result.stderr.strip():
                error_msg += f" - {result.stderr.strip()}"
            return error_msg

        if not result.stdout.strip() and not result.stderr.strip():
            return "No output produced."

        output_parts = []
        if result.stdout.strip():
            output_parts.append(f"STDOUT: {result.stdout.strip()}")
        if result.stderr.strip():
            output_parts.append(f"STDERR: {result.stderr.strip()}")
        
        return " ".join(output_parts)

    except subprocess.TimeoutExpired:
        return "Error: Script execution timed out after 30 seconds"
    except Exception as e:
        return f"Error: executing Python file: {e}"

   

   