import os
from webapp import create_app
from webapp.cli import register

# Get config Class for app and create app
env = os.environ.get("WEBAPP_ENV", "dev")
app = create_app(f"config.{env.capitalize()}Config")
register(app)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000, threaded=True)
