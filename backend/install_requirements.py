import subprocess
import sys
import os

def install_requirements():
    # Correct path for your Blender Python
    blender_python = "/Applications/Blender.app/Contents/Resources/4.2/python/bin/python3.11"
    
    print(f"Using Python at: {blender_python}")
    
    try:
        # Install Flask directly first
        subprocess.check_call([
            blender_python,
            "-m",
            "pip",
            "install",
            "flask"
        ])
        print("Successfully installed Flask")
        
    except Exception as e:
        print(f"Error installing requirements: {e}")

if __name__ == "__main__":
    install_requirements() 