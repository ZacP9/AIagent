from config import MAX_FILE_CONTENT_CHAR

def get_files_info(working_directory, directory="."):
    """
    Get information about files in the specified directory.

    Args:
        working_directory (str): The base directory to search in.
        directory (str): The subdirectory to search in, defaults to current directory.

    Returns:
        string: A string containing file names and their sizes.
    """
    import os

    full_path = os.path.join(working_directory, directory)

    # If the directory argument is not a directory, again, return an error string:
    if not os.path.isdir(full_path):
        return f"Error: \"{directory}\" is not a valid directory"
    
    # Convert both paths to absolute paths for proper comparison
    abs_full_path = os.path.abspath(full_path)
    abs_working_dir = os.path.abspath(working_directory)

   # If the absolute path to the directory is outside the working_directory, return a string error message:
    if not abs_full_path.startswith(abs_working_dir):
        return f"Error: Cannot list \"{directory}\" as it is outside the permitted working directory"

    files_info = []
    for filename in os.listdir(full_path):
        file_path = os.path.join(full_path, filename)
        if os.path.isfile(file_path):
            filename = filename.strip()
            file_size = os.path.getsize(file_path)
            files_info.append(f"- {filename}: file_size={file_size} bytes, is_dir=False")
        elif os.path.isdir(file_path):
            filename = filename.strip()
            dir_size = os.path.getsize(file_path)
            files_info.append(f"- {filename}: file_size={dir_size} bytes, is_dir=True")

    all_content_string = "\n".join(files_info)
    return all_content_string


def get_file_content(working_directory, file_path):
    """
    Get the content of a file in the specified directory.

    Args:
        working_directory (str): The base directory to search in.
        file_path (str): The path to the file relative to the working directory.

    Returns:
        str: The content of the file or an error message if the file does not exist.
    """
    import os

    full_path = os.path.join(working_directory, file_path)

    abs_full_path = os.path.abspath(full_path)
    abs_working_dir = os.path.abspath(working_directory)

    if not abs_full_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(full_path, 'r') as f:
            content = f.read(MAX_FILE_CONTENT_CHAR)
    except Exception as e:
        return f'Error: Could not read file "{file_path}": {str(e)}'

    return content

def write_file(working_directory, file_path, content):
    """
    Write content to a file in the specified directory.

    Args:
        working_directory (str): The base directory to write in.
        file_path (str): The path to the file relative to the working directory.
        content (str): The content to write to the file.

    Returns:
        str: A success message or an error message if the write operation fails.
    """
    import os

    full_path = os.path.join(working_directory, file_path)

    abs_full_path = os.path.abspath(full_path)
    abs_working_dir = os.path.abspath(working_directory)

    if not abs_full_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    # if path does not exist, create the necessary directories
    try:
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
    except Exception as e:
        return f'Error: Could not create directories for "{file_path}": {str(e)}'   

    try:
        with open(full_path, 'w') as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: Could not write to file "{file_path}": {str(e)}'