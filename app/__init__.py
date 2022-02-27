from crypt import methods
#from django.shortcuts import redirect
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

csrf=CSRFProtect()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    #CSRF (Cross site request forgery: Solicitud de falsicificacion de sitios)
    """
    print(request.method)
    print(request.form['usuario'])
    print(request.form['password'])
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

def pagina_no_encontrada(error):
    return render_template('errores/404.html'),404

def inicializar_app(config):
    app.config.from_object(config)
    csrf.init_app(app) ## Inicia la app mediante la llave en config
    app.register_error_handler(404, pagina_no_encontrada)##Manejador de errores
    return app

