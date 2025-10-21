from base.config.mysqlconection import connectToMySQL
from flask import flash
import re  # sirve para las expresiones regulares

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class Usuario:
    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def guardar(cls, form):
        query = (
            "INSERT INTO usuarios (nombre, apellido, email, password, created_at, updated_at) "
            "VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password)s, NOW(), NOW());"
        )
        result = connectToMySQL('esquema_t').query_db(query, form)
        return result

    @staticmethod
    def validar_usuarios(form):
        is_valid = True

        # Nombre
        if not form.get('nombre') or len(form.get('nombre')) < 3:
            flash('El nombre debe tener al menos 3 caracteres', "register")
            is_valid = False

        # Apellido
        if not form.get('apellido') or len(form.get('apellido')) < 4:
            flash('El apellido debe tener al menos 4 caracteres', "register")
            is_valid = False

        # Email
        email = form.get('email') or form.get('Email')
        if not email or not EMAIL_REGEX.match(email):
            flash('Correo inválido', "register")
            is_valid = False
        else:
            query = "SELECT * FROM usuarios WHERE email = %(email)s;"
            results = connectToMySQL('esquema_t').query_db(
                query, {'email': email})
            if results and len(results) >= 1:
                flash('Correo ya registrado', 'register')
                is_valid = False

        # Password
        password = form.get('password')
        if not password or len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres', "register")
            is_valid = False

        if password != form.get('confirm'):
            flash('Las contraseñas no coinciden', "register")
            is_valid = False

        return is_valid

        if len(form['nombre']) < 3:
            flash('El nombre debe tener al menos 3 caracteres', "register")
            is_valid = False

        if len(form['apellido']) < 4:
            flash('El apellido debe tener al menos 4 caracteres', "register")
            is_valid = False

        if not EMAIL_REGEX.match(form['email']):
            flash('Correo invàlido', "register")
            is_valid = False

        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        results = connectToMySQL('esquema_t').query_db(query. form)
        if len(results) >= 1:
            flash('Correo ya registrado')
            is_valid = False

        if form['password'] < 6:
            flash('La contraseña debe tener al menos 6 caracteres', "register")
            is_valid = False

        if form['password'] != form['confirm']:
            flash('Las contraseñasno coinciden', "register")
        return is_valid

    # Mètodo para obtener un usuario por su correo electronico
    @classmethod
    def obtener_por_email(cls, form):
        # consultar para obtener el usuario por correo
        query = "SELECT * FROM usuarios Where email = %(email)s"
        results = connectToMySQL('esquema_t').query_db(query, form)
        # si el usuario existe, devolvemos la instancia del usuario
        if len(results) == 1:
            usuario = cls(results[0])
            return usuario
        else:
            return False

    # Mètodo para obtener un usuario por su id

    @classmethod
    def obtener_por_id(cls, id):
        query = "SELECT * FROM usuarios WHERE id = %(id)s"
        data = {'id': id['id'] if isinstance(id, dict) else id}
        results = connectToMySQL('esquema_t').query_db(query, data)

        if results:
            return cls(results[0])
        return None

    # Mètodo para mostrar todos los usuarios de la base de datos

    # Mètodo para eliminar un usuario por su id
    @classmethod
    def borrar(cls, diccionario):
        query = "DELETE FROM usuarios WHERE id = %(id)s"
        result = connectToMySQL('esquema_t'). query_db(query, diccionario)
        return result

    # Mètodo para obtener datos de un usuario por su id

    # Mètodo para actualizar los datos de un usuario
    @classmethod
    def actualizar(cls, formulario):
        query = "UPDATE usuarios SET nombre = %(nombre)s, apellido = %(apellido)s, email=%(email)s WHERE id = %(id)s"
        result = connectToMySQL('esquema_t'). query_db(query, formulario)
        return result

    # Mètodo para obtener todos
