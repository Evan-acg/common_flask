def run_flask():
    import sys
    from os.path import abspath, dirname

    from common_utils.core.scaffold import Flask

    sys.path.append(dirname(dirname(abspath(__file__))))
    app: Flask = Flask(__name__, controller_scan_dir="test_data.app.modules")
    options = {
        "port": app.config["PORT"],
        "host": app.config["HOST"],
        "debug": app.config["DEBUG"],
    }
    app.run(**options)


if __name__ == "__main__":
    run_flask()
