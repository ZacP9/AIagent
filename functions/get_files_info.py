
def get_files_info(working_directory, directory="."):
    """
    Get information about files in the specified directory.

    Args:
        working_directory (str): The base directory to search in.
        directory (str): The subdirectory to search in, defaults to current directory.

    Returns:
        list: A list of dictionaries containing file names and their sizes.
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

# - README.md: file_size=1032 bytes, is_dir=False
# - src: file_size=128 bytes, is_dir=True
# - package.json: file_size=1234 bytes, is_dir=False