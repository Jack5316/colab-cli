# Colab CLI

A command-line interface for interacting with Google Colab notebooks from your terminal.

## Installation

```bash
# Clone the repository (or download the files)
git clone https://github.com/yourusername/colab-cli.git
cd colab-cli

# Install the package
pip install -e .

# This makes the `colab-cli` command available in your terminal
```

## Usage

### Opening a notebook

```bash
# Open a local notebook in Colab
colab-cli notebook open path/to/your/notebook.ipynb

# Open in a new window instead of a new tab
colab-cli notebook open path/to/your/notebook.ipynb --new-window
```

### Listing recent notebooks

```bash
# List the 10 most recently opened notebooks
colab-cli notebook list

# List only the 5 most recent notebooks
colab-cli notebook list -n 5
```

### Configuration

```bash
# View all configuration settings
colab-cli config get

# View a specific configuration setting
colab-cli config get default_drive_folder

# Set a configuration value
colab-cli config set default_drive_folder "My Colab Notebooks"
```

## Features

- Open local notebooks in Google Colab
- Track recently opened notebooks
- Configurable settings
- Command-line interface for easy scripting

## Requirements

- Python 3.6+
- Internet connection to access Google Colab

## Limitations

- Some operations like downloading notebooks directly require Google authentication
- For uploading local notebooks, the tool opens the Colab upload page and you still need to select the file manually