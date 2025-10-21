from base.config.mysqlconection import connectToMySQL
from flask import flash
from datetime import datetime

class Pelicula:
    def __init__(self, data):
        self.id = data.get('id')
        self.titulo = data.get('titulo')
        self.sinopsis = data.get('sinopsis')
        self.director = data.get('director', '')
        self.fecha_estreno = data.get('fecha_estreno', '')
        self.usuario_id = data.get('usuario_id')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')
        self.creador = None  # Para almacenar los datos del usuario creador

    @classmethod
    def guardar(cls, form):
        query = """
            INSERT INTO peliculas (titulo, sinopsis, director, fecha_estreno, usuario_id, created_at, updated_at) 
            VALUES (%(titulo)s, %(sinopsis)s, %(director)s, %(fecha_estreno)s, %(usuario_id)s, NOW(), NOW());
        """
        return connectToMySQL('esquema_t').query_db(query, form)

    @classmethod
    def obtener_todas(cls):
        query = """
            SELECT p.*, u.nombre, u.apellido 
            FROM peliculas p 
            JOIN usuarios u ON p.usuario_id = u.id
            ORDER BY p.created_at DESC;
        """
        results = connectToMySQL('esquema_t').query_db(query)
        peliculas = []
        for pelicula in results:
            p = cls(pelicula)
            p.creador = {
                'nombre': pelicula['nombre'],
                'apellido': pelicula['apellido']
            }
            peliculas.append(p)
        return peliculas

    @classmethod
    def obtener_por_id(cls, id):
        query = """
            SELECT p.*, u.nombre, u.apellido 
            FROM peliculas p 
            JOIN usuarios u ON p.usuario_id = u.id 
            WHERE p.id = %(id)s;
        """
        results = connectToMySQL('esquema_t').query_db(query, {'id': id})
        if results:
            pelicula = cls(results[0])
            pelicula.creador = {
                'nombre': results[0]['nombre'],
                'apellido': results[0]['apellido']
            }
            return pelicula
        return None

    @classmethod
    def actualizar(cls, data):
        query = """
            UPDATE peliculas 
            SET titulo = %(titulo)s, sinopsis = %(sinopsis)s, director = %(director)s, fecha_estreno = %(fecha_estreno)s, updated_at = NOW()
            WHERE id = %(id)s;
        """
        return connectToMySQL('esquema_t').query_db(query, data)

    @classmethod
    def eliminar(cls, id):
        query = "DELETE FROM peliculas WHERE id = %(id)s;"
        return connectToMySQL('esquema_t').query_db(query, {'id': id})

    @staticmethod
    def validar(form):
        is_valid = True

        if not form.get('titulo'):
            flash('El título es requerido', 'pelicula')
            is_valid = False
        elif len(form['titulo']) < 3:
            flash('El título debe tener al menos 3 caracteres', 'pelicula')
            is_valid = False

        # Validar si el título ya existe
        query = "SELECT * FROM peliculas WHERE titulo = %(titulo)s"
        results = connectToMySQL('esquema_t').query_db(query, {'titulo': form['titulo']})
        if results:
            flash('Este título de película ya existe', 'pelicula')
            is_valid = False

        if not form.get('sinopsis'):
            flash('La sinopsis es requerida', 'pelicula')
            is_valid = False
        elif len(form['sinopsis']) < 3:
            flash('La sinopsis debe tener al menos 3 caracteres', 'pelicula')
            is_valid = False

        if not form.get('director') or len(form.get('director')) < 3:
            flash('El nombre del director es requerido y debe tener al menos 3 caracteres', 'pelicula')
            is_valid = False

        if not form.get('fecha_estreno'):
            flash('La fecha de estreno es requerida', 'pelicula')
            is_valid = False

        return is_valid