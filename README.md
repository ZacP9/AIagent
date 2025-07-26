# AI Agent

A Python-based AI coding agent that uses Google's Gemini 2.0 Flash model to interact with code repositories through function calling. The agent can analyze code, read files, execute Python scripts, and provide intelligent responses about your codebase.

> **Note**: This project was created as part of the [Boot.dev](https://boot.dev) curriculum.

## Features

- **Interactive Function Calling**: The AI can call functions to explore and analyze your codebase
- **File System Operations**: List directories, read file contents, and write new files
- **Python Script Execution**: Run Python files with arguments and capture output
- **Iterative Problem Solving**: Multi-turn conversations where the AI builds context through function calls
- **Verbose Mode**: Optional detailed logging of AI interactions and token usage
- **Security**: All file operations are constrained to a specified working directory

## Available Functions

The AI agent has access to the following functions:

- `get_files_info(directory)`: List files and directories with sizes
- `get_file_content(file_path)`: Read the contents of a file
- `run_python_file(file_path, args)`: Execute Python scripts with optional arguments
- `write_file(file_path, content)`: Create or overwrite files

## Configuration

Edit `config.py` to customize:

- `MAX_FILE_CONTENT_CHAR`: Maximum characters to read from files (default: 10000)
- `WORKING_DIR`: Directory where the agent can operate (default: "./calculator")
- `MAX_ITERS`: Maximum iterations to prevent infinite loops (default: 20)

## How It Works

1. **User Input**: You provide a question or request via command line
2. **AI Planning**: The Gemini model analyzes your request and decides which functions to call
3. **Function Execution**: The agent executes the necessary functions (reading files, running code, etc.)
4. **Iterative Processing**: The AI reviews function results and may call additional functions
5. **Final Response**: Once the AI has gathered sufficient information, it provides a comprehensive answer

## Security Features

- **Working Directory Constraint**: All file operations are restricted to the configured working directory
- **Path Validation**: Prevents access to files outside the permitted directory
- **Iteration Limits**: Prevents infinite loops with configurable maximum iterations
- **Input Validation**: Validates file types and paths before execution

## Requirements

- Python 3.12+
- google-genai==1.12.1
- Google Gemini API key