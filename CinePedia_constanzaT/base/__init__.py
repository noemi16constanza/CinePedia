from flask import Flask, render_template
from base.controllers import usuarios_new as usuarios, peliculas
from datetime import datetime

# definir el filtro de fechas
def format_date(value, format='%Y-%m-%d'):
    if isinstance(value, str):
        value = datetime.strptime(value, '%Y-%m-%d')
    return value.strftime(format)

def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DEBUG= True,
    )

    app.register_blueprint(usuarios.bp)
    app.register_blueprint(peliculas.bp)
    app.add_template_filter(format_date, 'format_date')

    @app.route('/')
    def index():
        return render_template('auth.html')

    return app