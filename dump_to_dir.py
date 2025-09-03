#!/usr/bin/env python3

import os
import sys
import shutil

# Define ANSI color codes
RED = '\033[31m'
GREEN = '\033[32m'
LIGHT_BLUE = '\033[94m'
ORANGE = '\033[38;5;208m'
YELLOW = '\033[33m'
PURPLE = '\033[35m'
RESET = '\033[0m'

USAGE_MESSAGE = f"""
{GREEN}Expected Usage:{RESET}
    Linux/Mac:
        {YELLOW}./dump_to_dir.py <target_dir> <source_dir>{RESET}
    Windows:
        {YELLOW}python dump_to_dir.py <target_dir> <source_dir>{RESET}

This script will move all files from the subdirectories within the source directory
to the root of the target directory.
"""

def check_dependencies():
    """ Checks if a virtual environment is active and required libraries are installed.

    This function verifies that the user is running the script in a
    virtual environment because we do not subscribe to the religion of
    dependency hell. It then attempts to import the necessary
    libraries to ensure all dependencies are met. If a library is
    missing, the script will provide instructions for installation and exit.
    This check can be bypassed with the --force flag

    Returns:
        None: A tuple containing the imported 'shutil' and 'inquirer' modules.

    Raises:
        SystemExit: If the user is not in a virtual environment and
            the --force flag is not used, or if a required library is missing.
    """
    # Check for YOLO
    force_flag = '--force' in sys.argv

    if force_flag:
        sys.argv.remove('--force')
        print(f"May the gods of YOLO by with you: bypassing virtual environment check.")
    
    try:
        import inquirer
    except ImportError as e:
        print(f"{RED}Error{RESET}: A required library is missing: {e.name}")
        print(f"Please install dependencies using: pip install -r requirements.txt")
        sys.exit(1)
    
    if not force_flag and os.getenv('VIRTUAL_ENV') is None:
        print(f"{RED}Warning{RESET}: You are not running in a {GREEN}virtual environment{RESET}.")
        print(f"It is highly recommended to use a {GREEN}virtual environment{RESET} for this script, {PURPLE}modules{RESET} will be checked and installed.\n")

        print(f"To create a virtual environment, run the following commands:")
        print(f"\tpython3 -m venv venv\n")

        print("Activate the virtual environment:")
        print(f"{YELLOW}Linux/Mac:{RESET}")
        print(f"\tsource venv/bin/activate")
        print(f"{YELLOW}Windows:{RESET}")
        print(f"\tvenv\\Scripts\\activate")

        print(f"\nIf you're new to Python and want to learn more about Python {GREEN}virtual environments{RESET}, you can find out more here:")
        print(f"{LIGHT_BLUE}https://docs.python.org/3/library/venv.html{RESET}\n")

        print(f"If you're a veteran Python developer, and you've been through and survived dependency {RED}hell{RESET},")
        print(f"and {ORANGE}YOLO{RESET} is your mantra since you did not read the script or any of the notes before you ran it,")
        print(f"you may force this script with the {YELLOW}--force{RESET} flag.")
        
        sys.exit(1)
        
    return inquirer

# Run dependency checks:
inquirer = check_dependencies()

# Check if the target and source directories are provided and valid.
if len(sys.argv) == 1:
    print(USAGE_MESSAGE)
    print(f"{YELLOW}No directories provided.{RESET}\nHow would you like to proceed?")
    questions = [
        inquirer.List(
            "default_action",
            message="",
            choices=[
                "Use script's location (flatten in place)", "Exit"
            ],
        ),
    ]
    answers = inquirer.prompt(questions)

    if answers["default_action"] == "Exit":
        print(f"{RED}Exiting...{RESET}")
        sys.exit(0)
    else:
        target_dir = os.path.dirname(os.path.abspath(__file__))
        source_dir = os.path.dirname(os.path.abspath(__file__))

elif len(sys.argv) == 3:
    target_dir = sys.argv[1]
    source_dir = sys.argv[2]
else:
    print(f"{USAGE_MESSAGE}")
    sys.exit(1)

if not os.path.isdir(target_dir):
    print(f"{RED}Error{RESET}: Target directory does not exist.")
    sys.exit(1)

if not os.path.isdir(source_dir):
    print(f"{RED}Error{RESET}: Source directory does not exist.")
    sys.exit(1)

    target_dir = os.path.abspath(target_dir)
    source_dir = os.path.abspath(source_dir)

print(f"{GREEN}Source Directory:{RESET} {source_dir}")
print(f"{GREEN}Target Directory:{RESET} {target_dir}\n")
print(f"Continue?")
# Confirm action with the user.
questions = [
    inquirer.Confirm(
        "confirm",
        message=f"",
    )
]
answers = inquirer.prompt(questions)

if not answers["confirm"]:
    print(f"{RED}Operation cancelled by user.{RESET}")
    sys.exit(0)

subdirs = [d for d in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, d))]
