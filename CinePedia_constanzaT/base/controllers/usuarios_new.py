import functools
from flask import Blueprint, render_template, request, redirect, session, flash, url_for, g
from flask_bcrypt import Bcrypt
from base.models.usuario import Usuario

bcrypt = Bcrypt()

bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

@bp.route('/registrar', methods=['POST'])
def registrar():
    if not Usuario.validar_usuarios(request.form):
        return redirect('/')

    pass_encrypt = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
    form = {
        'nombre': request.form['nombre'],
        'apellido': request.form['apellido'],
        'email': request.form['email'],
        'password': pass_encrypt
    }

    nuevo_id = Usuario.guardar(form)
    session['usuario_id'] = nuevo_id
    flash('Usuario registrado exitosamente', 'success')
    return redirect(url_for('usuarios.dashboard'))

@bp.route('/login', methods=['POST'])
def login():
    usuario = Usuario.obtener_por_email({'email': request.form['email']})
    
    if not usuario or not bcrypt.check_password_hash(usuario.password, request.form['password']):
        flash('Email o contraseña incorrectos', 'error')
        return redirect('/')
    
    session['usuario_id'] = usuario.id
    return redirect(url_for('usuarios.dashboard'))

@bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@bp.route('/dashboard')
def dashboard():
    if 'usuario_id' not in session:
        return redirect('/')
    
    usuario = Usuario.obtener_por_id({'id': session['usuario_id']})
    if usuario is None:
        session.clear()
        return redirect('/')
    
    return render_template('dashboard.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('usuario_id')
    
    if user_id is None:
        g.user = None
    else:
        g.user = Usuario.obtener_por_id({'id': user_id})