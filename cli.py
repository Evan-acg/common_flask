import glob
import os
import shutil
import subprocess
import sys
from os.path import dirname, exists, join
from typing import Dict

import click


class Payload:
    def __init__(self) -> None:
        self.verbose: bool = True
        self.module_dir: str = "common_utils"


payload = click.make_pass_decorator(Payload, ensure=True)


def activate():
    # 判断当前系统是windows还是linux
    if sys.platform == "win32":
        activate_script: str = join("venv", "Scripts", "activate")
    else:
        activate_script: str = join("venv", "bin", "activate")

    if not exists(activate_script):
        subprocess.run(f"python -m venv venv", shell=True)
    subprocess.run(activate_script, shell=True)
    print(f"activate venv {sys.executable}")


@click.group()
@payload
def main(ctx):
    activate()


@main.command()
def test():
    """使用pytest进行测试"""
    command: str = "python -m pytest -v -s"
    subprocess.run(command, shell=True)


@main.command()
@click.option(
    "-l",
    "--lint",
    default="all",
    required=True,
    type=click.Choice(["all", "flake", "mypy"]),
)
@click.pass_context
def lint(ctx, lint, *args, **kwargs):
    """使用flake8和mypy进行代码检查"""
    commands: Dict[str, str] = {
        "flake": f"flake8  {ctx.obj.module_dir}/ --count --max-line-length=128",
        "mypy": f"mypy {ctx.obj.module_dir} --follow-imports=skip",
    }
    if "all" == lint:
        for command in commands.values():
            subprocess.run(command, shell=True)

    elif lint in commands:
        subprocess.run(commands[lint], shell=True)

    else:
        raise ValueError(f"unknown lint command {lint}")


@main.command()
@click.pass_context
def format(ctx):
    """使用isort和black进行代码格式化"""
    commands = [
        f"isort {ctx.obj.module_dir}",
        f"black {ctx.obj.module_dir}",
    ]
    for command in commands:
        subprocess.run(command, shell=True)


@main.command()
def clean():
    """清理构建文件和缓存文件"""
    pwd: str = dirname(__file__)
    shutil.rmtree(join(pwd, "build"), ignore_errors=True)
    shutil.rmtree(join(pwd, "dist"), ignore_errors=True)
    for file in os.listdir("."):
        if file.endswith(".egg-info"):
            shutil.rmtree(file, ignore_errors=True)
    subprocess.run("pip uninstall -y common_flask_utils", shell=True)


@main.command()
@click.pass_context
def build(ctx):
    """构建项目并安装到当前环境中"""
    ctx.invoke(clean)
    ctx.invoke(test)
    subprocess.run("python setup.py sdist bdist_wheel", shell=True)
    for file in glob.glob("dist/*.whl"):
        subprocess.run(f"pip install {file}", shell=True)


@main.command()
@click.pass_context
def publish(ctx):
    """发布项目到pypi"""
    subprocess.run("twine upload dist/*", shell=True)
    ctx.invoke(clean)


@main.command()
@click.argument("i", nargs=-1)
@click.argument("u", nargs=-1)
def deps(i, u):
    """安装或卸载依赖包"""
    if i:
        command: str = f"pip install {' '.join(i)}"
        subprocess.run(command, shell=True)
    if u:
        command: str = f"pip uninstall {' '.join(u)} -y"
        subprocess.run(command, shell=True)


@main.command()
@click.option("-p", "--port", default=None, help="端口号")
@click.option("-h", "--host", default=None, help="主机地址")
@click.option("-d", "--debug", default=None, help="开发模式")
def run(port, host, debug):
    """运行flask应用"""
    from common_utils.core.scaffold import Flask

    sys.path.insert(0, dirname(dirname(__file__)))
    app: Flask = Flask(__name__, controller_scan_dir="test_data.app.modules")
    options: Dict[str, str | int | bool] = {
        "port": port or app.config["PORT"],
        "host": host or app.config["HOST"],
        "debug": debug or app.config["DEBUG"],
    }

    app.run(**options)


@main.command()
@click.pass_context
def refresh(ctx):
    """刷新项目"""
    ctx.invoke(clean)
    ctx.invoke(build)


if __name__ == "__main__":
    main()
