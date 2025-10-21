from flask import Blueprint, render_template, request, redirect, session, flash, url_for, g
from base.models.pelicula import Pelicula
from base.models.usuario import Usuario
from base.models.comentario import Comentario
from functools import wraps

bp = Blueprint('peliculas', __name__, url_prefix='/peliculas')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            return redirect(url_for('usuarios.login'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/')
def index():
    peliculas = Pelicula.obtener_todas()
    return render_template('peliculas/index.html', peliculas=peliculas)

@bp.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    if request.method == 'POST':
        if not Pelicula.validar(request.form):
            return render_template('peliculas/crear.html', pelicula=request.form)
        
        form = {
            'titulo': request.form['titulo'],
            'sinopsis': request.form['sinopsis'],
            'director': request.form['director'],
            'fecha_estreno': request.form['fecha_estreno'],
            'usuario_id': session['usuario_id']
        }
        
        Pelicula.guardar(form)
        flash('Película creada exitosamente', 'success')
        return redirect(url_for('peliculas.index'))
    
    return render_template('peliculas/crear.html')

@bp.route('/<int:id>')
def ver(id):
    pelicula = Pelicula.obtener_por_id(id)
    if pelicula is None:
        flash('Película no encontrada', 'error')
        return redirect(url_for('peliculas.index'))
    
    comentarios = Comentario.obtener_por_pelicula(id)
    return render_template('peliculas/ver.html', pelicula=pelicula, comentarios=comentarios)

@bp.route('/<int:id>/comentar', methods=['POST'])
@login_required
def comentar(id):
    pelicula = Pelicula.obtener_por_id(id)
    if pelicula is None:
        flash('Película no encontrada', 'error')
        return redirect(url_for('peliculas.index'))
    
    # Verificar que el usuario no sea el creador de la película
    if pelicula.usuario_id == session['usuario_id']:
        flash('No puedes comentar tu propia película', 'error')
        return redirect(url_for('peliculas.ver', id=id))
    
    if not Comentario.validar(request.form):
        return redirect(url_for('peliculas.ver', id=id))
    
    form = {
        'contenido': request.form['contenido'],
        'pelicula_id': id,
        'usuario_id': session['usuario_id']
    }
    
    Comentario.guardar(form)
    flash('Comentario agregado exitosamente', 'success')
    return redirect(url_for('peliculas.ver', id=id))

@bp.route('/comentarios/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_comentario(id):
    comentario = Comentario.obtener_por_id(id)
    if comentario is None:
        flash('Comentario no encontrado', 'error')
        return redirect(url_for('peliculas.index'))
    
    if comentario.usuario_id != session['usuario_id']:
        flash('No tienes permiso para eliminar este comentario', 'error')
        return redirect(url_for('peliculas.ver', id=comentario.pelicula_id))
    
    Comentario.eliminar(id)
    flash('Comentario eliminado exitosamente', 'success')
    return redirect(url_for('peliculas.ver', id=comentario.pelicula_id))

@bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar(id):
    pelicula = Pelicula.obtener_por_id(id)
    
    if pelicula is None:
        flash('Película no encontrada', 'error')
        return redirect(url_for('peliculas.index'))
    
    if pelicula.usuario_id != session['usuario_id']:
        flash('No tienes permiso para editar esta película', 'error')
        return redirect(url_for('peliculas.index'))
    
    if request.method == 'POST':
        if not Pelicula.validar(request.form):
            # Pasar los datos del formulario y el id de la película, usando .get() para evitar KeyError
            form_data = {
                'id': id,
                'titulo': request.form.get('titulo', ''),
                'sinopsis': request.form.get('sinopsis', ''),
                'director': request.form.get('director', ''),
                'fecha_estreno': request.form.get('fecha_estreno', '')
            }
            return render_template('peliculas/editar.html', pelicula=form_data)
        
        form = {
            'id': id,
            'titulo': request.form['titulo'],
            'sinopsis': request.form['sinopsis'],
            'director': request.form['director'],
            'fecha_estreno': request.form['fecha_estreno']
        }
        
        Pelicula.actualizar(form)
        flash('Película actualizada exitosamente', 'success')
        return redirect(url_for('peliculas.ver', id=id))
    
    return render_template('peliculas/editar.html', pelicula=pelicula)

@bp.route('/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar(id):
    pelicula = Pelicula.obtener_por_id(id)
    
    if pelicula is None:
        flash('Película no encontrada', 'error')
        return redirect(url_for('peliculas.index'))
    
    if pelicula.usuario_id != session['usuario_id']:
        flash('No tienes permiso para eliminar esta película', 'error')
        return redirect(url_for('peliculas.index'))
    
    Pelicula.eliminar(id)
    flash('Película eliminada exitosamente', 'success')
    return redirect(url_for('peliculas.index'))