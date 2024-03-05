import glob
import os
import shutil
import subprocess
import sys
from os.path import dirname, exists, join
from typing import Dict, List

runnable: str = sys.executable


# 判断当前系统是windows还是linux
if sys.platform == "win32":
    activate_script: str = join("venv", "Scripts", "activate")
else:
    activate_script: str = join("venv", "bin", "activate")

if not exists(activate_script):
    print("Virtual environment not found. Creating...")
else:
    print("Virtual environment found. Activating...")


def activate():
    print("Activating virtual environment...")
    subprocess.run(activate_script, shell=True)


def test():
    subprocess.run(f"{runnable} -m pytest -v -s ", shell=True)


def clean():
    # 删除某个文件夹
    pwd: str = dirname(__file__)
    shutil.rmtree(join(pwd, "build"), ignore_errors=True)
    shutil.rmtree(join(pwd, "dist"), ignore_errors=True)
    for file in os.listdir("."):
        if file.endswith(".egg-info"):
            shutil.rmtree(file, ignore_errors=True)
    subprocess.run("pip uninstall -y common_flask_utils", shell=True)


def build():
    clean()
    subprocess.run("python setup.py sdist bdist_wheel", shell=True)
    for file in glob.glob("dist/*.whl"):
        subprocess.run(f"pip install {file}", shell=True)
    test()


def release():
    subprocess.run("twine upload dist/*", shell=True)
    clean()


def main(commands: List[str]):
    actions: Dict[str, callable] = {
        "clean": clean,
        "test": test,
        "build": build,
        "release": release,
    }

    activate()
    for command in commands:
        if not command in actions:
            continue
        actions[command]()


if __name__ == "__main__":
    print("Running...")
    if len(sys.argv) == 1:
        print("No command provided. Exiting...")
        sys.exit(1)
    
    commands: List[str] = sys.argv[1:]
    main(commands)
