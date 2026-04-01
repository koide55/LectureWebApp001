def create_app(config_class=None):
    from flask import Flask

    from .config import Config
    from .routes import main_bp

    if config_class is None:
        config_class = Config

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    app.register_blueprint(main_bp)

    return app
