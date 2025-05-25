import os
import subprocess
import sys

def compile_resources():
    # Get the directory of this script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Compile resources
    print("Compiling resources...")
    subprocess.run([
        'pyrcc5',
        os.path.join(current_dir, 'resources.qrc'),
        '-o',
        os.path.join(current_dir, 'resources_rc.py')
    ])
    
    # Compile UI
    print("Compiling UI...")
    subprocess.run([
        'pyuic5',
        os.path.join(current_dir, 'consulta_dialog.ui'),
        '-o',
        os.path.join(current_dir, 'ui_consulta_dialog.py')
    ])
    
    print("Compilation completed successfully!")

if __name__ == '__main__':
    compile_resources() 