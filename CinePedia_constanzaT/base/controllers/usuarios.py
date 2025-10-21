import functools  # sirve para decorar funciones
# sirve para crear rutas
from flask import Flask, Blueprint, render_template, request, redirect, session, flash, url_for, g
from flask_bcrypt import Bcrypt
from datetime import datetime, date
from base.models.usuario import Usuario

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

bcrypt = Bcrypt()  # sirve para encriptar contraseñas

# sirve para agrupoar rutas relacionadas con los usuarios.
bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')


@bp.route('/registrar', methods=['POST'])
def registrar():
    if not Usuario.validar_usuarios(request.form):
        return redirect('/')

    pass_encrypt = bcrypt.generate_password_hash(
        request.form['password']).decode('utf-8')

    form = {
        'nombre': request.form.get('nombre'),
        'apellido': request.form.get('apellido'),
        'email': request.form.get('email') or request.form.get('Email'),
        'password': pass_encrypt
    }

    nuevo_id = Usuario.guardar(form)
    session['usuario_id'] = nuevo_id
    flash('¡Usuario registrado exitosamente!', 'success')
    return redirect(url_for('usuarios.dashboard'))


@bp.route('/dashboard')
def dashboard():
    if 'usuario_id' not in session:
        return redirect('/')

    form = {"id": session['usuario_id']}
    usuario = Usuario.obtener_por_id(form)
    return render_template('dashboard.html', usuario=usuario)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form_data = request.form
    data = {'email': form_data.get('email') or form_data.get('Email')}
    usuario = Usuario.obtener_por_email(data)
    if not usuario:
        flash('Usuario o Contraseña incorrecta', "login")
        return redirect('/')

    if not bcrypt.check_password_hash(usuario.password, form_data['password']):
        flash("Contraseña incorrecta", "login")
        return redirect('/')

    session['usuario_id'] = usuario.id
    return redirect(url_for('usuarios.dashboard'))


@bp.before_app_request
def cargar_usuario_logueado():
    usuario_id = session.get('usuario_id')
    if usuario_id is None:
        g.user = None
    else:
        # Obtener usuario por idy almacenarlo en 'G.user'
        g.user = Usuario.obtener_por_id({'id': usuario_id})


def login_requerido(view):
    @functools.wraps(view)
    def vista_envuelta(**kwargs):
        if g.user is None:
            # No hay usuario logueado, redirigir al login
            return redirect(url_for('usuario.login'))
        # Usuario logueado, permite acceso a las vistas
        return view(**kwargs)

    return vista_envuelta


@bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')
