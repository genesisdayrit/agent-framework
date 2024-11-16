import os
import sys
import pyperclip
from pathlib import Path

def get_project_root():
    """Get the project root path from environment variable or try to find it"""
    root_path = os.getenv('PROJECT_ROOT')
    if not root_path:
        # Try to find it by looking for .git directory
        current_path = Path.cwd()
        while current_path != current_path.parent:
            if (current_path / '.git').exists():
                return str(current_path)
            current_path = current_path.parent
        raise ValueError("Could not find project root. Please set PROJECT_ROOT environment variable")
    return root_path

def get_docs_subdirectories():
    """Get all subdirectories in the docs folder"""
    docs_path = Path(get_project_root()) / 'docs'
    if not docs_path.exists():
        raise ValueError("docs directory not found in project root")
    
    subdirs = [d for d in docs_path.iterdir() if d.is_dir()]
    return subdirs

def get_doc_files(subdir):
    """Get all documentation files in the specified subdirectory"""
    path = Path(get_project_root()) / 'docs' / subdir
    files = [f for f in path.iterdir() if f.is_file() and f.suffix in ['.md', '.txt']]
    return files

def display_options(options, show_extensions=False):
    """Display numbered options to the user"""
    for i, option in enumerate(options, 1):
        name = option.name if show_extensions else option.stem
        print(f"{i}. {name}")

def get_user_choice(options, show_extensions=False):
    """Get user's choice either by number or name"""
    while True:
        display_options(options, show_extensions)
        choice = input("\nEnter number or name of your choice: ").strip()
        
        # Try to process as number
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                return options[idx]
        
        # Try to process as name
        for option in options:
            if (show_extensions and choice.lower() == option.name.lower()) or \
               (not show_extensions and choice.lower() == option.stem.lower()):
                return option
        
        print("\nInvalid choice. Please try again.")

def copy_file_contents(file_path):
    """Copy the contents of the file to clipboard"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            pyperclip.copy(content)
            print(f"\nContents of {file_path.name} have been copied to your clipboard!")
    except Exception as e:
        print(f"Error copying file contents: {e}")

def main():
    try:
        print("Welcome to the documentation navigator!\n")
        
        # Get available subdirectories
        print("Available documentation categories:")
        subdirs = get_docs_subdirectories()
        if not subdirs:
            print("No documentation subdirectories found!")
            return
        
        # Let user choose subdirectory
        chosen_subdir = get_user_choice(subdirs)
        print(f"\nYou selected: {chosen_subdir.name}")
        
        # Get available files in chosen subdirectory
        print("\nAvailable documents:")
        files = get_doc_files(chosen_subdir.name)
        if not files:
            print("No documentation files found in this directory!")
            return
        
        # Let user choose file
        chosen_file = get_user_choice(files, show_extensions=False)
        print(f"\nYou selected: {chosen_file.stem}")
        
        # Copy contents to clipboard
        copy_file_contents(chosen_file)
        
    except ValueError as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
