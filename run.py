import argparse
import glob
import os
import shutil
import subprocess
import sys
from os.path import dirname, exists, join
from typing import Dict, List

runnable: str = sys.executable


def activate():
    # 判断当前系统是windows还是linux
    if sys.platform == "win32":
        activate_script: str = join("venv", "Scripts", "activate")
    else:
        activate_script: str = join("venv", "bin", "activate")

    if not exists(activate_script):
        subprocess.run(f"{runnable} -m venv venv", shell=True)
    subprocess.run(activate_script, shell=True)


def test(args: str = "all"):
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


def publish():
    subprocess.run("twine upload dist/*", shell=True)
    clean()


def format():
    subprocess.run("isort . && black .", shell=True)


def lint(lint_dir: str = "app", command: str = "all"):
    lint_flake: str = f"flake8  {lint_dir}/ --count --max-line-length=128"
    lint_mypy: str = f"mypy {lint_dir} --follow-imports=skip"
    if command == "all":
        subprocess.run(lint_flake, shell=True)
        subprocess.run(lint_mypy, shell=True)

    if command == "mypy":
        subprocess.run(lint_mypy, shell=True)
    if command == "flake":
        print(lint_flake)
        subprocess.run(lint_flake, shell=True)


def install(packages: List[str]):
    for package in packages:
        subprocess.run(f"pip install {package}", shell=True)


def uninstall(packages: List[str]):
    for package in packages:
        subprocess.run(f"pip uninstall {package} -y", shell=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Project Starter")

    parser.add_argument("-i", "--install", nargs="+", help="Install packages")
    parser.add_argument("-s", "--commands", nargs="+", help="Commands to run")
    # parser.add_argument("-t", "--test", nargs="?", const="all", help="Test the project")
    parser.add_argument("-t", "--test", action="store_true", help="Test the project")
    parser.add_argument("-c", "--clean", action="store_true", help="Clean the project")
    parser.add_argument("-b", "--build", action="store_true", help="Build the project")
    parser.add_argument(
        "-p", "--publish", action="store_true", help="Release the project"
    )
    parser.add_argument(
        "-r", "--refresh", action="store_true", help="Refresh the project"
    )

    parser.add_argument(
        "-m",
        "--mode",
        nargs="?",
        const="prod",
        choices=["dev", "prod"],
        help="Set the mode",
    )
    parser.add_argument(
        "-l",
        "--lint",
        nargs="?",
        const="all",
        choices=["all", "mypy", "flake"],
        help="Lint the project",
    )
    parser.add_argument(
        "-f", "--format", action="store_true", help="Format the project"
    )

    args = parser.parse_args()

    activate()
    if args.install:
        install(args.install)
    if args.commands:
        module = __import__(__name__)
        for command in args.commands:
            if (fn := getattr(module, command)) is None:
                continue
            fn()
    if args.test:
        test()

    if args.clean:
        clean()
    if args.build:
        build()

    if args.publish:
        publish()

    if args.refresh:
        clean()
        build()
        publish()
        test()

    if args.mode:
        print(args.mode)

    if args.lint:
        lint(lint_dir="common_utils", command=args.lint)

    if args.format:
        format()
