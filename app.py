import os
from flask import Flask, jsonify, render_template, redirect, url_for, request, flash, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

ruta = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(ruta, 'database', 'app.db')}"
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = 'ñ'

class Album(db.Model):
    __tablename__ = 'albums'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(50))
    artista = db.Column(db.String(50))
    fecha_lanzamiento = db.Column(db.String(10))

@app.route('/')
def home():
    confirmacion = request.args.get('confirmacion')
    error = request.args.get('error')

    try:
        albums = Album.query.all()
        return render_template('formulario.html', confirmacion=confirmacion, error=error, albums=albums)

    except Exception as e:
        print(f'Error al consultar: {e}')
        return render_template('formulario.html', confirmacion=confirmacion, error=error, albums=[])

@app.route('/consulta')
def consulta():
    albums = Album.query.all()
    return render_template('consulta.html', albums=albums)

# RUTA CON MANEJO DE ERRORES
@app.errorhandler(404)
def pagina_no_encontrada(e):
    return 'Cuidado: Error de capa 8!!!', 404

# Ruta para checar conexión
@app.route('/dbcheck')
def db_check():
    try:
        db.session.execute(text('SELECT 1'))  
        return jsonify({'status': 'ok', 'message': 'Conectado con exito'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error de conexion: {str(e)}'}), 500

@app.route('/album', methods=['POST'])
def crear_album():
    album = Album(titulo=request.form.get('titulo', '').strip(), 
                  artista=request.form.get('artista', '').strip(), 
                  fecha_lanzamiento=request.form.get('fecha', '').strip())
    try:
        db.session.add(album)
        db.session.commit()
        flash('Álbum insertado correctamente', 'ok')
        return redirect(url_for('home'))     
    except Exception as e:
        flash(f'Ocurrión un error {e}', 'error')
        return redirect(url_for('home'))

@app.route('/albums/<int:id>', methods=['GET'])
def eliminar_album(id):
    album = Album.query.get_or_404(id)
    try:
        db.session.delete(album)
        db.session.commit()
        flash('Album eliminado correctamente')
        return redirect(url_for('home'))
    except Exception as e:
        flash(f'Error: {e}')
        return redirect(url_for('home'))
    
@app.route('/detalles/<id>')
def detalles(id):
    try:
        album = Album.query.get_or_404(id)
        return render_template('consulta.html', album=album)
    except Exception as e:
        print(f'Error al consultar el album: {e}')
        return render_template('consulta.html', album=[])

if __name__ == '__main__':
    app.run(port=3000, debug=True)