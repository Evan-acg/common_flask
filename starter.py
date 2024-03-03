def run_flask():
    import sys
    from os.path import abspath, dirname

    from common_utils.core.scaffold import Flask
    from common_utils.utils.blueprint_util import blueprint_register
    from common_utils.utils.logger_util import logger_register

    sys.path.append(dirname(dirname(abspath(__file__))))
    app: Flask = Flask(__name__)
    blueprint_register(app, "test_data.app.modules", url_prefix="/api")
    logger_register()

    @app.get("/urls")
    def urls():
        return [rule.rule for rule in app.url_map.iter_rules()]

    app.run(debug=True)


if __name__ == "__main__":
    run_flask()
