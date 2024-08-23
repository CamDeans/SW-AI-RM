# dev_setup.py

import subprocess
import os
import sys

def run_command_in_new_terminal(command, working_directory):
    if sys.platform.startswith('win'):
        # For Windows
        full_command = f'cd /d {working_directory} && {command}'
        subprocess.Popen(['start', 'cmd', '/k', full_command], shell=True)
    elif sys.platform.startswith('darwin'):
        # For macOS
        apple_script = f'''
        tell application "Terminal"
            do script "cd {working_directory} && {command}"
        end tell
        '''
        subprocess.run(['osascript', '-e', apple_script])
    elif sys.platform.startswith('linux'):
        # For Linux (assuming GNOME Terminal)
        subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', f'cd {working_directory} && {command}; exec bash'])
    else:
        print(f"Unsupported operating system: {sys.platform}")
        sys.exit(1)

def main():
    # Get the project root directory (where this script is located)
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    # Frontend setup
    frontend_dir = os.path.join(project_root, 'frontend')
    frontend_command = 'npm start'
    run_command_in_new_terminal(frontend_command, frontend_dir)
    
    # Backend setup
    backend_dir = os.path.join(project_root, 'backend')
    backend_command = 'venv\\Scripts\\activate && flask run'
    run_command_in_new_terminal(backend_command, backend_dir)

if __name__ == "__main__":
    main()