import subprocess
p = subprocess.Popen("python ./framework.py --crash_run_shut 3 2>&1 > output.txt", shell=True)
