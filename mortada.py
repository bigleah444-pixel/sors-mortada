import os
import subprocess
import base64


repo_encoded = "aHR0cHM6Ly9naXRodWIuY29tL0FzaHFhbHNt dC9Tb3VyY2UxLmdpdA=="
branch = "main"

def run(cmd):
    print(f" تنفيذ: {cmd}")
    subprocess.run(cmd, shell=True, check=True)

def _run_git_clone():
    print(" جاري تحميل سورس مرتضى ")
    repo_url = base64.b64decode(repo_encoded.replace(" ", "")).decode()
    run(f"git clone -b {branch} {repo_url} source_temp")
    os.chdir("source_temp")

def _install_requirements():
    print(" تثبيت مكاتب مرتضى ")
    run("pip install -r requirements.txt")

def _start_project():
    print(" بدء تشغيل مرتضى")
    # تشغيل server.py في الخلفية ثم main
    run("python3 server.py &")
    run("python3 server.py & python3 main.py")

if __name__ == "__main__":
    _run_git_clone()
    _install_requirements()
    _start_project()
