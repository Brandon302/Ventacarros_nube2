import os
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()

app = Flask(__name__)

# Configuración de la base de datos PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definición de la tabla Carros
class Carro(db.Model):
    __tablename__ = 'carros'
    no_placas = db.Column(db.String, primary_key=True)
    marca = db.Column(db.String)
    modelo = db.Column(db.String)
    kilometros = db.Column(db.Integer)

# Crear tablas automáticamente si no existen
with app.app_context():
    db.create_all()

# Ruta principal para mostrar todos los carros
@app.route('/')
def index():
    carros = Carro.query.all()
    return render_template('index.html', carros=carros)

# Ruta para crear un nuevo carro
@app.route('/carros/new', methods=['GET', 'POST'])
def create_carro():
    if request.method == 'POST':
        no_placas = request.form['no_placas']
        marca = request.form['marca']
        modelo = request.form['modelo']
        kilometros = request.form['kilometros']

        nvo_carro = Carro(
            no_placas=no_placas,
            marca=marca,
            modelo=modelo,
            kilometros=kilometros
        )

        db.session.add(nvo_carro)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('create_carro.html')

# Ruta para eliminar un carro
@app.route('/carros/delete/<string:no_placas>')
def delete_carro(no_placas):
    carro = Carro.query.get(no_placas)
    if carro:
        db.session.delete(carro)
        db.session.commit()
    return redirect(url_for('index'))

# Ruta para actualizar un carro
@app.route('/carros/update/<string:no_placas>', methods=['GET', 'POST'])
def update_carro(no_placas):
    carro = Carro.query.get(no_placas)

    if request.method == 'POST':
        carro.marca = request.form['marca']
        carro.modelo = request.form['modelo']
        carro.kilometros = request.form['kilometros']
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('update_carro.html', carro=carro)

if __name__ == '__main__':
    app.run(debug=True)
