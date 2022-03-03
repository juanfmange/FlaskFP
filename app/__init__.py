#from crypt import methods
#from django.shortcuts import redirect
from flask import Flask, flash, render_template, request, redirect, url_for, jsonify
from flask_wtf.csrf import CSRFProtect
from flask_mysqldb import MySQL
from flask_login import LoginManager, current_user, login_required,login_user, logout_user
from flask_mail import Mail

from werkzeug.security import generate_password_hash, check_password_hash

from .models.entities.Compra import Compra
from .models.entities.Libro import Libro
from .models.entities.Usuario import Usuario

from .consts import *
from .emails import confirmacion_compra

from .models.ModeloCompra import ModeloCompra
from .models.ModeloUsuario import ModeloUsuario
from .models.ModeloLibro import ModeloLibro
## From es del archivo, import donde se toma la clase

app = Flask(__name__)

csrf=CSRFProtect()
db = MySQL(app)
login_manager_app = LoginManager(app) #administra los logins de la app
mail=Mail()

## Gestion correctamente de las sesiones
@login_manager_app.user_loader
def load_user(id):
    return ModeloUsuario.obtener_por_id(db,id)

############################################################
### Generador de contraseñas con SHA256
@app.route('/password/<password>')
def encriptar_password(password):
    encriptado = generate_password_hash(password)
    valor = check_password_hash(encriptado,password)
    return "Encriptado: {0} | coincide: {1}".format(encriptado,valor)
#############################################################


@app.route('/login', methods=['GET','POST'])
def login():
    #CSRF (Cross site request forgery: Solicitud de falsicificacion de sitios)
    """
    print(request.method)
    print(request.form['usuario'])
    print(request.form['password'])
    """
    """
    if request.method == 'POST':
        if request.form['usuario'] == 'admin1' and request.form['password'] == '123456':
        #print(request.form['usuario'])
        #print(request.form['password'])
            return redirect(url_for('index'))
        else:
         return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')
    
    """
    if request.method == 'POST':
        usuario = Usuario(
        None, request.form['usuario'], request.form['password'], None)
        usuario_logeado = ModeloUsuario.login(db, usuario)
        if usuario_logeado != None:
            login_user(usuario_logeado)
            flash(MENSAJE_BIENVENIDA, 'success')
            ##almacena los datos del usuario para iniciar sesion
            return redirect(url_for('index'))
        else:
            flash(LOGIN_CREDENCIALESIVALIDAS,'warning')
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')
    
@app.route('/logout')
def logout():
    logout_user()
    flash(LOGOUT, 'success')
    return redirect(url_for('login'))

@app.route('/')
@login_required  # Decorador que requiere login para ciertas rutas
def index():
    if current_user.is_authenticated:
        if current_user.tipousuario.id == 1:
            try:
                libros_vendidos = ModeloLibro.listar_libros_vendidos(db)
                data = {
                    'titulo':'Libros vendidos',
                    'libros_vendidos':libros_vendidos
                }
                return render_template('index.html', data=data)
            except Exception as ex:
                return render_template('errores/error.html', mensaje=format(ex))
        else:
            try:
                compras = ModeloCompra.listar_compras_usuario(db,current_user)
                data = {
                    'titulo': 'Mis compras',
                    'compras': compras
                }
                return render_template('index.html', data=data)
            except Exception as ex:
                return render_template('errores/error.html', mensaje=format(ex))
    else:
        return redirect(url_for('login'))
    
    
@app.route('/libros')
@login_required
def listar_libros():
    try: 
        libros = ModeloLibro.listar_libros(db)
        data = {
            'titulo':'Listado de libros',
            'libros':libros
        }
        return render_template('listado_libros.html',data=data)
    except Exception as ex:
        #print(ex)
        return render_template('errores/error.html',mensaje=format(ex))## redirige a una platilla si ocurre un error


@app.route('/comprarLibro', methods=['POST'])
@login_required
def comprar_libro():
    data_request = request.get_json()
    data={}
    try:
        #libro = Libro(data_request['isbn'],None,None,None,None)
        libro = ModeloLibro.leer_libro(db, data_request['isbn'])
        compra=Compra(None,libro,current_user)
        data['exito'] = ModeloCompra.registrar_compra(db, compra)
        confirmacion_compra (app,mail,current_user,libro)
    except Exception as ex:
        data['mensaje']=format(ex)
        data['exito']=False
    return jsonify(data)


def pagina_no_encontrada(error):
    return render_template('errores/404.html'),404


def inicializar_app(config):
    app.config.from_object(config)
    csrf.init_app(app) ## Inicia la app mediante la llave en config
    mail.init_app(app)
    app.register_error_handler(404, pagina_no_encontrada)##Manejador de errores
    app.register_error_handler(401, pagina_no_autorizada)
    return app


def pagina_no_autorizada(error):
    return redirect(url_for('login'))


