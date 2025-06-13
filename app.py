import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
ruta = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(ruta, 'database', 'app.db')}"
db = SQLAlchemy(app)

# RUTA SIMPLE
@app.route('/')
def home():
    return 'Hola FLASK'

# RUTA CON PARÁMETROS
@app.route('/saludo/<nombre>')
def saludar(nombre):
    return 'Hola ' + nombre + '!'

# RUTA CON MANEJO DE ERRORES
@app.errorhandler(404)
def pagina_no_encontrada(e):
    return 'Cuidado: Error de capa 8!!!', 404

# RUTA DOBLE
@app.route('/usuario')
@app.route('/usuaria')
def doble_ruta():
    return 'Soy el mismo recurso del servidor'

# RUTA POST - Investigar error
@app.route('/formulario', methods=['POST'])
def formulario():
    return 'Soy un formulario'

if __name__ == '__main__':
    app.run(port=3000, debug=True)