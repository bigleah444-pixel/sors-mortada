import os
import subprocess

# ضع هنا رابط الريبو المباشر (HTTPS)
repo_url = "https://github.com/bigleah444-pixel/sors-mortada.git"
branch = "main"

def run(cmd):
    print(f" تنفيذ: {cmd}")
    subprocess.run(cmd, shell=True, check=True)

def _run_git_clone():
    print(" جاري تحميل سورس مرتضى ")
    run(f"git clone -b {branch} {repo_url} source_temp")
    os.chdir("source_temp")

def _install_requirements():
    print(" تثبيت مكاتب مرتضى ")
    run("pip install -r requirements.txt")

def _start_project():
    print(" بدء تشغيل مرتضى")
    # تشغيل server.py في الخلفية (Linux/Mac) ثم main.py
    run("python3 server.py &")
    run("python3 main.py")

if __name__ == "__main__":
    _run_git_clone()
    _install_requirements()
    _start_project()
