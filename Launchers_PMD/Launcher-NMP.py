# /////////////////////////////////////////////
# ///////////// NMP Launcher //////////////////
# /////////////////////////////////////////////

import subprocess
import sys
import os

try:
    script_path = os.path.join(os.path.dirname(__file__), "NMP.py")
    subprocess.run([sys.executable, "-m", "streamlit", "run", script_path], check=True)
except subprocess.CalledProcessError as e:
    print(f"An error occurred while running the script: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")