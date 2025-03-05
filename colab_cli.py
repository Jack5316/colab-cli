#!/usr/bin/env python3
"""
colab-cli - A command-line interface for interacting with Google Colab notebooks.
"""

import argparse
import os
import sys
import webbrowser
import json
import requests
from pathlib import Path
import subprocess
from typing import Optional, List

class ColabCLI:
    """Google Colab command-line interface."""
    
    def __init__(self):
        self.config_dir = Path.home() / '.colab-cli'
        self.config_file = self.config_dir / 'config.json'
        self.recent_notebooks = self.config_dir / 'recent.json'
        self._ensure_config_exists()
        
    def _ensure_config_exists(self):
        """Ensure configuration directory and files exist."""
        self.config_dir.mkdir(exist_ok=True)
        
        if not self.config_file.exists():
            with open(self.config_file, 'w') as f:
                json.dump({
                    "default_drive_folder": "",
                    "browser_path": "",
                    "auth_token": ""
                }, f, indent=2)
                
        if not self.recent_notebooks.exists():
            with open(self.recent_notebooks, 'w') as f:
                json.dump([], f, indent=2)
    
    def load_config(self):
        """Load configuration from the config file."""
        with open(self.config_file, 'r') as f:
            return json.load(f)
    
    def save_config(self, config):
        """Save configuration to the config file."""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def get_recent_notebooks(self):
        """Get list of recently accessed notebooks."""
        try:
            with open(self.recent_notebooks, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def add_recent_notebook(self, path):
        """Add a notebook to the recent list."""
        recent = self.get_recent_notebooks()
        
        # Remove if it exists already
        recent = [nb for nb in recent if nb != path]
        
        # Add to the front of the list
        recent.insert(0, path)
        
        # Keep only the latest 10
        recent = recent[:10]
        
        with open(self.recent_notebooks, 'w') as f:
            json.dump(recent, f, indent=2)
    
    def notebook_open(self, path: str, new_tab: bool = True):
        """Open a notebook in Google Colab."""
        path = os.path.abspath(os.path.expanduser(path))
        
        if not os.path.exists(path):
            print(f"Error: Notebook '{path}' not found")
            return False
            
        # Construct the Colab URL
        if path.startswith(str(Path.home() / 'Google Drive')):
            # Handle Google Drive paths
            relative_path = os.path.relpath(path, str(Path.home() / 'Google Drive'))
            colab_url = f"https://colab.research.google.com/drive/{relative_path}"
        else:
            # Upload to Colab directly
            colab_url = "https://colab.research.google.com/notebook#fileId=upload"
            print(f"Will upload local notebook: {path}")
            # Note: This just opens the upload page. User will still need to select the file.
        
        # Open in browser
        print(f"Opening notebook in Colab: {os.path.basename(path)}")
        webbrowser.open(colab_url, new=2 if new_tab else 1)
        
        # Add to recent notebooks
        self.add_recent_notebook(path)
        return True
    
    def notebook_list(self, count: int = 10):
        """List recent notebooks."""
        recent = self.get_recent_notebooks()[:count]
        if not recent:
            print("No recent notebooks found")
            return
            
        print("Recent notebooks:")
        for i, path in enumerate(recent, 1):
            print(f"{i}. {path}")
    
    def notebook_download(self, url_or_id: str, output_path: Optional[str] = None):
        """Download a notebook from Colab."""
        # Extract ID if full URL is provided
        if url_or_id.startswith('https://colab.research.google.com/'):
            # Extract the ID from the URL
            parts = url_or_id.split('/')
            if 'drive' in parts:
                drive_index = parts.index('drive')
                if drive_index + 1 < len(parts):
                    notebook_id = parts[drive_index + 1]
            else:
                print("Error: Could not extract notebook ID from URL")
                return False
        else:
            notebook_id = url_or_id
        
        if not output_path:
            output_path = f"colab_notebook_{notebook_id}.ipynb"
        
        # For authenticated download, we'd need the user's Google auth token
        # This is just a placeholder for the command, actual implementation would be more complex
        print(f"Downloading notebook {notebook_id} to {output_path}")
        print("Note: Full download functionality requires Google authentication")
        print(f"Visit: https://colab.research.google.com/drive/{notebook_id}")
        print(f"Then use File > Download > .ipynb to save the notebook")
        
        return True
    
    def config_set(self, key: str, value: str):
        """Set a configuration value."""
        config = self.load_config()
        if key not in config:
            print(f"Error: Unknown configuration key: {key}")
            print(f"Valid keys: {', '.join(config.keys())}")
            return False
            
        config[key] = value
        self.save_config(config)
        print(f"Configuration updated: {key} = {value}")
        return True
    
    def config_get(self, key: Optional[str] = None):
        """Get configuration value(s)."""
        config = self.load_config()
        
        if key:
            if key not in config:
                print(f"Error: Unknown configuration key: {key}")
                print(f"Valid keys: {', '.join(config.keys())}")
                return False
            print(f"{key} = {config[key]}")
        else:
            print("Current configuration:")
            for k, v in config.items():
                if k == 'auth_token' and v:
                    print(f"{k} = ***********")
                else:
                    print(f"{k} = {v}")
        
        return True

def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description="Google Colab CLI")
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # notebook commands
    notebook_parser = subparsers.add_parser('notebook', help='Notebook operations')
    notebook_subparsers = notebook_parser.add_subparsers(dest='notebook_command')
    
    # notebook open
    open_parser = notebook_subparsers.add_parser('open', help='Open a notebook in Colab')
    open_parser.add_argument('path', help='Path to the notebook file')
    open_parser.add_argument('--new-window', action='store_false', dest='new_tab', 
                           help='Open in new window instead of new tab')
    
    # notebook list
    list_parser = notebook_subparsers.add_parser('list', help='List recent notebooks')
    list_parser.add_argument('-n', '--count', type=int, default=10, 
                           help='Number of notebooks to list')
    
    # notebook download
    download_parser = notebook_subparsers.add_parser('download', help='Download a notebook from Colab')
    download_parser.add_argument('url_or_id', help='Colab URL or notebook ID')
    download_parser.add_argument('-o', '--output', help='Output file path')
    
    # config commands
    config_parser = subparsers.add_parser('config', help='Configuration operations')
    config_subparsers = config_parser.add_subparsers(dest='config_command')
    
    # config set
    set_parser = config_subparsers.add_parser('set', help='Set a configuration value')
    set_parser.add_argument('key', help='Configuration key')
    set_parser.add_argument('value', help='Configuration value')
    
    # config get
    get_parser = config_subparsers.add_parser('get', help='Get configuration value(s)')
    get_parser.add_argument('key', nargs='?', help='Configuration key (optional)')
    
    args = parser.parse_args()
    cli = ColabCLI()
    
    if args.command == 'notebook':
        if args.notebook_command == 'open':
            cli.notebook_open(args.path, args.new_tab)
        elif args.notebook_command == 'list':
            cli.notebook_list(args.count)
        elif args.notebook_command == 'download':
            cli.notebook_download(args.url_or_id, args.output)
        else:
            notebook_parser.print_help()
    elif args.command == 'config':
        if args.config_command == 'set':
            cli.config_set(args.key, args.value)
        elif args.config_command == 'get':
            cli.config_get(args.key)
        else:
            config_parser.print_help()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()