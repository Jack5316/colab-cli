# Colab CLI Examples

## Basic Usage

### Opening a notebook

```bash
# Open a notebook from your local machine
colab-cli notebook open ~/Documents/MyNotebook.ipynb

# Open a notebook from Google Drive (if mounted)
colab-cli notebook open ~/Google\ Drive/Colab\ Notebooks/Analysis.ipynb
```

### Recent notebooks

```bash
# List recent notebooks
colab-cli notebook list

# Open the most recent notebook (combining with other tools)
RECENT_NB=$(colab-cli notebook list | grep -m 1 -o "/.*\.ipynb")
colab-cli notebook open "$RECENT_NB"
```

### Configuration

```bash
# Set your preferred Google Drive folder for notebooks
colab-cli config set default_drive_folder "Colab Notebooks"

# Check your current configuration
colab-cli config get
```

## Integration with other tools

### Creating a new notebook and opening it

```bash
# Create a new notebook and open it in Colab
touch new_analysis.ipynb
echo '{"cells":[],"metadata":{"colab":{"name":"new_analysis.ipynb"}},"nbformat":4,"nbformat_minor":0}' > new_analysis.ipynb
colab-cli notebook open new_analysis.ipynb
```

### Batch processing

```bash
# Open all notebooks in a directory
for nb in *.ipynb; do
    colab-cli notebook open "$nb"
    sleep 2  # Wait a bit between opening each notebook
done
```

### Creating aliases for common operations

Add these to your `~/.bashrc` or `~/.zshrc`:

```bash
# Quick open notebook
alias colab-open="colab-cli notebook open"

# List recent notebooks
alias colab-recent="colab-cli notebook list"

# Open most recent notebook
alias colab-last="colab-cli notebook open \$(colab-cli notebook list | grep -m 1 -o '/.*\.ipynb')"
```