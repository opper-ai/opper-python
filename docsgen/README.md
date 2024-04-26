# DocsGen

DocsGen is a Python tool designed to automatically generate documentation for the OpperAI service's API methods. It imports the opperai python SDK, extracts docstrings from the code, formats them into structured documentation in MDX format, and also outputs a JSON representation of the documentation elements.

## Features

- **Automatic Documentation Generation**: Converts docstrings into MDX and JSON formats.
- **Support for Async Operations**: Utilizes Python's asyncio for efficient documentation generation.
- **Integration with OpperAI**: Designed to work seamlessly with the OpperAI service's API.

## Requirements

- Python 3.8+
- Pydantic
- asyncio

## Installation

Clone the repository and install the required Python packages:

``` bash
git clone https://your-repository-url.git
cd docsgen
pip install -r requirements.txt
```

## Usage

``` bash
python docsgen.py
```

This will generate documentation for all methods in the `client.functions`, `client.indexes`, and `client.spans` modules of the OpperAI client.

## Output

- **MDX Files**: Generated in the `docs.mdx` file.
- **JSON Files**: Documentation elements are also saved in `docs.json` for further processing or integration.

## Todo

- Figure out how to run 
- Make modulular so its possible to do this on the typescript SDK
- ??? 

This README provides a clear overview of the project, its features, how to set it up, use it, and contribute to it. Adjust the repository URL and any specific details as necessary for your project.