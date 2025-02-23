from flask import Flask
from routes.home import home_bp
from routes.login import login_bp
from routes.profile import profile_bp
from routes.jobs import jobs_bp
from routes.resources import resources_bp

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.register_blueprint(home_bp)
app.register_blueprint(login_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(jobs_bp)
app.register_blueprint(resources_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)