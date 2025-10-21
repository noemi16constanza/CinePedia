from base.config.mysqlconection import connectToMySQL
from flask import flash
from datetime import datetime

class Comentario:
    def __init__(self, data):
        self.id = data['id']
        self.contenido = data['contenido']
        self.pelicula_id = data['pelicula_id']
        self.usuario_id = data['usuario_id']
        self.created_at = data['created_at']
        self.usuario = None  # Para almacenar los datos del usuario que comentó

    @classmethod
    def guardar(cls, form):
        query = """
            INSERT INTO comentarios (contenido, pelicula_id, usuario_id, created_at) 
            VALUES (%(contenido)s, %(pelicula_id)s, %(usuario_id)s, NOW());
        """
        return connectToMySQL('esquema_t').query_db(query, form)

    @classmethod
    def obtener_por_pelicula(cls, pelicula_id):
        query = """
            SELECT c.*, u.nombre, u.apellido 
            FROM comentarios c 
            JOIN usuarios u ON c.usuario_id = u.id 
            WHERE c.pelicula_id = %(pelicula_id)s 
            ORDER BY c.created_at DESC;
        """
        results = connectToMySQL('esquema_t').query_db(query, {'pelicula_id': pelicula_id})
        comentarios = []
        for row in results:
            comentario = cls(row)
            comentario.usuario = {
                'id': row['usuario_id'],
                'nombre': row['nombre'],
                'apellido': row['apellido']
            }
            comentarios.append(comentario)
        return comentarios

    @classmethod
    def eliminar(cls, id):
        query = "DELETE FROM comentarios WHERE id = %(id)s;"
        return connectToMySQL('esquema_t').query_db(query, {'id': id})

    @classmethod
    def obtener_por_id(cls, id):
        query = "SELECT * FROM comentarios WHERE id = %(id)s;"
        results = connectToMySQL('esquema_t').query_db(query, {'id': id})
        return cls(results[0]) if results else None

    @staticmethod
    def validar(form):
        is_valid = True
        if not form.get('contenido'):
            flash('El comentario no puede estar vacío', 'comentario')
            is_valid = False
        elif len(form['contenido']) < 3:
            flash('El comentario debe tener al menos 3 caracteres', 'comentario')
            is_valid = False
        return is_valid